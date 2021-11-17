# -*- coding: utf-8 -*-

import json
import sys
sys.path.append("./investing_strategy")
import matplotlib.pyplot as plt
import backtrader as bt
from datetime import timedelta
import datetime as dt
import v20
import pandas as pd
import numpy as np
import time
import operator
import strategy5 as e
import configureCerebro as cC
import math
CONSTANTE=-100000
OPTIMIZE=False
INITIAL_CAPITAL=90000+10000000

file_name="./investing_strategy/results/results.csv"
 


#symbols=["EUR_USD"]
#symbols=["EUR_GBP","EUR_USD","GBP_USD","EUR_CAD","GBP_CAD","EUR_AUD","USD_CAD","AUD_CAD","EUR_NZD","AUD_NZD","NZD_USD"]
symbols=["EUR_NZD","NZD_USD"]
symbols=["NZD_JPY","EUR_JPY","USD_JPY"]
symbols=["EUR_USD","EUR_GBP","GBP_USD"]
#symbols=["AUD_CAD","AUD_NZD","NZD_CAD"]
symbols=["EUR_USD"]




f=open('lines.json')
events= json.load(f)  
fechas=["2002-01-01","2021-6-30"] 

#PARAMETERS
MAperiodLong=[19,20,21,22,23,24,25]
MAperiodShort=[6,7,8,9,10,11,12,13]
MAperiodLong2=[23,24,25]
MAperiodShort2=[14,15]

maxEntries=[10]
lookBack=4
lcompras=[0,1,2,3,4,5,6,7,8,9]
paramStopLoss=[0.25]
largo=22
corto=8
largo2=22
corto2=8
for i in range(len(fechas)-1):
    
    
    DATE1=fechas[i]
    DATE2=fechas[i+1]
    FROM = dt.datetime.strptime(DATE1,"%Y-%m-%d")
    TO= dt.datetime.strptime(DATE2,"%Y-%m-%d")
  
   
    

  
    if len(symbols)==0:
        print("No symbols")
        break
    else:
            
            #configure cerebro: add data ...
        cerebro,prize_df=cC.configureCerebro(symbols,FROM,TO,INITIAL_CAPITAL,events)
        cerebro.addobserver(bt.observers.Broker)
        for symbol1 in events.keys():
                for k   in range(len(events[symbol1])):
                    events[symbol1][k]=events[symbol1][k].replace(" ","")
        if not OPTIMIZE:
            
            #run strategy
            # run is donde with daily period. Can be change in program configurarCerebro changing the csv file and editing line 20.
           
            #print(events)
            cerebro.addstrategy(e.TestStrategy,symbols=symbols,events=events,MAperiodLong=largo,MAperiodShort=corto,MAperiodLong2=largo2,MAperiodShort2=corto2)
            thestrats = cerebro.run()
            cerebro.plot(iplot=False,start=dt.date(2002, 1, 1), end=dt.date(2021, 11, 1))
        
            thestrat = thestrats[0]
            pyfoliozer = thestrat.analyzers.getbyname('pyfolio')
            d_returns1, d_positions, d_transactions, d_gross_lev = pyfoliozer.get_pf_items()
            d_drawdown= thestrat.analyzers.getbyname("drawdown").get_analysis()
            d_returns= thestrat.analyzers.getbyname("returns").get_analysis()
            d_anualReturn= thestrat.analyzers.getbyname("anualreturn").get_analysis()
            
            array=np.array(d_returns1)
            media=array.mean()
            desv = array.std()
            sharpe=(252 * media - 0.01) / (math.sqrt(252) * desv)
            print("Drowdown %s"%d_drawdown["max"]["moneydown"])
            print("Sharpe %s"%sharpe)
            print("Number of transactions (x2) %s"%len(d_transactions))
        else:
           
            
            cerebro.optstrategy(e.TestStrategy,lookBack=lookBack,symbols=(symbols,),MAperiodLong=MAperiodLong,MAperiodShort=MAperiodShort,maxEntries=maxEntries,events=(events,),paramStopLoss=paramStopLoss)
            opt_runs = cerebro.run(stdstats=False)
            final_results_list = []
            #save reusults of backtesing
            dataframeRes=pd.DataFrame(columns=["paramStopLoss","maxEntries","longMean","shortMean","lookBack","profit","draw_down","sharpe","numberOfTransactions"])
            dataframeRes.set_index(["paramStopLoss","maxEntries","longMean","shortMean","lookBack"],inplace=True,drop=True) 
            for run in opt_runs:
                for strategy in run:
                    value = round(strategy.broker.get_value(),2)
                    PnL = round(value -INITIAL_CAPITAL,2)
                    maxEntries = strategy.params.maxEntries
                    longMean = strategy.params.MAperiodLong
                    shortMean = strategy.params.MAperiodShort
                    lookBack=strategy.params.lookBack
                    paramStopLoss=strategy.params.paramStopLoss
                    pyfoliozer = strategy.analyzers.getbyname('pyfolio')
                    d_returns1, d_positions, d_transactions, d_gross_lev = pyfoliozer.get_pf_items()
                    d_drawdown =strategy.analyzers.getbyname("drawdown").get_analysis()
                    d_returns = strategy.analyzers.getbyname("returns").get_analysis()
                    d_anualReturn = strategy.analyzers.getbyname("anualreturn").get_analysis()
                    array = np.array(d_returns1)
                    media = array.mean()
                    desv = array.std()
                    sharpe=(252 * media - 0.00) / (math.sqrt(252) * desv)
                    dataframeRes.loc[paramStopLoss,maxEntries,longMean,shortMean,lookBack]=[PnL,d_drawdown["max"]["moneydown"],sharpe,len(d_transactions)]
                 
            dataframeRes.to_csv(file_name)
