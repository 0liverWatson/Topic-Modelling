import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import random
import glob
import os
from app import app
import json
str11 = "https://raw.githubusercontent.com/SubhshreeMangaraj/Topic-Modelling/master/DS/";

#Extract the events for all the windows
#--------------------------------------

# #5 minutes window
# -----------------
list_of_files_5 = glob.glob('data/topics/5_*.json')
latest_file_5 = max(list_of_files_5, key=os.path.getctime)

with open(latest_file_5) as json_file:
    json_str = json.load(json_file)
data_5 = json.loads(json_str)

# #10 minutes window
# -----------------
# list_of_files_10 = glob.glob('data/topics/10_*.json')
# latest_file_10 = max(list_of_files_10, key=os.path.getctime)
#
# with open(latest_file_10) as json_file:
#     json_str = json.load(json_file)
# data_10 = json.loads(json_str)

# #5 minutes window
# -----------------
# list_of_files_60 = glob.glob('data/topics/60_*.json')
# latest_file_60 = max(list_of_files_60, key=os.path.getctime)
#
# with open(latest_file_60) as json_file:
#     json_str = json.load(json_file)
# data_60 = json.loads(json_str)
# event_list5 = pd.read_csv("https://raw.githubusercontent.com/SubhshreeMangaraj/Topic-Modelling/master/DS/5min/eventlist_5min.csv")
# el5 = event_list5.Events.unique()
# el5 = el5.tolist()
#

traces =[]

layout_page1 = html.Div([
                    html.H2('Evolution of top bursty topics over the 5 Minutes window'),
                    html.Button('Click to see the list of events',id="but1"),
                    html.H4( id = 'head1'),
                    dcc.Dropdown(
                        id='opt-dropdown_5min'
                        # options=[{'label': opt, 'value': opt} for opt in el5]
                    ),
                    dcc.Graph(id='5min1_event'),
                    html.H4('List of Bursting Topics ( Select one to view the keyword evolution ) '),
                    dcc.Dropdown(
                        id='opt-dropdown_5min_topics'
                    ),
                    dcc.Graph(id='5min1_topic')
])

# layout_page2 = html.Div([
#                     html.H2('Evolution of top bursty topics over the 10 Minutes window'),
#                     html.H4('List of Bursting Events ( Select one to view the topic evolution ) '),
#                     dcc.Dropdown(
#                           id='opt-dropdown_10min',
#                           options=[{'label': opt, 'value': opt} for opt in el10]
#                       ),
#                       dcc.Graph(id='10min1_event'),
#                       html.H4('List of Bursting Topics ( Select one to view the keyword evolution ) '),
#                       dcc.Dropdown(
#                           id='opt-dropdown_10min_topics'
#                       ),
#                       dcc.Graph(id='10min1_topic')
# ])
#
# layout_page3 = html.Div([
#                     html.H2('Evolution of top bursty topics over the 1 Hour window'),
#                     html.H4('List of Bursting Events ( Select one to view the topic evolution ) '),
#                     dcc.Dropdown(
#                           id='opt-dropdown_1hr',
#                           options=[{'label': opt, 'value': opt} for opt in el1]
#                       ),
#                       dcc.Graph(id='1hr1_event'),
#                       html.H4('List of Bursting Topics ( Select one to view the keyword evolution) '),
#                       dcc.Dropdown(
#                           id='opt-dropdown_1hr_topics'
#                       ),
#                       dcc.Graph(id='1hr1_topic')
# ])

# For 5 minutes window
#----------------------------------------------------------------------------------------
#Callback for Fig 1 - Evolution of topics in an event
#----------------------------------------------------

@app.callback(
   Output('head1', 'value'),
   [Input('but1', 'n_clicks')]
)

def but1_click(n):
    if n:
        return 'List of Bursting Events ( Select one to view the topic evolution )'



@app.callback(
   Output('opt-dropdown_5min', 'options'),
   [Input('but1', 'n_clicks')]
)

def but1_click1(n):
    if n:
        list_of_files_5 = glob.glob('data/topics/5_*.json')
        latest_file_5 = max(list_of_files_5, key=os.path.getctime)

        with open(latest_file_5) as json_file:
            json_str = json.load(json_file)
        data_5 = json.loads(json_str)
        el5 = []
        for m in data_5:
            el5.append(m['event_name'])
        return [{'label': opt, 'value': opt} for opt in el5]


@app.callback(
   Output('5min1_event', 'figure'),
   [Input('opt-dropdown_5min', 'value')]
)
def update_fig5min(selectedevent):

    el5=[]
    strength5=[]
    list_of_files_5 = glob.glob('data/topics/5_*.json')
    latest_file_5 = max(list_of_files_5, key=os.path.getctime)

    with open(latest_file_5) as json_file:
        json_str = json.load(json_file)
    data_5 = json.loads(json_str)
    for i in data_5:
        if (i['event_name'] == selectedevent):
            el5.append(i['event_name'])
            strength5.append(i['strengths'])
    df = pd.DataFrame([el5, strength5]).T

    for i in range(len(df)):
        df1 = df.iloc[i, 1]
        dd = pd.DataFrame(df1).T
        traces = [];
        number_of_colors = 20
        for (columnName, columnData) in dd.iteritems():
            traces.append(
                go.Scatter(
                    x=[0.5, 1, 1.5, 2, 2.5],
                    y=columnData.values,
                    type='scatter',
                    mode='lines',
                    line=dict(width=0.5),
                    stackgroup='one',
                    fill='tonexty',
                    name=columnName

                ))
        return {
            'data': traces,
            'layout': {
                'title': 'Visualization of Topic Evolution'
            },
        }

#Callback for dropdown
#---------------------
@app.callback(
    dash.dependencies.Output("opt-dropdown_5min_topics", "options"),
    [dash.dependencies.Input('opt-dropdown_5min', 'value')],
)
def update_options(selectedevent):
    el5=[]
    topic5=[]

    list_of_files_5 = glob.glob('data/topics/5_*.json')
    latest_file_5 = max(list_of_files_5, key=os.path.getctime)

    with open(latest_file_5) as json_file:
        json_str = json.load(json_file)
    data_5 = json.loads(json_str)

    for i in data_5:
        if (i['event_name'] == selectedevent):
            el5.append(i['event_name'])
            topic5.append(i['topics'])
    df = pd.DataFrame([el5, topic5]).T

    num_of_topics = (len(df[1][0]))

    return [{'label': opt, 'value': opt} for opt in range(0,num_of_topics)]

#Callback for fig 2 - Evolution of keywords in topics
#----------------------------------------------------
@app.callback(
   Output('5min1_topic', 'figure'),
   [Input('opt-dropdown_5min_topics', 'value'),
    Input('opt-dropdown_5min', 'value')]
)
def update_fig5min_topics(selectedtopic,selectedevent):
    el5 = []
    topic5 = []
    traces = [];

    list_of_files_5 = glob.glob('data/topics/5_*.json')
    latest_file_5 = max(list_of_files_5, key=os.path.getctime)

    with open(latest_file_5) as json_file:
        json_str = json.load(json_file)
    data_5 = json.loads(json_str)

    for i in data_5:
        if (i['event_name'] == selectedevent):
            el5.append(i['event_name'])
            topic5.append(i['topics'])
    df = pd.DataFrame([el5, topic5]).T

    tempdf = df[1][0]
    df2 = tempdf[2]
    for k in range(len(df2)):
        # print(df2[k])
        df3 = pd.DataFrame(df2[k])
        df3.columns = ['key_strength', 'keyword']
        final_df3 = df3.sort_values(by=['keyword'])
        traces.append(
            go.Bar(
                x=[0.5, 1, 1.5, 2, 2.5],
                y=final_df3['key_strength'],
                name=final_df3['keyword'],
                opacity=0.5
            ))
    return {
        'data': traces,
        'layout': {
            'title': 'Visualization of Keyword Evolution',
            'barmode': 'stack'
        },
    }
#--------------------------------------------------------------------------------------------------




# # For 10 minutes window
# #----------------------------------------------------------------------------------------
# #Callback for Fig 1 - Evolution of topics in an event
# #----------------------------------------------------
# @app.callback(
#    Output('10min1_event', 'figure'),
#    [Input('opt-dropdown_10min', 'value')]
# )
# def update_fig10min(selectedevent):
#
#     #val = str + "/10min/events/window_10min_" +selectedevent + ".csv";
#
#     myTuple = (str11, "/10min/events/window_10min_", selectedevent, ".csv")
#     x = "".join(myTuple)
#     val = x
#
#     topic_list_10min1 = pd.read_csv(val);
#     dd = topic_list_10min1.drop(columns=['year']);
#     traces = [];
#     number_of_colors = 20
#     for (columnName, columnData) in dd.iteritems():
#         traces.append(
#             go.Scatter(
#                 x=[0.5, 1, 1.5, 2, 2.5, 3,3.5,4,4.5,5],
#                 y=columnData.values,
#                 type='scatter',
#                 mode='lines',
#                 line=dict(width=0.5),
#                 stackgroup='one',
#                 fill='tonexty',
#                 name=columnName
#
#             ))
#     return {
#         'data': traces,
#         'layout': {
#             'title': 'Visualization of Topic Evolution'
#         },
#     }
#
# #Callback for dropdown
# #---------------------
# @app.callback(
#     dash.dependencies.Output("opt-dropdown_10min_topics", "options"),
#     [dash.dependencies.Input('opt-dropdown_10min', 'value')],
# )
# def update_options(selectedevent):
#     #val = str + "/10min/events/window_10min_" + selected_event + ".csv";
#
#     myTuple = (str11, "/10min/events/window_10min_", selectedevent, ".csv")
#     x = "".join(myTuple)
#     val = x
#
#     dd = pd.read_csv(val);
#     dd = dd.drop(columns=['year']);
#     top10 = dd;
#     top10 = list(top10.columns)
#     return [{'label': opt, 'value': opt} for opt in top10]
#
# #Callback for fig 2 - Evolution of keywords in topics
# #----------------------------------------------------
# @app.callback(
#    Output('10min1_topic', 'figure'),
#    [Input('opt-dropdown_10min_topics', 'value'),
#     Input('opt-dropdown_10min', 'value')]
# )
# def update_fig10min_topics(selectedtopic,selectedevent):
#
#     #val = str + "/10min/topics/window_10min_" + selectedevent + "_" + selectedtopic + ".csv";
#
#     myTuple = (str11, "/10min/topics/window_10min_", selectedevent, "_", selectedtopic, ".csv")
#     x = "".join(myTuple)
#     val = x
#
#     topic_list_10min1 = pd.read_csv(val);
#     dd = topic_list_10min1.drop(columns=['year']);
#     traces = [];
#     number_of_colors = 20
#     for (columnName, columnData) in dd.iteritems():
#         traces.append(
#             go.Bar(
#                 x=[0.5, 1, 1.5, 2, 2.5, 3,3.5,4,4.5,5],
#                 y=columnData.values,
#                 name=columnName,
#                 opacity=0.5
#             ))
#     return {
#         'data': traces,
#         'layout': {
#             'title': 'Visualization of Keyword Evolution',
#             'barmode': 'stack'
#         },
#     }
# #--------------------------------------------------------------------------------------------------
#
#
#
# # For 1 hour window
# #----------------------------------------------------------------------------------------
# #Callback for Fig 1 - Evolution of topics in an event
# #----------------------------------------------------
# @app.callback(
#    Output('1hr1_event', 'figure'),
#    [Input('opt-dropdown_1hr', 'value')]
# )
# def update_fig1hr(selectedevent):
#
#     #val = str + "/1hr/events/window_1hr_" +selectedevent + ".csv";
#
#     myTuple = (str11, "/1hr/events/window_1hr_", selectedevent, ".csv")
#     x = "".join(myTuple)
#     val = x
#
#     topic_list_1hr1 = pd.read_csv(val);
#     dd = topic_list_1hr1.drop(columns=['year']);
#     traces = [];
#     number_of_colors = 20
#     for (columnName, columnData) in dd.iteritems():
#         traces.append(
#             go.Scatter(
#                 x=[0.5, 1, 1.5, 2, 2.5, 3],
#                 y=columnData.values,
#                 type='scatter',
#                 mode='lines',
#                 line=dict(width=0.5),
#                 stackgroup='one',
#                 fill='tonexty',
#                 name=columnName
#
#             ))
#     return {
#         'data': traces,
#         'layout': {
#             'title': 'Visualization of Topic Evolution'
#         },
#     }
#
# #Callback for dropdown
# #---------------------
# @app.callback(
#     dash.dependencies.Output("opt-dropdown_1hr_topics", "options"),
#     [dash.dependencies.Input('opt-dropdown_1hr', 'value')],
# )
# def update_options(selectedevent):
#     #val = str + "/1hr/events/window_1hr_" + selected_event + ".csv";
#
#     myTuple = (str11, "/1hr/events/window_1hr_", selectedevent, ".csv")
#     x = "".join(myTuple)
#     val = x
#
#     dd = pd.read_csv(val);
#     dd = dd.drop(columns=['year']);
#     top1 = dd;
#     top1 = list(top1.columns)
#     return [{'label': opt, 'value': opt} for opt in top1]
#
# #Callback for fig 2 - Evolution of keywords in topics
# #----------------------------------------------------
# @app.callback(
#    Output('1hr1_topic', 'figure'),
#    [Input('opt-dropdown_1hr_topics', 'value'),
#     Input('opt-dropdown_1hr', 'value')]
# )
# def update_fig1hr_topics(selectedtopic,selectedevent):
#
#     #val = str + "/1hr/topics/window_1hr_" + selectedevent + "_" + selectedtopic + ".csv";
#
#     myTuple = (str11, "/1hr/topics/window_1hr_", selectedevent, "_", selectedtopic, ".csv")
#     x = "".join(myTuple)
#     val = x
#
#     topic_list_1hr1 = pd.read_csv(val);
#     dd = topic_list_1hr1.drop(columns=['year']);
#     traces = [];
#     number_of_colors = 20
#     for (columnName, columnData) in dd.iteritems():
#         traces.append(
#             go.Bar(
#                 x=[0.5, 1, 1.5, 2, 2.5, 3],
#                 y=columnData.values,
#                 name=columnName,
#                 opacity=0.5
#             ))
#     return {
#         'data': traces,
#         'layout': {
#             'title': 'Visualization of Keyword Evolution',
#             'barmode': 'stack'
#         },
#     }
# #--------------------------------------------------------------------------------------------------
