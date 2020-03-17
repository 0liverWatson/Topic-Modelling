# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 05:51:11 2020

@author: ProBook
"""

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet 
from nltk import pos_tag 
import re
import pandas as pd
import numpy as np
import EventDetection
from datetime import datetime

import DiscruptiveScore as ds
import dtm




lemmatizer = WordNetLemmatizer()
RealTimeTweets = pd.DataFrame(columns = ['Time','Text', 'Hashtages','Coordinates','City','Person_Name'])


# =============================================================================
# TO get POS of the word
# =============================================================================
def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)  

def datetime_func(date_str):
    return datetime.strptime(date_str, '%H:%M:%S')


class Tweet():
    def __init__(self):
        
        print("First Tweet Received...")
        self.count = 0
        self.flag = False
        self.flag1 = 0
        self.Time = 0
        self.Window_5_min = EventDetection.EventDetectionClass(10)
        self.Window_10_min = EventDetection.EventDetectionClass(20)
        self.Window_1_hour = EventDetection.EventDetectionClass(50)
        
    
    def Tweet_Collection(self, tweet):
        Match = datetime_func(re.search(r'(\d+:\d+:\d+)', tweet['created_at']).group(1))
        if(self.flag == False):
            self.Time =  Match
            self.flag = True
        print((Match-self.Time).total_seconds())
        
        if((Match-self.Time).total_seconds()>300):
            self.Window_10_min.Append_Data(RealTimeTweets)
            self.Window_1_hour.Append_Data(RealTimeTweets)
            self.Window_5_min.Append_Data(RealTimeTweets)
            
            
            if(self.Window_1_hour.Count == 12):
                RealTimeTweets.drop(RealTimeTweets.index, inplace=True)
                self.count = 0
                self.Window_1_hour.set_flag()
                
                if(len(self.Window_1_hour.DataFrame)>9999):
                    Th = (len(self.Window_1_hour.DataFrame)/100)*0.6
                    self.Window_1_hour.Event_Extraction(self.Window_1_hour.DataFrame,Th)
                else:
                    self.Window_1_hour.Event_Extraction(self.Window_1_hour.DataFrame,self.Window_1_hour.MinThreshold)
                self.Window_1_hour.Count = 0
                
                if(len(self.Window_10_min.DataFrame)>2000):
                    Th = (len(self.Window_10_min.DataFrame)/100)*1
                    self.Window_10_min.Event_Extraction(self.Window_10_min.DataFrame,Th)
                else:
                    self.Window_10_min.Event_Extraction(self.Window_10_min.DataFrame,self.Window_10_min.MinThreshold)
                self.Window_10_min.Count = 0   
                    
                if(len(self.Window_5_min.DataFrame)>1000):
                    Th = (len(self.Window_5_min.DataFrame)/100)*1
                    self.Window_5_min.Event_Extraction(self.Window_5_min.DataFrame,Th)
                else:
                    self.Window_5_min.Event_Extraction(self.Window_5_min.DataFrame,self.Window_5_min.MinThreshold)
                    self.Window_5_min.DataFrame.drop(self.Window_5_min.DataFrame.index, inplace = True)
                self.flag = False
                
                self.flag1 = 1
                
                
            
            elif(self.Window_10_min.Count == 2):
                RealTimeTweets.drop(RealTimeTweets.index, inplace=True)
                self.count = 0
                self.Window_10_min.set_flag()
                
                if(len(self.Window_10_min.DataFrame)>2000):
                    Th = (len(self.Window_10_min.DataFrame)/100)*1
                    self.Window_10_min.Event_Extraction(self.Window_10_min.DataFrame,Th)
                else:
                    self.Window_10_min.Event_Extraction(self.Window_10_min.DataFrame,self.Window_10_min.MinThreshold)
                self.Window_10_min.Count = 0 
                    
                if(len(self.Window_5_min.DataFrame)>1000):
                    Th = (len(self.Window_5_min.DataFrame)/100)*1
                    self.Window_5_min.Event_Extraction(self.Window_5_min.DataFrame,Th)
                else:
                    self.Window_5_min.Event_Extraction(self.Window_5_min.DataFrame,self.Window_5_min.MinThreshold) 
                 
                self.flag = False
                self.flag1 = 2
               
                
            else:
                RealTimeTweets.drop(RealTimeTweets.index, inplace=True)
                
                self.count = 0
                self.Window_5_min.set_flag()
                if(len(self.Window_5_min.DataFrame)>1000):
                    Th = (len(self.Window_5_min.DataFrame)/100)*1
                    self.Window_5_min.Event_Extraction(self.Window_5_min.DataFrame,Th)
                else:
                    self.Window_5_min.Event_Extraction(self.Window_5_min.DataFrame,self.Window_5_min.MinThreshold)
                
                self.flag = False
                self.flag1 = 3
                
# =============================================================================
#         All the FUnctionality comes after this for integration
# =============================================================================

            # print("####################")
            # print("####################")
            # print("####################")
            # print("####################")
            # print()
            # print()

            # print(len(self.Window_5_min.List_Of_Events))

            # print()
            # print()


            # print("####################")
            # print("####################")
            # print("####################")
            # print("####################")
            
            disruptive_events_5 = ds.get_disruptive_score(self.Window_5_min.List_Of_Events, 5)

            dtm5 = dtm.TopicModelling(disruptive_events_5, 5)
            dtm5.process_window()

            if(self.Window_10_min.Active):
                disruptive_events_10 = ds.get_disruptive_score(self.Window_10_min.List_Of_Events, 10)
                dtm10 = dtm.TopicModelling(disruptive_events_10, 10)
                dtm10.process_window()
                # for i in range():
                #     func disruption(self.Window_10_min.List_Of_Events[i][1])
                #     pirn()name , score

            if(self.Window_1_hour.Active):
                disruptive_events_60 = ds.get_disruptive_score(self.Window_1_hour.List_Of_Events, 60)
                dtm60 = dtm.TopicModelling(disruptive_events_60, 60)
                dtm60.process_window()
        
        
        
        
# =============================================================================
#       This is to empty dataframe and list of events after the visualization has been produced  
# =============================================================================
        if(self.flag1 == 1):
            self.Window_10_min.Empty_DataFrame_Events()
            self.Window_5_min.Empty_DataFrame_Events()
            self.Window_1_hour.Empty_DataFrame_Events()
        elif(self.flag1 == 2):
            self.Window_10_min.Empty_DataFrame_Events()
            self.Window_5_min.Empty_DataFrame_Events()
        elif(self.flag1 == 3):
            self.Window_5_min.Empty_DataFrame_Events()
        #The code below is to get data from twitter
        try:
            text = tweet['text']  #Filtering text and hashtags from the tweet
            text2= []
            
            for hashtag in tweet['entities']['hashtags']:
                text2.append(hashtag['text'])
                
            if("RT @" not in text):
                text = re.sub(r"(?:\#|RT |\@|https?\://)\S+", "", text)  #removing URLs, mentions and hashtags from the tweets 
                text = text.encode('ascii', errors = 'ignore')
                text = text.decode()
                #starttime = time.time()
                text = ' '.join([lemmatizer.lemmatize(word,get_wordnet_pos(word)) for word in text.split()])
                #print("time take",time.time()-starttime)
                #text = ' '.join([word for word in ])
         
                
                #print(type(tweet['place']['bounding_box']['coordinates'][0]))
                if( tweet['place'] != None):
                    corrdinates = tweet['place']['bounding_box']['coordinates'][0]
                    corrdinates = corrdinates[0]
                    
                    
                    RealTimeTweets.loc[self.count] = [tweet['created_at'],text,text2,corrdinates,tweet['place']['name'],tweet['user']['screen_name']]  #storing the data in the dataframe
                    
                #Dummy.loc[self.count] = [match.group(1),text,text2]
                    self.count +=1
            
                    print(self.count)
            else:
                #print(text)
                print("Retweet ai hai@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2")
               
                #starttime = time.time()
                      
        except KeyError:
            pass
     
