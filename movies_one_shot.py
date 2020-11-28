# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 20:14:00 2020

@author: bbari
"""


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import pandas as pd


   
def get_movie_row(title_wrapper, posterUrl, rating, info, col_names):
    information = ""
    name = title_wrapper.text.split("\n")[0].split("(")[0]
    year = title_wrapper.text.split("\n")[0].split("(")[1].split(")")[0]
    if("|" in title_wrapper.text.split("\n")[1] ):
        temp = title_wrapper.text.split("\n")[1]
    else:
        temp = title_wrapper.text.split("\n")[2]
    limit = temp.split("|")[0]
    duration = temp.split("|")[1]
    information += temp.split("|")[2]
    nation = temp.split("|")[3].split("(")[1].split(")")[0]
    
    imageUrl = posterUrl
    
    ratingfloat = rating.text.split("\n")[0].split("/")[0]
    ratingCount = rating.text.split("\n")[1]
    
    information += info.text.split("\n")[0]
    if(":" in info.text.split("\n")[1]):
        directors = info.text.split("\n")[1].split(":")[1]
        writers = info.text.split("\n")[2].split(":")[1]
        actors = info.text.split("\n")[3].split(":")[1].split("|")[0]
    else:
        directors = info.text.split("\n")[2].split(":")[1]
        writers = info.text.split("\n")[3].split(":")[1]
        actors = info.text.split("\n")[4].split(":")[1].split("|")[0]
   
    return pd.DataFrame([[name, year, duration, ratingfloat, ratingCount, nation, imageUrl, information, limit, actors, writers, directors]], columns=col_names)
    





column_names = ["name", "year", "duration" , "rating", "ratingCount", "nation", "imageUrl", "info", "limit", "actors", "writers", "directors"]
df = pd.DataFrame(columns = column_names)


chrome_options = webdriver.chrome.options.Options()  
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless") 
from webdriver_manager.chrome import ChromeDriverManager
wd = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)


page = wd.get("https://www.imdb.com/chart/top/")
list_elem = wd.find_elements_by_class_name("lister-list")

titles = list_elem[0].find_elements_by_class_name("titleColumn")
title_tag_as = []

for title in titles:
    title_tag_as.append(title.find_elements_by_tag_name("a"))
links = [elem[0].get_attribute('href') for elem in title_tag_as]


i = 0
for link in links:
    i = i +1
    if(i < 155):
        continue
    wd = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    title_page = wd.get(link)
    wait = WebDriverWait(wd, 20)
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "title_wrapper")))
    title_wrapper =  wd.find_elements_by_class_name('title_wrapper')
    print(title_wrapper[0].text)
    posterUrl = wd.find_elements_by_class_name('poster')
    posterUrl =  posterUrl[0].find_elements_by_tag_name("img")[0].get_attribute('src')
    
    
    rating =  wd.find_elements_by_class_name("ratings_wrapper")
    
    info = wd.find_elements_by_class_name("plot_summary")
    try:
        df2 =  get_movie_row(title_wrapper[0], posterUrl, rating[0], info[0], column_names)
        df = pd.concat([df2, df])
    except:
        continue
    wd.quit()
 
    
df.to_csv('moovies.csv', mode='a', index=False)