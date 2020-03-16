# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 01:07:16 2020

@author: ProBook
"""

import pandas as pd
import numpy as np
import en_core_web_sm
import time
import math
import ast

nlp = en_core_web_sm.load()

class EventDetectionClass():
    List_Of_Events = []
    Active = False
    Last_Update = ''
    Count = 0
    DataFrame = pd.DataFrame(columns = ['Time','Text', 'Hashtages','Coordinates','City','Person_Name'])
    
    def __init__(self,TH):
        self.List_Of_Events = []
        self.Active = False
        self.Last_Update = ''
        self.DataFrame = pd.DataFrame(columns = ['Time','Text', 'Hashtages','Coordinates','City','Person_Name'])
        self.Count = 0
        self.MinThreshold = TH
        
        
    def Append_Data(self,Data):
        self.DataFrame = pd.concat([self.DataFrame,Data],ignore_index=True)
        self.Count +=1
       
        
    def set_flag(self):
            self.Active = True 

                          
    def Event_Extraction(self,DF,Threshold):
    
        DF.dropna(axis=0, inplace = True) 
        print(DF)
        DF.to_csv("Rohma.csv")
        st = time.time()
        DF['Entities'] = DF['Text'].apply(lambda x: spacy_entity(x))
        print(time.time()-st)
        
        DF1 = DF.copy()
        
        DF.dropna(axis=0, inplace = True)
        ##this is too delete empty text tweets
        DF['Text'] = DF['Text'].apply(lambda x: x.lower())
        
    
    # =============================================================================
    # 
    # Creation of Interted index of Entities
    # 
    # =============================================================================
        DF['indexes'] = DF.index
        DF['index']= list(range(0,len(DF)))
        DF.set_index('index',inplace =True)
        All_Entities = []       
        Entities_Inverted_Index = []
        Number_of_Entities = 0
        Linear_Sum_Entities = 0
        Standard_Deviation_Entities = 0 
        Square_Sum_Entities = 0
        Mean_Entities = 0
        count = 1
        
        for index in DF.index:
            Tweet_Entities = (DF.iloc[index]['Entities'])
            Tweet_Entities = [i[0] for i in Tweet_Entities]
            Tweet_Entities = list(set(Tweet_Entities))
            for Entity in Tweet_Entities:
                if(Entity not in All_Entities):
                    #Entity = Entity + "_Entity"
                    All_Entities.append(Entity)
                    Entities_Inverted_Index.append([DF.iloc[index]['indexes']])
                    count +=1
                else:
                    Entity_index = All_Entities.index(Entity)
                    Entities_Inverted_Index[Entity_index].append(DF.iloc[index]['indexes'])
    # =============================================================================
    #    Calculation of Bursty Score for Entities                 
    # =============================================================================
                    
        Number_of_Entities = len(All_Entities)
        for i in range(0,len(Entities_Inverted_Index)):
            Linear_Sum_Entities = Linear_Sum_Entities + len(Entities_Inverted_Index[i])
            Square_Sum_Entities = Square_Sum_Entities + pow(len(Entities_Inverted_Index[i]),2)
        Mean_Entities = Linear_Sum_Entities / Number_of_Entities
        Standard_Deviation_Entities = math.sqrt((Square_Sum_Entities/Number_of_Entities)-pow((Linear_Sum_Entities/Number_of_Entities),2))
        Bursty_Score_Entities = Mean_Entities + (3 * Standard_Deviation_Entities)
        
    # =============================================================================
    # CLuster Creation of Entities
    # =============================================================================
        
        Window_5_Min_Entities = []
        for i in range(0,len(Entities_Inverted_Index)):
            if(len(Entities_Inverted_Index[i])> Bursty_Score_Entities):
                print(All_Entities[i], len(Entities_Inverted_Index[i]))
                Sub_DataFrame = DF[DF['indexes'].isin(Entities_Inverted_Index[i])]
                Window_5_Min_Entities.append([All_Entities[i],Sub_DataFrame])
                
    # =============================================================================
    # Merging Entity Cluster
    # =============================================================================
        list_of_Entity_Nodes = []
        for i in range (0,len(Window_5_Min_Entities)):
            list_of_Entity_Nodes.append(Node(Window_5_Min_Entities[i][0],i)) 
      
        for i in range (0,len(Window_5_Min_Entities)):
            I_Entity = Window_5_Min_Entities[i][0]
            for j in range (0,len(Window_5_Min_Entities)):
                if(i>=j):
                    continue
                else:
                    Entity_Counter = 0
                    Check_Node = False
                    for Tweet_Entities in Window_5_Min_Entities[j][1]['Entities']:
                        Tweet_Entities = [x[0] for x in Tweet_Entities]
                        if(I_Entity in Tweet_Entities):
                            Entity_Counter+=1
                    Ith_DataFrame_length = len(Window_5_Min_Entities[i][1])
                    Jth_DataFrame_length = len(Window_5_Min_Entities[j][1])
                    if(Ith_DataFrame_length<Jth_DataFrame_length):
                        #print(Ith_DataFrame_length / 3,"    ", Jth_DataFrame_length / 3)
                        if(Entity_Counter > Ith_DataFrame_length / 10):
                            printval = list_of_Entity_Nodes[i]
                            while printval.nextval is not None:
                                if(printval.index == j):
                                    Check_Node = True
                                    break
                                print("1",printval.dataval)
                                printval = printval.nextval
                            index  = printval.index
                            if(index != j and Check_Node == False):
                                list_of_Entity_Nodes[index].nextval = list_of_Entity_Nodes[j]
                            list_of_Entity_Nodes[j].preval = list_of_Entity_Nodes[index]
                            
                    else:
                        if(Entity_Counter > Jth_DataFrame_length / 10):
                            printval = list_of_Entity_Nodes[i]
                            while printval.nextval is not None:
                                if(printval.index == j):
                                    Check_Node = True
                                    break
                                print("1",printval.dataval)
                                printval = printval.nextval
                            index  = printval.index
                            if(index != j and Check_Node == False):
                                list_of_Entity_Nodes[index].nextval = list_of_Entity_Nodes[j]
                            list_of_Entity_Nodes[j].preval = list_of_Entity_Nodes[index]
                           
    # =============================================================================
    #     Traversing Graph                    
    # =============================================================================
        New_Window_5_Min_Entities = []                
        for i in range (0,len(list_of_Entity_Nodes)):
            Name = Window_5_Min_Entities[i][0]
            length = len(Window_5_Min_Entities[i][1])
            ConCat_DataFrame = pd.DataFrame(columns = ['Time', 'Text', 'Hashtages', 'Coordinates', 'City', 'Entities','indexes'])
            printval = list_of_Entity_Nodes[i]
            check = False
            check1 = False
            Entities_list = []
            if(printval.preval == None):
                check = True
                print("Starting node is ",printval.dataval)
            while printval is not None:
                if(check):
                    ConCat_DataFrame = pd.concat([ConCat_DataFrame,Window_5_Min_Entities[printval.index][1]],ignore_index=True)
                    ConCat_DataFrame.drop_duplicates(subset ="indexes", keep = False, inplace = True)
                    
                    Entities_list.append(printval.dataval)
                    check1 = True 
                    if(length<len(Window_5_Min_Entities[printval.index][1])):
                        length = len(Window_5_Min_Entities[printval.index][1])
                        Name = Window_5_Min_Entities[printval.index][0]
                printval = printval.nextval
            if(check1):
                New_Window_5_Min_Entities.append([Entities_list,ConCat_DataFrame,Name])
            
            
        
        '''
        for i in range(0,len(New_Window_5_Min_Entities)):
            Name = str(New_Window_5_Min_Entities[i][0]) + '.csv'
            New_Window_5_Min_Entities[i][1].to_csv(Name,index = False)
        '''
           
            
    # =============================================================================
    #         Hashtags detection
    #         
    # =============================================================================
        
        Linear_Sum_Hashtags = 0
        Standard_Deviation_Hashtags = 0 
        Square_Sum_Hashtags = 0
        Mean_Hashtags = 0
        Dummy = DF1.copy()
        Dummy1 = Dummy[Dummy['Hashtages'] == '[]'] #removing tweets without any hashtag
        Dummy.drop(index = Dummy1.index, inplace = True, axis = 0)
        
        Dummy1["Entities"].isna().sum()
        indexes  = list(range(0,len(Dummy)))
        Dummy['index'] = indexes  #creating a dummy index
        Dummy['indexes'] = Dummy.index
        Dummy.set_index('index', inplace = True)
        
        All_Hastags = []
        Hashtags_Inverted_Index = []
        
        for index in Dummy.index:
            print(Dummy['Hashtages'])
            print(index,"  ",ast.literal_eval(Dummy.iloc[index]['Hashtages']))
            Hashtag_list = ast.literal_eval(Dummy.iloc[index]['Hashtages'])
    
            for Hashtag in Hashtag_list:
                if(Hashtag not in All_Hastags):
                    #Hashtag1 = Hashtag + "_Hashtag"
                    All_Hastags.append(Hashtag)
                    Hashtags_Inverted_Index.append([Dummy.iloc[index]['indexes']])
                else:
                    Hashtag_index = All_Hastags.index(Hashtag)
                    Hashtags_Inverted_Index[Hashtag_index].append(Dummy.iloc[index]['indexes'])
                
    
        
        
        Number_of_Hashtags = len(All_Hastags)
        for i in range(0,len(Hashtags_Inverted_Index)):
            #print(All_Entities[i],len(Entities_Inverted_Index[i]))
            Linear_Sum_Hashtags = Linear_Sum_Hashtags + len(Hashtags_Inverted_Index[i])
            Square_Sum_Hashtags = Square_Sum_Hashtags + pow(len(Hashtags_Inverted_Index[i]),2)
        Mean_Hashtags = Linear_Sum_Hashtags / Number_of_Hashtags
        Standard_Deviation_Hashtags = math.sqrt((Square_Sum_Hashtags/Number_of_Hashtags)-pow((Linear_Sum_Hashtags/Number_of_Hashtags),2))
        Bursty_Score_Hashtags = Mean_Hashtags + (3 * Standard_Deviation_Hashtags) 
       
        
        Window_5_Min_hashtag = []
        for i in range(0,len(Hashtags_Inverted_Index)):
            if(len(Hashtags_Inverted_Index[i])> Bursty_Score_Hashtags):
                Sub_DataFrame = Dummy[Dummy['indexes'].isin(Hashtags_Inverted_Index[i])]
                Window_5_Min_hashtag.append([All_Hastags[i],Sub_DataFrame])
           
    # =============================================================================
    # Merging Hashtag clusters       
    # =============================================================================
       
        list_of_Hashtag_Nodes = []
        for i in range (0,len(Window_5_Min_hashtag)):
            print(Window_5_Min_hashtag[i][0])
            list_of_Hashtag_Nodes.append(Node(Window_5_Min_hashtag[i][0],i)) 
    
        
        
        for i in range (0,len(Window_5_Min_hashtag)):
            Ith_length = len(Window_5_Min_hashtag[i][1])
            for j in range (0,len(Window_5_Min_hashtag)):
                if(i>=j):
                    continue
                else:
                    Check_Node = False
                    if(j>len(Window_5_Min_hashtag)):
                        continue
                    Jth_length = len(Window_5_Min_hashtag[j][1])
                    Intersection =  len(list(set(Window_5_Min_hashtag[i][1]['indexes']).intersection(set(Window_5_Min_hashtag[j][1]['indexes']))))
                    if(Ith_length<Jth_length):
                        if(Intersection>=len(Window_5_Min_hashtag[i][1])/10):
                            print("This is the Ith Hashtag1...",i,Window_5_Min_hashtag[i][0], "This is the Jth Entity",j, Window_5_Min_hashtag[j][0])
                            printval = list_of_Hashtag_Nodes[i]
                            while printval.nextval is not None:
                                if(printval.index == j):
                                    Check_Node = True
                                    break
                                print("1",printval.dataval)
                                printval = printval.nextval
                            index  = printval.index
                            if(index != j and Check_Node == False):
                                list_of_Hashtag_Nodes[index].nextval = list_of_Hashtag_Nodes[j]
                            list_of_Hashtag_Nodes[j].preval = list_of_Hashtag_Nodes[index]
                          
                    else:
                         if(Intersection>=len(Window_5_Min_hashtag[j][1])/10):
                            print("This is the Ith Hashtag3...",i,Window_5_Min_hashtag[i][0], "This is the Jth Entity",j, Window_5_Min_hashtag[j][0])
                            printval = list_of_Hashtag_Nodes[i]
                            while printval.nextval is not None:
                                if(printval.index == j):
                                    Check_Node = True
                                    break
                                print("3",printval.dataval)
                                printval = printval.nextval
                            index  = printval.index
                            if(index != j and Check_Node == False):
                                list_of_Hashtag_Nodes[index].nextval = list_of_Hashtag_Nodes[j]
                            list_of_Hashtag_Nodes[j].preval = list_of_Hashtag_Nodes[index]
                            
    
    # =============================================================================
    # Traversing the graph
    # =============================================================================
        New_Window_5_Min_hashtag = []
        
        for i in range (0,len(Window_5_Min_hashtag)):
            Name =  Window_5_Min_hashtag[i][0]
            length = len(Window_5_Min_hashtag[i][1])
            ConCat_DataFrame = pd.DataFrame(columns = ['Time', 'Text', 'Hashtages', 'Coordinates', 'City', 'Entities','indexes'])
            printval = list_of_Hashtag_Nodes[i]
            check = False
            check1 = False
            Hashtags_list = []
            if(printval.preval == None):
                check = True
                
               
            while printval is not None:
                if(check):
                    ConCat_DataFrame = pd.concat([ConCat_DataFrame,Window_5_Min_hashtag[printval.index][1]],ignore_index=True)
                    ConCat_DataFrame.drop_duplicates(subset ="indexes", keep = False, inplace = True)
                    
                    Hashtags_list.append(printval.dataval)
                    check1 = True
                    if(length<len(Window_5_Min_hashtag[printval.index][1])):
                        length = len(Window_5_Min_hashtag[printval.index][1])
                        Name = Window_5_Min_hashtag[printval.index][0]
                printval = printval.nextval
            if(check1):
                New_Window_5_Min_hashtag.append([Hashtags_list,ConCat_DataFrame,Name])
         
    # =============================================================================
    #  Disjointing Tweets from Events           
    # =============================================================================
           
        
        Window_5_Min_All_Events = New_Window_5_Min_hashtag + New_Window_5_Min_Entities   
        count =0
     
        count1 = 0
        for i in range(0,len(Window_5_Min_All_Events)):
            for j in range(0,i):
                Intersection = list(set(Window_5_Min_All_Events[i][1]['indexes']).intersection(set(Window_5_Min_All_Events[j][1]['indexes'])))
                Number_Intersections = len(Intersection)
                if(Number_Intersections == 0):
                    print("Yes")
                    count +=1
                    continue
                count1 +=1
                Window_5_Min_All_Events[j][1] =  Window_5_Min_All_Events[j][1][~Window_5_Min_All_Events[j][1]['indexes'].isin(Intersection)]       
                   
       #All_Event_Window_5 = [x for x in Window_5_Min_All_Events if ((len(x[1])>Bursty_Score_Hashtags) and (len(x[1])>10))]
            self.List_Of_Events = [x for x in Window_5_Min_All_Events if len(x[1])>Threshold]
            
       
       
        
        for i in range (0,len(self.List_Of_Events)):     
            #All_Event_Window_5[i][1].sort_values(by = 'indexes', ascending=True, inplace = True)
            print(self.List_Of_Events[i][2],"   ",len(self.List_Of_Events[i][1]))
    

# =============================================================================
# Node Class 
# =============================================================================
class Node:
    def __init__(self, dataval=None, index = None):
        self.index = index
        self.dataval = dataval
        self.preval = None
        self.nextval = None    



# =============================================================================
# Entity Detection Library 
# =============================================================================
def spacy_entity(df):
    df1 = nlp(df)
    df2 = []
    for w in df1.ents:
        if(w.label_ == 'PERSON' or w.label_ == 'ORG' or w.label_ == 'GPE' or w.label_ == 'NORP'or w.label_ == 'FAC'or w.label_ == 'EVENT'):
            df2.append([w.text.lower(),w.label_])
    if(df2 == []):
        return np.nan
    else:
        return df2
    