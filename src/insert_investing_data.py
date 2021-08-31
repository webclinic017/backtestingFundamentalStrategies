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
sys.path.append('../estrategia_investing')
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
fecha1=dt.datetime(2004,1,1)
fecha2=dt.datetime(2005,1,1)
print(fecha1.strftime("%Y/%m/%d"))
calendario=news.economic_calendar(from_date=fecha1.strftime("%d/%m/%Y"),to_date=fecha2.strftime("%d/%m/%Y"))
calendario=calendario.loc[operator.__or__(calendario.loc[:,"importance"]=="high", calendario.loc[:,"importance"]=="high")]

print(calendario.tail())

for e in calendario.index:
    try:
        array=[]
        array.append(calendario.loc[e,"forecast"])
        array.append(calendario.loc[e,"actual"])
        array.append(calendario.loc[e,"previous"])
        fecha=str(calendario.loc[e,"date"])
        año=fecha.split("/")[2]
        mes=fecha.split("/")[1]
        dia=fecha.split("/")[0]
        fecha=año+"/"+mes+"/"+dia
        bd.añadirCalendario(calendario.loc[e,"id"],fecha+" "+str(calendario.loc[e,"time"]),calendario.loc[e,"zone"],calendario.loc[e,"currency"],calendario.loc[e,"importance"],calendario.loc[e,"event"],calendario.loc[e,"actual"],calendario.loc[e,"forecast"],calendario.loc[e,"previous"])
    except Exception as u:
        print (u)
