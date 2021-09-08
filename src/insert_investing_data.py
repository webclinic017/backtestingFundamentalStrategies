# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 19:55:04 2021

@author: Manuel
"""


from  investpy import news
import datetime as dt
import pytz as tz
from datetime import timedelta
import pandas as pd
import operator
import json
import sys
sys.path.append('./investing_strategy/')
import  bd
def transformarValor(valor=str):
    if valor[len(valor)-1]=="%":
        print ("Porcentaje")
    elif  valor[len(valor)-1]=="K":
        print ("K")
    elif  valor[len(valor)-1]=="M":
        print ("M")
    else:
        print (valor)
    
bd=bd.Bd()
date1=dt.datetime(2004,1,1)
date2=dt.datetime(2005,1,1)
print(date1.strftime("%Y/%m/%d"))
calendar=news.economic_calendar(from_date=date1.strftime("%d/%m/%Y"),to_date=date2.strftime("%d/%m/%Y"))
calendar=calendar.loc[operator.__or__(calendar.loc[:,"importance"]=="high", calendar.loc[:,"importance"]=="high")]

print(calendar.tail())

for e in calendar.index:
    try:
        array=[]
        array.append(calendar.loc[e,"forecast"])
        array.append(calendar.loc[e,"actual"])
        array.append(calendar.loc[e,"previous"])
        date=str(calendar.loc[e,"date"])
        year=date.split("/")[2]
        month=date.split("/")[1]
        day=date.split("/")[0]
        fecha=year+"/"+month+"/"+day
        bd.addCalendar(calendar.loc[e,"id"],fecha+" "+str(calendar.loc[e,"time"]),calendar.loc[e,"zone"],calendar.loc[e,"currency"],calendar.loc[e,"importance"],calendar.loc[e,"event"],calendar.loc[e,"actual"],calendar.loc[e,"forecast"],calendar.loc[e,"previous"])
    except Exception as u:
        print (u)
