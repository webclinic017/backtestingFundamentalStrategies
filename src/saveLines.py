#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 14:43:37 2021

@author: manuel
"""
import json
symbols=["NZD_JOY","EUR_JPY","USD_JPY","GBP_JPY"]

symbols=["EUR_USD","EUR_GBP","GBP_USD"]
symbols=["AUD_CAD","AUD_NZD","CAD_NZD","AUD_JPY","CAD_JPY","EUR_USD","EUR_GBP","GBP_USD"]
symbols=["EUR_USD"]
#symbols=["EUR_USD","EUR_GBP","GBP_USD"]

lines={}
pares=[]
for symbol in symbols:
    array=symbol.split("_")
  
    if array[0] not in pares:
        pares.append(array[0])
    if  array[1] not in pares:
        pares.append(array[1])
for symbol in pares:
 if symbol=="EUR":   
    lines["EUR"]=["german manufacturing","cpi"]
 if symbol=="USD":
     
    lines["USD"]=["ISM manufacturing pmi","cpi"]
 if symbol=="GBP":
    lines["GBP"]=["manufacturing pmi","cpi "]
 if symbol=="NZD":
    lines["NZD"]=["BUSINESS NZ PMI","cpi"]
 if symbol=="JPY":
    lines["JPY"]=["Services pmi","National Core CPI"]
 if symbol=="CAD":
    lines["CAD"]=["pmi","cpi"]
 if symbol=="AUD":
    lines["AUD"]=["aig manufacturing index","cpi"]
"""for symbol in pares:
    lines[symbol].append("gdp")
    lines[symbol].append("retail sales")"""
    
   



with open('lines.json', 'w') as json_file:
  json.dump(lines, json_file)