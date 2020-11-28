# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 00:46:52 2020

@author: bbari
"""
import pandas as pd
import wikipedia
import io, sys, os, hashlib
from selenium import webdriver
from image_scrapper import search_and_download
import wikipedia
column_names = ["personName", "birthDate", "imageUrl", "info"]

df = pd.DataFrame(columns = column_names)

dataset = pd.read_csv('moovies.csv' )

dataset = dataset.iloc[:, -3:-1].values

pure_names = []

## awwww shit what the heckkkk!!! written when high otherwise, wouldn't bother to mess this shit
for item in dataset:
    for name in item:
        if("," in name):
            names = name.split(",")
            for string in names :
                if("(" in string):
                    if("|" in string.split("(")[0]):
                        pure_names.append( string.split("(")[0].split("|")[0])
                    else:
                        pure_names.append( string.split("(")[0])
                else:
                    if("|" in string):
                        pure_names.append( string.split("|")[0])
                    else:
                        pure_names.append( string)
        else:
            if("(" in name):
                pure_names.append(name.split("(")[0])
            else:
                if("|" in name):
                    pure_names.append(name.split("|")[0])
                else:
                    pure_names.append(name)

pure_names.remove("actors") ##// some fucked headers
pure_names.remove("writers") ##// dont mind these lines


chrome_options = webdriver.chrome.options.Options()  
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")

i = 0
from webdriver_manager.chrome import ChromeDriverManager
wd = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
for name in pure_names:
    try:
        information = wikipedia.summary(name, auto_suggest= False)
    except:
        try:
            information = wikipedia.summary(name+ " (actor)", auto_suggest= True)
        except:
            continue
    try:
        birthDate = information.split("born")[1].split(")")[0]
    except:
        birthDate = "NaN"
    df2 = pd.DataFrame([[name, birthDate,  search_and_download(wd, name, 'chromedriver.exe', number_images=1), information]], columns = column_names)
    df = pd.concat([df2, df])
    
    i = i+1
    print("Progress: %" + "{:06.2f}".format((i/len(pure_names)*100)))
     
        
df.to_csv('person_row.csv', mode='a', header=False, index=False) 
    
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     