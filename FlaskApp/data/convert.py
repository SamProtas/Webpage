import urllib2
import json
import datetime
import pandas as pd
import numpy as np
import sqlite3
import os

conn = sqlite3.connect('HG.db')
c = conn.cursor()

#data= pd.read_sql('SELECT * FROM stats', conn) #database to a dataframe 'data'
#data.to_csv('HG_data_csv.csv')

csv = pd.read_csv('HG_data_csv.csv')
csv.to_sql('stats', conn, if_exists='replace',index=False)
conn.commit()
conn.close()


