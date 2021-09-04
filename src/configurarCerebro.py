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
def configurarCerebro(symbols,DESDE,HASTA,CAPITAL_INICIAL,eventos:{}):
    cerebro = bt.Cerebro(optreturn=False,maxcpus=2,optdatas=True)
       
    for symbol in symbols:
            i=0
         
            prize_df = pd.read_csv("../data/divisasSpreadHurstD1/" + symbol + ".csv")
            prize_df.drop(labels=["hurst","half_life"],axis=1,inplace=True)
            prize_df["time"] = pd.to_datetime(prize_df['time'])
            prize_df = prize_df.loc[operator.__and__(prize_df.loc[:, "time"] >=DESDE,
                                prize_df.loc[:, "time"] <= HASTA )]
            prize_df["time"]=prize_df["time"].dt.normalize()
            prize_df.set_index("time",drop=True,inplace=True)
            prize_df.drop(labels="index",axis=1,inplace=True)
            simbolo1=symbol.split("_")[0]
            simbolo2=symbol.split("_")[1]
            for simbolo in [simbolo1,simbolo2]:
                for evento in eventos[simbolo]:
                  
                    i+=1
                    calendario=events.obtenerCalendario(simbolo,DESDE,HASTA,evento)
                    calendario["fecha"]=pd.to_datetime(calendario["fecha"],)
            
           
                    calendario["fecha"]=calendario["fecha"].dt.normalize()
            
                    prize_df["eventos"+str(i)]=0
            
                    calendario.set_index(keys=["fecha"],drop=True,inplace=True)
                   
          
          
    
                    for fecha in calendario.index.values:
                        #print("%s %s"%(fecha,calendario.loc[fecha,"actual"]))
                        try:
                            prize_df.loc[fecha,"eventos"+str(i)]=calendario.loc[fecha,"actual"]
                        except Exception as e:
                            prize_df.loc[fecha,"eventos"+str(i)]=calendario.loc[fecha,"actual"][0]
           
           
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
            
    return cerebro,prize_df
