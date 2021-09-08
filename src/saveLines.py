#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 14:43:37 2021

@author: manuel
"""
import json
symbols=["EUR_USD","EUR_GBP","GBP_USD"]
lines={}
lines["EUR"]=["manufacturing pmi","cpi"]
lines["USD"]=["ISM manufacturing pmi","cpi"]
lines["GBP"]=["manufacturing pmi","cpi"]


with open('lines.json', 'w') as json_file:
  json.dump(lines, json_file)