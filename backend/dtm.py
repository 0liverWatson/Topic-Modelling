import pandas as pd
import gensim.parsing.preprocessing as parser
import numpy as np
from pprint import pprint

from gensim.models import ldaseqmodel,ldamodel, CoherenceModel
from gensim.corpora import Dictionary, bleicorpus
from gensim.matutils import hellinger
from gensim import corpora
from gensim.models.wrappers.dtmmodel import DtmModel

import time
import json


import gensim
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
lemmatizer = WordNetLemmatizer()
tokenizer = RegexpTokenizer(r'\w+')
nltk.download('wordnet')

import config

path = config.get('JSON', 'topics')
dtm_path = config.get('DTM', 'path')   
num_topics = config.get('DTM', 'topics')
top_n = config.get('DTM', 'words')

class event_reader:
    def __init__(self, data, mins):   # change mins to window size       
        
        data['Time'] = pd.to_datetime(data['Time'])
        data['pText'] = self.preprocess(data['Text'])        
        self.data = data.sort_values('Time')
        
        self.start_time = data.Time.min()
        self.end_time = data.Time.max()
        self.timeslice = mins   # calculate timeslice based on window size

        self.flat_list, self.time_slices = self.split_to_timeslices()

        self.model, self.corpus, self.dict =  self.initialize_model()
        
    def get_start_end_time(self):        
        return (self.start_time, self.end_time)    
    

    def preprocess(self, data):
        
        data = [s.lower() for s in data]

        data = [parser.remove_stopwords(s) for s in data]
        data = [parser.strip_numeric(s) for s in data]
        data = [tokenizer.tokenize(s) for s in data]

        data = [[token for token in doc if len(token) > 1] for doc in data]
        data = [[lemmatizer.lemmatize(word) for word in doc] for doc in data]

        return data
    
    def split_to_timeslices(self):
        words = []
        time_slices = []

        st = self.start_time
        et = st + pd.Timedelta(minutes=self.timeslice)

        df = self.data

        while st < self.end_time:
            et += pd.Timedelta(minutes=self.timeslice)


            dff = df.loc[(df['Time'] >= st) & (df['Time'] < et)]

            words.append(dff['pText'].to_numpy())

            time_slices.append(len(dff.index))

            st = et
            
        flat_list = []
        for sublist in words:
            for item in sublist:
                flat_list.append(item)
            
        return flat_list,time_slices

    def initialize_model(self):

        mydict = corpora.Dictionary()
        mycorpus = [mydict.doc2bow(doc, allow_update=True) for doc in self.flat_list]

        start = time.time()
        model = DtmModel(dtm_path, mycorpus, self.time_slices, num_topics=num_topics, id2word=mydict, 
                        initialize_lda=True, top_chain_var=0.05, lda_sequence_min_iter=15, lda_sequence_max_iter=50)
        print(time.time()-start)

        return model, mycorpus, mydict
        
    def get_DTM_for_time_slices(self):
        final_list = []
        
        
        for i in range(len(self.time_slices)):
            ts = []
            for j in range(num_topics):
              ts.append(self.model.show_topic(j,i,top_n))  
            final_list.append(ts)
        
        return final_list

    def get_topic_stengths(self):
        final_list = []


        vis = self.model.dtm_vis(self.corpus, 0)

        dtp = np.asarray(vis[0])
        doc_len = np.asarray(vis[2])
        doc_len = doc_len / max(doc_len)

        start = 0
        end = 0
        s = 0

        for sl  in self.time_slices:
            end += sl
            dtp_sub = dtp[start:end]
            doc_len_sub = doc_len[start:end]
            s = np.multiply(dtp_sub.transpose(), doc_len_sub)
            s = np.sum(s, axis=1)
            final_list.append(s.tolist())
            start += sl

        return final_list

class TopicModelling:
    def __init__(self, data, win):
        self.data = data
        self.window = win

    def process_window(self):
        final_list = []

        for event in self.data:

            sr = event_reader(event['data'], self.window)

            topics = sr.get_DTM_for_time_slices()
            
            strengths = sr.get_topic_stengths()

            obj = {
                'event_name' : event['event_name'],
                'topics' : topics,
                'strengths' : strengths
            }

            final_list.append(obj)

        s1 = json.dumps(final_list)
        with open(path+str(self.window)+'_'+str(time.time())+'.json','w') as json_file:
            json.dump(s1, json_file)

        return final_list



            
            