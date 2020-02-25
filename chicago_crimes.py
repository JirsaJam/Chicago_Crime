# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 14:54:48 2020

@author: jjirsa
"""

import pandas as pd
from sodapy import Socrata
import numpy as np
import seaborn as sns
import datetime

distance = 1

client = Socrata("data.cityofchicago.org", None)
results = client.get('ijzp-q8t2', where = "year > '2019'", limit = 50000)
df1 = pd.DataFrame(data = results)
df1 = df1.rename(columns ={'latitude': 'cust_lat', 'longitude': 'cust_lon'})
df1 = df1.dropna(subset = ['cust_lat'])
df1['date'] = df1['date'].astype(str)
df1['date'] = df1['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f'))
df1['hh:mm'] = df1['date'].dt.strftime('%H:%M')
df1['hour'] = df1['date'].dt.hour.astype(int)
df1['min'] = df1['date'].dt.minute.astype(int)
df1['dt'] = pd.to_datetime(df1['hh:mm'])

df1['event_lat'] = 41.9244051
df1['event_lon'] = -87.6645583

df1[['event_lat', 'event_lon', 'cust_lat', 'cust_lon']] = df1[['event_lat', 'event_lon', 'cust_lat', 'cust_lon']].astype(float) 

df1['event_lon'] = df1['event_lon'] * np.pi / 180
df1['event_lat'] = df1['event_lat'] * np.pi / 180
df1['cust_lon'] = df1['cust_lon'] * np.pi / 180
df1['cust_lat'] = df1['cust_lat'] * np.pi / 180
df1['dlon'] = df1['event_lon'] - df1['cust_lon']
df1['dlat'] = df1['event_lat'] - df1['cust_lat']
df1['a'] = np.sin(df1['dlat']/2.0)**2 + np.sin(df1['dlon']/2.0)**2 * np.cos(df1['cust_lat']) * np.cos(df1['event_lat'])
df1['c'] = 2 * np.arcsin(np.sqrt(df1['a']))
df1['dist'] = (6367 * df1['c']) * 0.621371
df1[f'{distance}+'] = df1[f'dist'] > distance
df1 = df1[df1[f'{distance}+'] == False]



ctype = df1.groupby('primary_type')['id'].nunique().reset_index().sort_values('id', ascending = False).head(10)
dtype = df1.groupby('description')['id'].nunique().reset_index().sort_values('id', ascending = False).head(10)
ltype = df1.groupby('location_description')['id'].nunique().reset_index().sort_values('id', ascending = False).head(10)
ttype = df1.groupby('dt')['id'].nunique().reset_index().sort_values('dt')

#ax = sns.barplot(data = ctype, x = 'primary_type', y = 'id')

ax = sns.catplot(data = ttype, x = 'dt', y = 'id', kind = 'bar')