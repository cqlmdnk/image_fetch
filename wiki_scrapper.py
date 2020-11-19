# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 20:22:38 2020

@author: bbari
"""

import time
import io, sys, os, hashlib
import pandas as pd
import wikipedia

df = pd.DataFrame(columns = ['info'])

col_names = ["nconst", "image"]
imdb_dataset = pd.read_csv('name.basics_0.csv', sep='\t')
names = pd.read_csv('names_images.csv', names = col_names )




result = pd.concat([names,imdb_dataset[["primaryName","birthYear"]] ], axis=1, sort=False)

i = 0
for loc, row in result.iterrows():
    i=i+1
    try:
        new_row = {'info': wikipedia.summary(row['primaryName'])}
        df = df.append(new_row, ignore_index =True)
    except:
        new_row = {'info': 'No information found.'}
        df = df.append(new_row, ignore_index =True)
    
    print(new_row)
    if(i==2000):
        break
    
result = pd.concat([result, df ], axis=1, sort=False)
result.to_csv('results.csv', mode='a', header=False, index=False)