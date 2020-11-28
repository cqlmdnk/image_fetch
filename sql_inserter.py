import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
  host="localhost",
  user="pbosf",
  password="power25",
  database="moviedatabase"
)

results = pd.read_csv('person_row.csv', header=None )


mycursor = mydb.cursor()




for i in range(1162):
    sql = "INSERT INTO person (personName, personBirth, personImageUrl, personInfo) VALUES (%s, %s, %s, %s)"
    val = (str(results.iloc[i,0]), str(results.iloc[i,1]), str(results.iloc[i,2]), str(results.iloc[i,3]))
    ret = mycursor.execute(sql, val)
    
mydb.commit()