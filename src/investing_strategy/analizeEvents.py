#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 18:44:47 2021

@author: manuel
"""
import operator
import pandas as pd
import numpy as np
import sys
sys.path.append('../../data')
import bd
import datetime as dt
from datetime import timedelta
import matplotlib.pyplot as plt
import operator  
import matplotlib.dates as mdates
bd=bd.Bd()
filtroSimbolo=True
fechaa1="2011-01-01"
fechaa2="2021-09-01"
filtro="aud"
importance="high"
def transformarValor(valor=str):
   try:
    if issubclass(type(float(valor)), float):
        return float(valor)
   except Exception as e:
    try: 
     if valor[len(valor)-1]=="%":
        #print ("Porcentaje")
        return float(valor[:-1])*100
     elif  valor[len(valor)-1]=="K":
        #print ("K")
        return  float(valor[:-1])*1000
     elif  valor[len(valor)-1]=="M":
        #print ("M")
        return float(valor[:-1])*1000000
    except:
    
         #print (valor)
        return -1.2344
def obtenerCalendario(simbolo,fecha1,fecha2,evento):
    dic={}
    dic2=[]
    #print(evento)
    
    dataframe=bd.getCalendar(evento,fecha1,fecha2,simbolo)
   
        
   
    dataframe.set_index("id",drop=True,inplace=True)
    
   
 
    
    array=dataframe.loc[:,["fecha","actual"]]
    array["date"]=array["fecha"]
    array.drop(labels=["fecha"],axis=1,inplace=True)
    #print(array)
  
   
    array=array.loc[ array["actual"].notna()]
    u=np.array(array["actual"])
    
    for l in range(len(u)):
        u[l]=transformarValor(u[l])
    #array=array[array!=-1.2344]
    array["actual"]=u
    #if evento=="cpi" and simbolo=="CAD":
    #print("Se aplica media")
    #array["actual"]=array["actual"].transform((
    #    #lambda x: x.rolling(window=8).mean()
    #    lambda x:x.ewm(span=2).mean()
    #))
    #print("Sd de la variable %s es %s"%(str(simbolo)+"_"+str(evento),np.std(u)))
  
    #print(array)
    
    
  
    return array


if __name__ == "__main__":
    dic={}
    dic2=[]
    file=open("eventos.txt")
    for line in file:
        if filtroSimbolo:
            dataframe1=bd.obtenerPorEventosFechasYSimbolo(line,fechaa1,fechaa2,filtro,importance)
        else:
            dataframe1=bd.obtenerPorEventosYFechas(line,fechaa1,fechaa2)
        dataframe1.set_index("id",drop=True,inplace=True)
        symbols= dataframe1["currency"]
        dic[line]=dataframe1
        symbols=np.unique(symbols)
        dic2.append(symbols)
    numero=0
    for e in dic.keys():
        symbols=np.unique(dic[e]["currency"])
        if len(symbols)>numero:
            numero=len(symbols)
        
        
            
    fig, axs = plt.subplots(len(dic))
    i=0
    for event in dic.keys():
        k=0
        for symbol in dic2[i]:
            print(symbol)
            print(event)
            array=dic[event].loc[dic[event]["currency"]==symbol,["fecha","actual"]]
            array=array.loc[ array["actual"].notna()]
            u=np.array(array["actual"])
            
            for l in range(len(u)):
                u[l]=transformarValor(u[l])
            #array=array[array!=-1.2344]
            print("Varianza de la variable %s es %s"%(str(symbol)+"_"+str(event),np.std(u)))
            array["actual"]=u
            fmt_month = mdates.MonthLocator()
            axs[i].xaxis.set_minor_locator(fmt_month)
            axs[i].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
            #axs[k].xaxis.set_minor_formatter(mdates.DateFormatter('%m'))
            axs[i].plot(array["fecha"],array["actual"])
            
            axs[i].set_title(event+" "+str(symbol))
            
            k+=1
        i+=1
        
