# -*- coding: utf-8 -*-

import json
import sys
sys.path.append("./estrategia_investing")
import backtrader as bt
from datetime import timedelta
import datetime as dt
import v20
import pandas as pd
import numpy as np
import time
import operator
import estrategia2 as e
import configurarCerebro as cC
import math
OPTIMIZAR=False
EVENTO_PRINCIPAL="pmi"
CAPITAL_INICIAL=300000

nombre_archivo="./estrategia_investing/resultados/resultados.csv"
 

arraySimbolos=pd.read_csv("../data/divisas.csv")
symbols=np.unique(arraySimbolos["Par"])
symbols=["EUR_USD"]
symbols=["EUR_GBP","EUR_USD","GBP_USD","EUR_CAD","GBP_CAD","EUR_AUD","USD_CAD","AUD_CAD","EUR_NZD","AUD_NZD","NZD_USD"]
symbols=["EUR_USD","EUR_GBP","GBP_USD"]
lineas={}


eventos={}
f=open('lines.json')
events= json.load(f)  
fechas=["2011-01-01","2021-04-01"] 

#PARAMETROS
MAperiodLong=[8,9,10,11,12]
MAperiodShort=[2,3,4,5,6]
maxEntradas=[10]
lookBack=4
for i in range(len(fechas)-1):
    
    
    DATE1=fechas[i]
    DATE2=fechas[i+1]
    DESDE = dt.datetime.strptime(DATE1,"%Y-%m-%d")
    HASTA= dt.datetime.strptime(DATE2,"%Y-%m-%d")
  
   
    

  
    if len(symbols)==0:
        print("No hay simbolos")
        break
    else:
            
            #configure cerebro: add data ...
        cerebro,prize_df=cC.configurarCerebro(symbols,DESDE,HASTA,CAPITAL_INICIAL,events)
        cerebro.addobserver(bt.observers.Broker)
        if not OPTIMIZAR:
            
            #run strategy
            # run is donde with daily period. Can be change in program configurarCerebro changing the csv file and editing line 20.
            for symbol1 in events.keys():
                for k   in range(len(events[symbol1])):
                    events[symbol1][k]=events[symbol1][k].replace(" ","")
          
            cerebro.addstrategy(e.TestStrategy,symbols=symbols,events=events)
            thestrats = cerebro.run()
            cerebro.plot(iplot=False,start=dt.date(2010, 4, 9), end=dt.date(2021, 3, 1))
        
            thestrat = thestrats[0]
            pyfoliozer = thestrat.analyzers.getbyname('pyfolio')
            d_returns1, d_positions, d_transactions, d_gross_lev = pyfoliozer.get_pf_items()
            d_drawdown= thestrat.analyzers.getbyname("drawdown").get_analysis()
            d_returns= thestrat.analyzers.getbyname("returns").get_analysis()
            d_anualReturn= thestrat.analyzers.getbyname("anualreturn").get_analysis()
            #d_sharpe=thestrat.analyzers.getbyname("sharpe").get_analysis()
            array=np.array(d_returns1)
            media=array.mean()
            desv = array.std()
            sharpe=(252 * media - 0.01) / (math.sqrt(252) * desv)
            print("Drowdown %s"%d_drawdown["max"]["moneydown"])
            print("Sharpe %s"%sharpe)
            print("Numero de transacciones (x2) %s"%len(d_transactions))
        else:
            strategy=e.TestStrategy()
            
            cerebro.optstrategy(strategy,lookBack=lookBack,symbols=(symbols,),MAperiodLong=MAperiodLong,MAperiodShort=MAperiodShort,maxEntradas=maxEntradas,events=(events,))
            opt_runs = cerebro.run(stdstats=False)
            final_results_list = []
            #save reusults of backtesing
            dataframeRes=pd.DataFrame(columns=["maxEntradas","mediaLarga","mediaCorto","lookBack","beneficio","draw_down","sharpe","numeroTransacciones"])
            dataframeRes.set_index(["maxEntradas","mediaLarga","mediaCorto","lookBack"],inplace=True,drop=True) 
            for run in opt_runs:
                for strategy in run:
                    value = round(strategy.broker.get_value(),2)
                    PnL = round(value - CAPITAL_INICIAL,2)
                    maxEntradas = strategy.params.maxEntradas
                    mediaMovilLargo = strategy.params.MAperiodLong
                    mediaMovilCorto = strategy.params.MAperiodShort
                    lookBack=strategy.params.lookBack
                  
                    pyfoliozer = strategy.analyzers.getbyname('pyfolio')
                    d_returns1, d_positions, d_transactions, d_gross_lev = pyfoliozer.get_pf_items()
                    d_drawdown =strategy.analyzers.getbyname("drawdown").get_analysis()
                    d_returns = strategy.analyzers.getbyname("returns").get_analysis()
                    d_anualReturn = strategy.analyzers.getbyname("anualreturn").get_analysis()
                    array = np.array(d_returns1)
                    media = array.mean()
                    desv = array.std()
                    sharpe=(252 * media - 0.01) / (math.sqrt(252) * desv)
                    dataframeRes.loc[maxEntradas,mediaMovilLargo,mediaMovilCorto,lookBack]=[PnL,d_drawdown["max"]["moneydown"],sharpe,len(d_transactions)]
                 
            dataframeRes.to_csv(nombre_archivo)
