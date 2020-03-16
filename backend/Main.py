# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 18:49:52 2020

@author: ProBook
"""
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import TwitterCred
import json
import TweetCollection

class StdOutListener(StreamListener):
  
    def __init__(self):
    # body of the constructor

        self.Twee = TweetCollection.Tweet()

    #def on_status(self, status):
    #    print(status.text)

    def on_data(self, data):
        jsonData=json.loads(data)
        self.Twee.Tweet_Collection(jsonData)
        return True
        
    def on_error(self, status):
        print(status)
        
        
if __name__ == '__main__':
    listener = StdOutListener()
    auth = OAuthHandler(TwitterCred.CONSUMER_KEY, TwitterCred.CONSUMER_SECRET)
    auth.set_access_token(TwitterCred.ACCESS_TOKEN, TwitterCred.ACCESS_TOKEN_SECRET)
    stream = Stream(auth, listener, tweet_mode = 'extended')
    #words = ['toiletpaperpanic','coronvirusuk','InternationalWomenDay2020','Eternal Atake','Amber Rudd','billyconnolly','Perrie','UFC248','Yoel','Nissan'] 
    #stream.filter(languages=["en"],locations = [-7.57216793459, 49.959999905, 1.68153079591, 58.6350001085])
    stream.filter(languages=["en"],locations = [-7.57216793459, 49.959999905, 1.68153079591, 58.6350001085])
    