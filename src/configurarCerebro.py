#configure cerebro for stationarity and momentum stratgies
import backtrader as bt
import pandas as pd
import operator
import sys
sys.path.append("estrategia")
import analisisEventos as events
import dataFeed as dF
import numpy as np 
import time
import datetime as dt
def comprobarSpreads(symbol,prize_df):
    spread1=prize_df["spread"].mean()
    close1=prize_df["close"].mean()

    print("Simbolo %s :SPREAD %s, CLOSE %s"%(symbol,spread1,close1))
  
    if spread1/close1>0.001 :
        print("Spread demasiado alto")
        return False
    return True
def configurarCerebro(symbols,DESDE,HASTA,CAPITAL_INICIAL):
    cerebro = bt.Cerebro(optreturn=False,maxcpus=2,optdatas=True)
       
    for symbol in symbols:
            print(symbol)
            prize_df = pd.read_csv("../data/divisasSpreadHurstD1/" + symbol + ".csv")
            prize_df.drop(labels=["hurst","half_life"],axis=1,inplace=True)
            prize_df["time"] = pd.to_datetime(prize_df['time'])
            prize_df = prize_df.loc[operator.__and__(prize_df.loc[:, "time"] >=DESDE,
                                prize_df.loc[:, "time"] <= HASTA )]
            prize_df["time"]=prize_df["time"].dt.normalize()
            prize_df.set_index("time",drop=True,inplace=True)
            prize_df.drop(labels="index",axis=1,inplace=True)
            data = dF.PandasData1(dataname=prize_df, name=symbol)
            calendario1,calendario2=events.obtenerCalendario(symbol,DESDE,HASTA)
           
            calendario1["fecha"]=pd.to_datetime(calendario1["fecha"])
            calendario2["fecha"]=pd.to_datetime(calendario2["fecha"])
           
            calendario1["fecha"]=calendario1["fecha"].dt.normalize()
            calendario2["fecha"]=calendario2["fecha"].dt.normalize()
            prize_df["eventos1"]=0
            prize_df["eventos2"]=0
            calendario1.set_index(keys=["fecha"],drop=True,inplace=True)
            calendario2.set_index(keys=["fecha"],drop=True,inplace=True)
          
    
            for fecha in calendario1.index.values:
            
                prize_df.loc[fecha,"eventos1"]=calendario1.loc[fecha,"actual"]
            for fecha in calendario2.index.values:  
        
                prize_df.loc[fecha,"eventos2"]=calendario2.loc[fecha,"actual"]
           
            prize_df=prize_df.loc[prize_df["close"].notna()]
            data = dF.PandasData1(dataname=prize_df, name=symbol)
        
            cerebro.adddata(data)     
    
    cerebro.broker.setcash(CAPITAL_INICIAL)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10000)
    cerebro.addanalyzer(bt.analyzers.PyFolio)
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name="drawdown")
    cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name="anualreturn")
    k = {}
    k["timeframe"] = bt.TimeFrame.Days
    k["tann"] = 252
    cerebro.addanalyzer(bt.analyzers.Returns, _name="returns", **k)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
            
    return cerebro,prize_df,calendario1,calendario2
