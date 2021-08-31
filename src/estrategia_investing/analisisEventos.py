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
def obtenerCalendario(par,fecha1,fecha2):
    dic={}
    dic2=[]
    evento="manufacturing pmi"
    simbolo=par.split("_")[0]
    simbolo2=par.split("_")[1]
    dataframe=bd.obtenerPorEventosYFechas(evento,fecha1,fecha2)
    dataframe.set_index("id",drop=True,inplace=True)
    
   
    print(simbolo)
    print(evento)
    
    array=dataframe.loc[dataframe["currency"]==simbolo,["fecha","actual"]]
    array=array.loc[ array["actual"].notna()]
    u=np.array(array["actual"])
    
    for l in range(len(u)):
        u[l]=transformarValor(u[l])
    #array=array[array!=-1.2344]
    array["actual"]=u
  
   
    plt.plot(array["fecha"],array["actual"])
    array1=dataframe.loc[dataframe["currency"]==simbolo2,["fecha","actual"]]
    array1=array1.loc[ array1["actual"].notna()]
    u=np.array(array1["actual"])
    
    for l in range(len(u)):
        u[l]=transformarValor(u[l])
    #array=array[array!=-1.2344]
    array1["actual"]=u
  
   
    #plt.plot(array["fecha"],array["actual"])
    
  
    return array,array1


if __name__ == "__main__":
    dic={}
    dic2=[]
    file=open("eventos.txt")
    for line in file:
        dataframe1=bd.obtenerPorEventos(line)
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
        
        
            
    fig, axs = plt.subplots(numero)
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
            array["actual"]=u
            fmt_month = mdates.MonthLocator()
            axs[k].xaxis.set_minor_locator(fmt_month)
            axs[k].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
            #axs[k].xaxis.set_minor_formatter(mdates.DateFormatter('%m'))
            axs[k].plot(array["fecha"],array["actual"])
            
            axs[k].set_title(event+" "+str(symbol))
            
            k+=1
        i+=1
        
