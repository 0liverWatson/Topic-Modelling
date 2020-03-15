import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import random

from app import app

str11 = "https://raw.githubusercontent.com/SubhshreeMangaraj/Topic-Modelling/master/DS/";

#Extract the events for all the windows
#--------------------------------------

#5 minutes window
event_list5 = pd.read_csv("https://raw.githubusercontent.com/SubhshreeMangaraj/Topic-Modelling/master/DS/5min/eventlist_5min.csv")
el5 = event_list5.Events.unique()
el5 = el5.tolist()

#10 minutes window
event_list10 = pd.read_csv("https://raw.githubusercontent.com/SubhshreeMangaraj/Topic-Modelling/master/DS/10min/eventlist_10min.csv")
el10 = event_list10.Events.unique()
el10 = el10.tolist()

#1 hr window
event_list1 = pd.read_csv("https://raw.githubusercontent.com/SubhshreeMangaraj/Topic-Modelling/master/DS/1hr/eventlist_1hr.csv")
el1 = event_list1.Events.unique()
el1 = el1.tolist()

# #4 hr window
# event_list4 = pd.read_csv("https://raw.githubusercontent.com/SubhshreeMangaraj/Topic-Modelling/master/DS/4hr/eventlist_4hr.csv")
# el4 = event_list4.Events.unique()
# el4 = el4.tolist()
#
# #8 hr window
# event_list8 = pd.read_csv("https://raw.githubusercontent.com/SubhshreeMangaraj/Topic-Modelling/master/DS/8hr/eventlist_8hr.csv")
# el8 = event_list8.Events.unique()
# el8 = el8.tolist()


traces =[]

layout_page1 = html.Div([
                    html.H2('Evolution of top bursty topics over the 5 Minutes window'),
                    html.H4('List of Bursting Events ( Select one to view the topic evolution ) '),
                    dcc.Dropdown(
                        id='opt-dropdown_5min',
                        options=[{'label': opt, 'value': opt} for opt in el5]
                    ),
                    dcc.Graph(id='5min1_event'),
                    html.H4('List of Bursting Topics ( Select one to view the keyword evolution ) '),
                    dcc.Dropdown(
                        id='opt-dropdown_5min_topics'
                    ),
                    dcc.Graph(id='5min1_topic')
])

layout_page2 = html.Div([
                    html.H2('Evolution of top bursty topics over the 10 Minutes window'),
                    html.H4('List of Bursting Events ( Select one to view the topic evolution ) '),
                    dcc.Dropdown(
                          id='opt-dropdown_10min',
                          options=[{'label': opt, 'value': opt} for opt in el10]
                      ),
                      dcc.Graph(id='10min1_event'),
                      html.H4('List of Bursting Topics ( Select one to view the keyword evolution ) '),
                      dcc.Dropdown(
                          id='opt-dropdown_10min_topics'
                      ),
                      dcc.Graph(id='10min1_topic')
])

layout_page3 = html.Div([
                    html.H2('Evolution of top bursty topics over the 1 Hour window'),
                    html.H4('List of Bursting Events ( Select one to view the topic evolution ) '),
                    dcc.Dropdown(
                          id='opt-dropdown_1hr',
                          options=[{'label': opt, 'value': opt} for opt in el1]
                      ),
                      dcc.Graph(id='1hr1_event'),
                      html.H4('List of Bursting Topics ( Select one to view the keyword evolution) '),
                      dcc.Dropdown(
                          id='opt-dropdown_1hr_topics'
                      ),
                      dcc.Graph(id='1hr1_topic')
])

# For 5 minutes window
#----------------------------------------------------------------------------------------
#Callback for Fig 1 - Evolution of topics in an event
#----------------------------------------------------
@app.callback(
   Output('5min1_event', 'figure'),
   [Input('opt-dropdown_5min', 'value')]
)
def update_fig5min(selectedevent):

    val = str11 + "/5min/events/window_5min_" + selectedevent + ".csv";
    topic_list_5min1 = pd.read_csv(val);
    dd = topic_list_5min1.drop(columns=['year']);
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

    val = str11 + "/5min/events/window_5min_" + selectedevent + ".csv";

    dd = pd.read_csv(val);
    dd = dd.drop(columns=['year']);
    top5 = dd;
    top5 = list(top5.columns)
    return [{'label': opt, 'value': opt} for opt in top5]

#Callback for fig 2 - Evolution of keywords in topics
#----------------------------------------------------
@app.callback(
   Output('5min1_topic', 'figure'),
   [Input('opt-dropdown_5min_topics', 'value'),
    Input('opt-dropdown_5min', 'value')]
)
def update_fig5min_topics(selectedtopic,selectedevent):

    val = str11 + "/5min/topics/window_5min_" + selectedevent + "_" + selectedtopic + ".csv";
    topic_list_5min1 = pd.read_csv(val);
    dd = topic_list_5min1.drop(columns=['year']);
    traces = [];
    for (columnName, columnData) in dd.iteritems():
        traces.append(
            go.Bar(
                x=[0.5, 1, 1.5, 2, 2.5],
                y=columnData.values,
                name=columnName,
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




# For 10 minutes window
#----------------------------------------------------------------------------------------
#Callback for Fig 1 - Evolution of topics in an event
#----------------------------------------------------
@app.callback(
   Output('10min1_event', 'figure'),
   [Input('opt-dropdown_10min', 'value')]
)
def update_fig10min(selectedevent):

    #val = str + "/10min/events/window_10min_" +selectedevent + ".csv";

    myTuple = (str11, "/10min/events/window_10min_", selectedevent, ".csv")
    x = "".join(myTuple)
    val = x

    topic_list_10min1 = pd.read_csv(val);
    dd = topic_list_10min1.drop(columns=['year']);
    traces = [];
    number_of_colors = 20
    for (columnName, columnData) in dd.iteritems():
        traces.append(
            go.Scatter(
                x=[0.5, 1, 1.5, 2, 2.5, 3,3.5,4,4.5,5],
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
    dash.dependencies.Output("opt-dropdown_10min_topics", "options"),
    [dash.dependencies.Input('opt-dropdown_10min', 'value')],
)
def update_options(selectedevent):
    #val = str + "/10min/events/window_10min_" + selected_event + ".csv";

    myTuple = (str11, "/10min/events/window_10min_", selectedevent, ".csv")
    x = "".join(myTuple)
    val = x

    dd = pd.read_csv(val);
    dd = dd.drop(columns=['year']);
    top10 = dd;
    top10 = list(top10.columns)
    return [{'label': opt, 'value': opt} for opt in top10]

#Callback for fig 2 - Evolution of keywords in topics
#----------------------------------------------------
@app.callback(
   Output('10min1_topic', 'figure'),
   [Input('opt-dropdown_10min_topics', 'value'),
    Input('opt-dropdown_10min', 'value')]
)
def update_fig10min_topics(selectedtopic,selectedevent):

    #val = str + "/10min/topics/window_10min_" + selectedevent + "_" + selectedtopic + ".csv";

    myTuple = (str11, "/10min/topics/window_10min_", selectedevent, "_", selectedtopic, ".csv")
    x = "".join(myTuple)
    val = x

    topic_list_10min1 = pd.read_csv(val);
    dd = topic_list_10min1.drop(columns=['year']);
    traces = [];
    number_of_colors = 20
    for (columnName, columnData) in dd.iteritems():
        traces.append(
            go.Bar(
                x=[0.5, 1, 1.5, 2, 2.5, 3,3.5,4,4.5,5],
                y=columnData.values,
                name=columnName,
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



# For 1 hour window
#----------------------------------------------------------------------------------------
#Callback for Fig 1 - Evolution of topics in an event
#----------------------------------------------------
@app.callback(
   Output('1hr1_event', 'figure'),
   [Input('opt-dropdown_1hr', 'value')]
)
def update_fig1hr(selectedevent):

    #val = str + "/1hr/events/window_1hr_" +selectedevent + ".csv";

    myTuple = (str11, "/1hr/events/window_1hr_", selectedevent, ".csv")
    x = "".join(myTuple)
    val = x

    topic_list_1hr1 = pd.read_csv(val);
    dd = topic_list_1hr1.drop(columns=['year']);
    traces = [];
    number_of_colors = 20
    for (columnName, columnData) in dd.iteritems():
        traces.append(
            go.Scatter(
                x=[0.5, 1, 1.5, 2, 2.5, 3],
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
    dash.dependencies.Output("opt-dropdown_1hr_topics", "options"),
    [dash.dependencies.Input('opt-dropdown_1hr', 'value')],
)
def update_options(selectedevent):
    #val = str + "/1hr/events/window_1hr_" + selected_event + ".csv";

    myTuple = (str11, "/1hr/events/window_1hr_", selectedevent, ".csv")
    x = "".join(myTuple)
    val = x

    dd = pd.read_csv(val);
    dd = dd.drop(columns=['year']);
    top1 = dd;
    top1 = list(top1.columns)
    return [{'label': opt, 'value': opt} for opt in top1]

#Callback for fig 2 - Evolution of keywords in topics
#----------------------------------------------------
@app.callback(
   Output('1hr1_topic', 'figure'),
   [Input('opt-dropdown_1hr_topics', 'value'),
    Input('opt-dropdown_1hr', 'value')]
)
def update_fig1hr_topics(selectedtopic,selectedevent):

    #val = str + "/1hr/topics/window_1hr_" + selectedevent + "_" + selectedtopic + ".csv";

    myTuple = (str11, "/1hr/topics/window_1hr_", selectedevent, "_", selectedtopic, ".csv")
    x = "".join(myTuple)
    val = x

    topic_list_1hr1 = pd.read_csv(val);
    dd = topic_list_1hr1.drop(columns=['year']);
    traces = [];
    number_of_colors = 20
    for (columnName, columnData) in dd.iteritems():
        traces.append(
            go.Bar(
                x=[0.5, 1, 1.5, 2, 2.5, 3],
                y=columnData.values,
                name=columnName,
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
