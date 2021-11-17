# file to analize results of backtesting of momentum and stationarity

import datetime as dt
import pandas as pd
import numpy as np



dataframe=pd.read_csv("./investing_strategy/results/results.csv")

#dataframe=dataframe.iloc[220:]
for column in dataframe.columns:
    if column!="sharpe" and column!="draw_down" and column!="numberOfTransactions" and column!="profit":
        
        print("Column name %s"%column)
        print("Porfit:")
        print(dataframe.groupby(column)["profit"].mean())
        print("Max drawdown:")
        print(dataframe.groupby(column)["draw_down"].mean())
        print("Sharpe:")
        print(dataframe.groupby(column)["sharpe"].mean())
        print("Numero of transactiond:")
        print(dataframe.groupby(column)["numberOfTransactions"].mean())
        
    

print(dataframe.groupby(["shortMean","longMean","lookBack"])["profit"].mean())

print(dataframe.groupby(["shortMean","longMean","lookBack"])["draw_down"].mean())
print(dataframe.groupby(["maxEntries","shortMean","longMean","lookBack"])["sharpe"].mean())
beneficios=pd.DataFrame(dataframe.groupby(["maxEntries","shortMean","longMean","lookBack"])["profit"].mean())
print(np.array((dataframe["profit"])).mean())
print(np.array((dataframe["draw_down"])).mean())
