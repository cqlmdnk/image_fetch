# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 18:48:26 2020

@author: bbari
"""

import mysql.connector
import pandas as pd


def add_movies_actor(cursor, movieID, personID):
    sql = "INSERT INTO movieactor (movieID, personID) VALUES (%s, %s)"
    val = ( movieID, personID)
    try:
        ret = cursor.execute(sql, val)
    except Exception as e:
        print(e)
    
def add_movies_director(cursor, movieID, personID):
    sql = "INSERT INTO moviedirector (movieID, personID) VALUES (%s, %s)"
    val = ( movieID, personID)
    try:
        ret = cursor.execute(sql, val)
    except Exception as e:
        print(e)
    
def add_movies_writer(cursor, movieID, personID):
    sql = "INSERT INTO moviewriter (movieID, personID) VALUES (%s, %s)"
    val = ( movieID, personID)
    try:
        ret = cursor.execute(sql, val)
    except Exception as e:
        print(e)
        
    

def add_movie(cursor, movieDf):
    sql = "INSERT INTO movie (movieName, releaseYear, duration, rating, ratingCount, nation, imageUrl, movieInfo, ageLimit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = ( movieDf['name'], movieDf['year'], movieDf['duration'], float(movieDf['rating']), int(movieDf['ratingCount'].replace(",","")), movieDf['nation'], movieDf['imageUrl'], movieDf['info'], movieDf['limit'] )
    ret = cursor.execute(sql, val)
    id_ret_sql = "SELECT movieID FROM movie WHERE movieName = %s"
    name = ( movieDf['name'],)
    cursor.execute(id_ret_sql, name)
    myresult = cursor.fetchall()
    return myresult[0][0]



mydb = mysql.connector.connect(
  host="localhost",
  user="pbosf",
  password="power25",
  database="moviedatabase"
)


mycursor = mydb.cursor()



dataset = pd.read_csv('movies.csv' )


for i in range(250):
    if i == 155:
        continue
    try:
        movieID = add_movie(mycursor, dataset.iloc[i,:])
    except:
        continue
    actors = dataset.iloc[i, 9].split(",")
    
    for actor in actors:
        id_ret_sql = "SELECT personID FROM person WHERE personName = %s"
        name = ( actor.strip(),)
        mycursor.execute(id_ret_sql, name)
        try:
            personID = mycursor.fetchall()[0][0]
            add_movies_actor(mycursor, movieID, personID)
        except:
            continue
    writers = dataset.iloc[i, 10].split(",")
    for writer in writers:
        id_ret_sql = "SELECT personID FROM person WHERE personName = %s"
        name = ( writer.split("(")[0].strip(),)
        mycursor.execute(id_ret_sql, name)
        try:
            personID = mycursor.fetchall()[0][0]
            add_movies_writer(mycursor, movieID, personID)
        except:
            continue
    directors = dataset.iloc[i, 11].split(",")
    for director in directors:
        id_ret_sql = "SELECT personID FROM person WHERE personName = %s"
        name = ( writer.split("(")[0].strip(),)
        mycursor.execute(id_ret_sql, name)
        try:
            personID = mycursor.fetchall()[0][0]
            add_movies_director(mycursor, movieID, personID)
        except:
            continue
    
    
    
    
    
    
mydb.commit()   
    
    
    
    
    
    
    
    
    
    
    
    
    
    