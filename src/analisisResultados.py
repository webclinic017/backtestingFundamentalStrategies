# file to analize results of backtesting of momentum and stationarity
import backtrader as bt
import datetime
import math
import os.path
import sys

import datetime as dt
import v20
import pandas as pd
import numpy as np
import time
import argparse
import operator
import matplotlib.pyplot
from sklearn.linear_model import LinearRegression
#change ESTRATEGIA to momentum or estacionaridad

dataframe=pd.read_csv("./estrategia_investing/resultados/resultados.csv")

#dataframe=dataframe.iloc[220:]
for columna in dataframe.columns:
    if columna!="sharpe" and columna!="draw_down" and columna!="numeroTransacciones" and columna!="beneficio":
        
        print("Nombre de columna %s"%columna)
        print("Beneficio:")
        print(dataframe.groupby(columna)["beneficio"].mean())
        print("Max drawdown:")
        print(dataframe.groupby(columna)["draw_down"].mean())
        print("Sharpe:")
        print(dataframe.groupby(columna)["sharpe"].mean())
        print("Numero de transacciones:")
        print(dataframe.groupby(columna)["numeroTransacciones"].mean())
        
    

print(dataframe.groupby(["maxEntradas","mediaCorto","mediaLarga","lookBack"])["beneficio"].mean())

print(dataframe.groupby(["maxEntradas","mediaCorto","mediaLarga","lookBack"])["draw_down"].mean())
print(dataframe.groupby(["maxEntradas","mediaCorto","mediaLarga","lookBack"])["sharpe"].mean())
beneficios=pd.DataFrame(dataframe.groupby(["maxEntradas","mediaCorto","mediaLarga","lookBack"])["beneficio"].mean())
print(np.array((dataframe["beneficio"])).mean())
print(np.array((dataframe["draw_down"])).mean())
