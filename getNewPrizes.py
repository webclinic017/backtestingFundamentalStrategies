#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 21:37:14 2021

@author: manuel
"""
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 10:00:53 2021

@author: Manuel
"""
import v20
import pandas as pd
import datetime as dt
import numpy as np
hostname="api-fxpractice.oanda.com"
port=443
token="27a60e08b57a7d98a03f6ff52a178b65-ffdb0f12cdd0ef2b679adcd8dd2a969c"
cuenta="101-004-17279313-006"
ssl=True
datetime_format="UNIX"
periodicidad="D"

ctx = v20.Context(
            hostname,
            port,
            ssl,
            application="sample_code",
            token=token,
            datetime_format=datetime_format
        )


kwargs={}
kwargs["granularity"] = periodicidad

kwargs["price"] = "B"
symbol="GBP_USD"
kwargs["count"]=5000
prize_df = pd.read_csv("./data/divisasSpreadD1/" + symbol + ".csv")
prize_df["time"] = pd.to_datetime(prize_df['time'])+pd.Timedelta(hours=2)
prize_df.set_index("time",drop=True,inplace=True)     

today = dt.datetime(2021,11,15,0).timestamp()
desde = dt.datetime(2021,7,22, 0).timestamp()
kwargs["fromTime"] = desde
print("Today inicial: %s para simbolo %s"%(dt.datetime.fromtimestamp(today),symbol))
print("Desde inicial: %s para simbolo %s"%(dt.datetime.fromtimestamp(desde),symbol))
while(desde<today):
    try:
        kwargs["price"] = "B"
        response = ctx.instrument.candles(symbol, **kwargs)

        kwargs["price"] = "A"
        response3 = ctx.instrument.candles(symbol, **kwargs)
        z = response.get("candles", 200)
        z3= response3.get("candles", 200)

        j=0
        for i in z:
            prize_df.loc[dt.datetime.fromtimestamp(float(i.time))]=[i.bid.c,i.bid.o,i.bid.l,i.bid.h,i.volume,z3[j].ask.c - z[j].bid.c]
            j+=1
        desde= float(z[len(z)-1].time)+60*60
        kwargs["fromTime"]=desde
        print("TIEMPO DE PARADA %s"%dt.datetime.fromtimestamp(desde))
    except:
        print("error en simbolo "+str(symbol))
nombre_archivo="./data/divisasSpreadD1v3/" + symbol + ".csv"
prize_df.to_csv(nombre_archivo)
a=pd.read_csv(nombre_archivo)
a.index=a["time"]
a=a.drop(labels="time",axis=1)