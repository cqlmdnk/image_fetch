# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 21:43:17 2020

@author: bbari
"""
from selenium import webdriver
import pandas as pd
from image_scrapper import search_and_download


column_names = ["nconst", "imageURL"]


df = pd.DataFrame(columns = column_names)

chrome_options = webdriver.chrome.options.Options()  
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless") 
from webdriver_manager.chrome import ChromeDriverManager
wd = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)


for i in range(27):
    dataset = pd.read_csv('name.basics_{:d}.csv'.format(i), sep='\t')
    print('name.basics_{:d}.csv'.format(i))
    for index, row in dataset.iterrows():
        try:
            df = df.append({'nconst': row['nconst'], 'imageURL': search_and_download(wd,row['primaryName'], 'chromedriver.exe', number_images=1)}, ignore_index=True)
            print(row['nconst'], row['primaryName'])
        except Exception as e:
            df = df.append({'nconst': row['nconst'], 'imageURL': "null"}, ignore_index=True)
            print("can't add image url")
            print(e)
        df.to_csv('names_images.csv', mode='a', header=False, index=False)
        df = pd.DataFrame(columns = column_names)
    del dataset    
