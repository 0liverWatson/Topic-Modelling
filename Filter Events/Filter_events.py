import numpy as np
import pandas as pd
import csv
import argparse
from afinn import Afinn
import json


data = pd.read_csv('C:/Users\Rohan Das\Documents\Rohan_Docs\Study\Semester 3\Kmd_project\Data/new/coronavirus.csv',skipinitialspace=True, delimiter =',')
data1 = pd.read_csv('C:/Users\Rohan Das\Documents\Rohan_Docs\Study\Semester 3\Kmd_project\Data/new/Covid_19.csv',skipinitialspace=True, delimiter =',')
data2 = pd.read_csv('C:/Users\Rohan Das\Documents\Rohan_Docs\Study\Semester 3\Kmd_project\Data/new/tonight.csv',skipinitialspace=True, delimiter =',')
data3 = pd.read_csv('C:/Users\Rohan Das\Documents\Rohan_Docs\Study\Semester 3\Kmd_project\Data/new/friday.csv',skipinitialspace=True, delimiter =',')

all_data = [
    {'event_name':'coronavirus', 'data':data},
    {'event_name': 'Covid_19', 'data':data1},
    {'event_name': 'tonight', 'data':data2},
    {'event_name': 'friday', 'data':data3}]
# eventname = ['coronavirus', 'Covid_19', 'tonight', 'friday']
disruptive_event = []
disruptive_eventname =[]
data_file = []

final_list = []
for df in all_data:
    # print(all_data[i].dropna(subset=['Text']))
    df['data'] = df['data'].dropna(subset=['Text'])
    tweets = df['data']['Text']
    afinn = Afinn(emoticons=True)
    disruptive_score = 0.0
    negative_score = 0
    sentiment = []
    # print(len(t))
    for k in tweets:
        s = afinn.score(k)
        if s < 0:
            sentiment.append('negative')
            s =1
        elif s == 0:
            sentiment.append('neutral')
            s =0
        else:
            sentiment.append('positive')
            s =0
        negative_score = negative_score + s
    disruptive_score = negative_score/len(df['data'].index)

    if disruptive_score > 0.4:
        final_list.append(df)

s1 = json.dumps(final_list)
with open('C:/Users\Rohan Das\Documents\Rohan_Docs\Study\Semester 3\Kmd_project\Data\File.json','w') as json_file:
    json.dump(s1, json_file)