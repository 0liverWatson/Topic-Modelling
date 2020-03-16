import numpy as np
import pandas as pd
import csv
import argparse
from afinn import Afinn
import json
import config
import time

# class DisruptiveScore:

#     def __init__(self):

path = config.get('JSON', 'events')

def get_disruptive_score(data, window):

    threshold = config.get('DiscruptiveScoreThresholds',str(window))

    all_data = convert_window_to_json(data)

    final_list = []
    for event in all_data:
        df = pd.read_json(event['data'])
        # print(all_data[i].dropna(subset=['Text']))
        df = df.dropna(subset=['Text'])
        tweets = df['Text']
        afinn = Afinn(emoticons=True)
        disruptive_score = 0.0
        negative_score = 0

        for k in tweets:
            s = afinn.score(k)
            if s < 0:
                s =1
            elif s == 0:
                s =0
            else:
                s =0
            negative_score = negative_score + s
        disruptive_score = negative_score/len(df.index)

        if disruptive_score > threshold:
            final_list.append(df)

        s1 = json.dumps(final_list)
        with open(path+str(window)+'_'+str(time.time())+'.json','w') as json_file:
            json.dump(s1, json_file)

    return final_list


def convert_window_to_json(df):
    final_list = []
    for event in df:
        final_list.append({
            'event_name': event[2], 
            'data': event[1], 
        })
    
    return final_list
    
