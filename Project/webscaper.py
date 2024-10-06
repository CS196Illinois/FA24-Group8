import requests
from bs4 import BeautifulSoup
import numpy as np 
import pandas as pd


#For the mysql database connection
"""
!pip3 install pymysql
import pymysql
import os
timeout = 10
connection = pymysql.connect(
  charset="utf8mb4",
  connect_timeout=timeout,
  cursorclass=pymysql.cursors.DictCursor,
  db="defaultdb",
  host=os.getenv('db_host'),
  password=os.getenv('db_password'),
  read_timeout=timeout,
  port=os.getenv('db_port'),
  user= os.getenv('db_user'),
  write_timeout=timeout,
)

try:
  cursor = connection.cursor()
  cursor.execute("CREATE TABLE mytest (id INTEGER PRIMARY KEY)")
  cursor.execute("INSERT INTO mytest (id) VALUES (1), (2)")
  cursor.execute("SELECT * FROM mytest")
  print(cursor.fetchall())
finally:
  connection.close()
"""

#code from alice 
data = []
for i in range(9):
    url = "https://researchops.web.illinois.edu/?page=" + str(i)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')  
        table_rows = soup.find_all('tr') 

        for row in table_rows:
            columns = row.find_all('td')
            row_data = [column.text.strip() for column in columns]
            if row_data:  
                data.append(row_data)

df = pd.DataFrame(data, columns=["Description", "Research Area", "Timing", "Deadline"])
