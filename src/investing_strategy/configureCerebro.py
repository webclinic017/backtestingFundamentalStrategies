#configure cerebro for stationarity and momentum stratgies
import backtrader as bt
import pandas as pd
import operator
import analizeEvents as aE
import numpy as np 
import datetime as dt
def checkSpreads(symbol,prize_df):
    spread1=prize_df["spread"].mean()
    close1=prize_df["close"].mean()

    
    if spread1/close1>0.001 :
        print("Spread to high")
        return False
    return True
def configureCerebro(symbols,FROM,TO,INITIAL_CAPITAL,events:{}):
    cerebro = bt.Cerebro(optreturn=False,maxcpus=2,optdatas=True)
       
    for symbol in symbols:
            i=0
         
            prize_df = pd.read_csv("../data/divisasSpreadHurstD1/" + symbol + ".csv")
            prize_df.drop(labels=["hurst","half_life"],axis=1,inplace=True)
            prize_df["time"] = pd.to_datetime(prize_df['time'])
            prize_df = prize_df.loc[operator.__and__(prize_df.loc[:, "time"] >=FROM,
                                prize_df.loc[:, "time"] <= TO )]
            prize_df["time"]=prize_df["time"].dt.normalize()
            prize_df.set_index("time",drop=True,inplace=True)
            prize_df.drop(labels="index",axis=1,inplace=True)
            symbol1=symbol.split("_")[0]
            symbol2=symbol.split("_")[1]
            for symbol3 in [symbol1,symbol2]:
                i+=1
                for event in events[symbol3]:
                  
                   
                    calendario=aE.obtenerCalendario(symbol3,FROM,TO,event)
                    calendario["date"]=pd.to_datetime(calendario["date"],)
            
           
                    calendario["date"]=calendario["date"].dt.normalize()
            
                    prize_df[event+str(i)]=0
            
                    calendario.set_index(keys=["date"],drop=True,inplace=True)
                   
          
          
    
                    for date in calendario.index.values:
                   
                        #print("%s %s"%(fecha,calendario.loc[fecha,"actual"]))
                        try:
                            prize_df.loc[date,event+str(i)]=calendario.loc[date,"actual"]
                        except Exception as e:
                            prize_df.loc[date,event+str(i)]=calendario.loc[date,"actual"][0]
           
           
            prize_df=prize_df.loc[prize_df["close"].notna()]
          
            lines=["spread"]
            for event in [symbol1,symbol2]:
             if event==symbol1: 
                for e in events[event]:
                    lines.append((e+str(0)).replace(" ",""))
             elif event==symbol2:
                for e in events[event]:
                    lines.append((e+str(1)).replace(" ",""))
                 
          
           
            k=5
            params=[]
            for line in lines:
                param=tuple([line,k])
                params.append(param)
                k+=1
            params=tuple(params)
          
            #print(params)
                
         
            
            mydict = dict(lines=tuple(lines), params =params,
    datafieds=bt.feeds.PandasData.datafields +lines)
           
            MyPandasClass = type(symbol, (bt.feeds.PandasData,), mydict)
            setattr(bt.metabase, symbol, MyPandasClass)
            data = MyPandasClass (dataname=prize_df, name=symbol)
            cerebro.adddata(data)     
    
    cerebro.broker.setcash(INITIAL_CAPITAL)
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
