import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import glob
import os
from app import app
import json


# Extract the events for all the windows
# --------------------------------------

# #5 minutes window
# -----------------
list_of_files_5 = glob.glob('data/topics/5_*.json')
if(len(list_of_files_5)>0):
    latest_file_5 = max(list_of_files_5, key=os.path.getctime)
    with open(latest_file_5) as json_file:
        json_str = json.load(json_file)
    data_5 = json.loads(json_str)

# #10 minutes window
# -----------------
list_of_files_10 = glob.glob('data/topics/10_*.json')
if(len(list_of_files_10)>0):
    latest_file_10 = max(list_of_files_10, key=os.path.getctime)

    with open(latest_file_10) as json_file:
        json_str = json.load(json_file)
    data_10 = json.loads(json_str)

# 60 minutes window
# -----------------
list_of_files_60 = glob.glob('data/topics/60_*.json')
if(len(list_of_files_60)>0):
    latest_file_60 = max(list_of_files_60, key=os.path.getctime)

    with open(latest_file_60) as json_file:
        json_str = json.load(json_file)
    data_60 = json.loads(json_str)

traces = []

layout_page1 = html.Div([
    html.H2('Evolution of topics and keywords over the 5 Minutes window'),
    html.Button('Click to see the list of events', id="but1"),
    html.H4(id='head1'),
    dcc.Dropdown(
        id='opt-dropdown_5min'
        # options=[{'label': opt, 'value': opt} for opt in el5]
    ),
    dcc.Graph(id='5min1_event'),
    html.H4('List of Topics ( Select one to view the keyword evolution ) '),
    dcc.Dropdown(
        id='opt-dropdown_5min_topics'
    ),
    dcc.Graph(id='5min1_topic')
])


layout_page2 = html.Div([
                    html.H2('Evolution of topics and keywords over the 10 Minutes window'),
                    html.Button('Click to see the list of events', id="but2"),
                    html.H4(id='head2'),
                    dcc.Dropdown(
                          id='opt-dropdown_10min',
                          # options=[{'label': opt, 'value': opt} for opt in el10]
                      ),
                      dcc.Graph(id='10min1_event'),
                      html.H4('List of Topics ( Select one to view the keyword evolution ) '),
                      dcc.Dropdown(
                          id='opt-dropdown_10min_topics'
                      ),
                      dcc.Graph(id='10min1_topic')
])
#
layout_page3 = html.Div([
                    html.H2('Evolution of topics and keywords over the 60 Minutes window'),
                    html.Button('Click to see the list of events', id="but3"),
                    html.H4(id='head3'),
                    dcc.Dropdown(
                          id='opt-dropdown_60min',
                          # options=[{'label': opt, 'value': opt} for opt in el1]
                      ),
                      dcc.Graph(id='60min1_event'),
                      html.H4('List of Topics ( Select one to view the keyword evolution) '),
                      dcc.Dropdown(
                          id='opt-dropdown_60min_topics'
                      ),
                      dcc.Graph(id='60min1_topic')
])

# For 5 minutes window
# ----------------------------------------------------------------------------------------
# Callback for Fig 1 - Evolution of topics in an event
# ----------------------------------------------------

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
    el5 = []
    strength5 = []
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
        traces = []
        number_of_colors = 20
        for (columnName, columnData) in dd.iteritems():
            traces.append(
                go.Scatter(
                    x=[1,2,3,4,5],
                    y=columnData.values,
                    # xlable='Time slice in minutes for 5 minutes',
                    # ylable='Strength of topics',
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
                'title': 'Visualization of Topic Evolution',
                 # dict(
                 #            xaxis={
                 #                'title': 'xaxis_column_name'
                 #
                 #            }
                 #    )
            },

            }



# Callback for dropdown
# ---------------------
@app.callback(
    dash.dependencies.Output("opt-dropdown_5min_topics", "options"),
    [dash.dependencies.Input('opt-dropdown_5min', 'value')],
)
def update_options(selectedevent):
    el5 = []
    topic5 = []

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

    return [{'label': opt, 'value': opt} for opt in range(0, num_of_topics)]


# Callback for fig 2 - Evolution of keywords in topics
# ----------------------------------------------------
@app.callback(
    Output('5min1_topic', 'figure'),
    [Input('opt-dropdown_5min_topics', 'value'),
     Input('opt-dropdown_5min', 'value')]
)
def update_fig5min_topics(selectedtopic, selectedevent):
    traces = []
    if selectedtopic:
        el5 = []
        topic5 = []

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
        df2 = tempdf[selectedtopic]
        # for k in range(len(df2)):
        #     # print(df2[k])
        #     df3 = pd.DataFrame(df2[k])
        #     df3.columns = ['key_strength', 'keyword']
        #     final_df3 = df3.sort_values(by=['keyword'])
        #     traces.append(
        #         go.Bar(
        #             x=[0.5, 1, 1.5, 2, 2.5],
        #             y=final_df3['key_strength'],
        #             name=final_df3['keyword'],
        #             opacity=0.5
        #         ))
        df3 = {}

        for timeslice in df2:
            ts = {e[1]: e[0] for e in timeslice}

            if len(df3) == 0:
                for word, p in ts.items():
                    df3[word] = [p]
            else:
                for word, p in ts.items():
                    df3[word].append(p)
        for word, p in df3.items():
            maxp = max(p)
            newp = [x / maxp for x in p]
            traces.append(
                go.Bar(
                    x=[1,2,3,4,5],
                    y=newp,
                    name=word,
                    opacity=0.5,
                ))
    return {
        'data': traces,
        'layout': {
            'title': 'Visualization of Keyword Evolution',
            'barmode': 'stack'
        },
    }
# --------------------------------------------------------------------------------------------------


# For 10 minutes window
# ----------------------------------------------------------------------------------------
# Callback for Fig 1 - Evolution of topics in an event
# ----------------------------------------------------

@app.callback(
    Output('head2', 'value'),
    [Input('but2', 'n_clicks')]
)
def but1_click(n):
    if n:
        return 'List of Bursting Events ( Select one to view the topic evolution )'

@app.callback(
    Output('opt-dropdown_10min', 'options'),
    [Input('but2', 'n_clicks')]
)
def but1_click1(n):
    if n:
        list_of_files_5 = glob.glob('data/topics/10_*.json')
        latest_file_5 = max(list_of_files_5, key=os.path.getctime)

        with open(latest_file_5) as json_file:
            json_str = json.load(json_file)
        data_5 = json.loads(json_str)
        el5 = []
        for m in data_5:
            el5.append(m['event_name'])
        return [{'label': opt, 'value': opt} for opt in el5]


@app.callback(
    Output('10min1_event', 'figure'),
    [Input('opt-dropdown_10min', 'value')]
)
def update_fig5min(selectedevent):
    el5 = []
    strength5 = []
    list_of_files_5 = glob.glob('data/topics/10_*.json')
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
        traces = []
        number_of_colors = 20
        for (columnName, columnData) in dd.iteritems():
            traces.append(
                go.Scatter(
                    x=[2,4,6,8,10],
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


# Callback for dropdown
# ---------------------
@app.callback(
    dash.dependencies.Output("opt-dropdown_10min_topics", "options"),
    [dash.dependencies.Input('opt-dropdown_10min', 'value')],
)
def update_options(selectedevent):
    el5 = []
    topic5 = []

    list_of_files_5 = glob.glob('data/topics/10_*.json')
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

    return [{'label': opt, 'value': opt} for opt in range(0, num_of_topics)]


# Callback for fig 2 - Evolution of keywords in topics
# ----------------------------------------------------
@app.callback(
    Output('10min1_topic', 'figure'),
    [Input('opt-dropdown_10min_topics', 'value'),
     Input('opt-dropdown_10min', 'value')]
)
def update_fig5min_topics(selectedtopic, selectedevent):
    traces = []
    if selectedtopic:
        el5 = []
        topic5 = []

        list_of_files_5 = glob.glob('data/topics/10_*.json')
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
        df2 = tempdf[selectedtopic]
        # for k in range(len(df2)):
        #     # print(df2[k])
        #     df3 = pd.DataFrame(df2[k])
        #     df3.columns = ['key_strength', 'keyword']
        #     final_df3 = df3.sort_values(by=['keyword'])
        #     traces.append(
        #         go.Bar(
        #             x=[0.5, 1, 1.5, 2, 2.5],
        #             y=final_df3['key_strength'],
        #             name=final_df3['keyword'],
        #             opacity=0.5
        #         ))
        df3 = {}

        for timeslice in df2:
            ts = {e[1]: e[0] for e in timeslice}

            if len(df3) == 0:
                for word, p in ts.items():
                    df3[word] = [p]
            else:
                for word, p in ts.items():
                    df3[word].append(p)
        for word, p in df3.items():
            maxp = max(p)
            newp = [x / maxp for x in p]
            traces.append(
                go.Bar(
                    x=[2,4,6,8,10],
                    y=newp,
                    name=word,
                    opacity=0.5,
                ))
    return {
        'data': traces,
        'layout': {
            'title': 'Visualization of Keyword Evolution',
            'barmode': 'stack'
        },
    }
# --------------------------------------------------------------------------------------------------

# For 60 minutes window
# ----------------------------------------------------------------------------------------
# Callback for Fig 1 - Evolution of topics in an event
# ----------------------------------------------------

@app.callback(
    Output('head3', 'value'),
    [Input('but3', 'n_clicks')]
)
def but1_click(n):
    if n:
        return 'List of Bursting Events ( Select one to view the topic evolution )'

@app.callback(
    Output('opt-dropdown_60min', 'options'),
    [Input('but3', 'n_clicks')]
)
def but1_click1(n):
    if n:
        list_of_files_5 = glob.glob('data/topics/60_*.json')
        latest_file_5 = max(list_of_files_5, key=os.path.getctime)

        with open(latest_file_5) as json_file:
            json_str = json.load(json_file)
        data_5 = json.loads(json_str)
        el5 = []
        for m in data_5:
            el5.append(m['event_name'])
        return [{'label': opt, 'value': opt} for opt in el5]


@app.callback(
    Output('60min1_event', 'figure'),
    [Input('opt-dropdown_60min', 'value')]
)
def update_fig5min(selectedevent):
    el5 = []
    strength5 = []
    list_of_files_5 = glob.glob('data/topics/60_*.json')
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
        traces = []
        number_of_colors = 20
        for (columnName, columnData) in dd.iteritems():
            traces.append(
                go.Scatter(
                    x=[10,20,30,40,50,60],
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


# Callback for dropdown
# ---------------------
@app.callback(
    dash.dependencies.Output("opt-dropdown_60min_topics", "options"),
    [dash.dependencies.Input('opt-dropdown_60min', 'value')],
)
def update_options(selectedevent):
    el5 = []
    topic5 = []

    list_of_files_5 = glob.glob('data/topics/60_*.json')
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

    return [{'label': opt, 'value': opt} for opt in range(0, num_of_topics)]


# Callback for fig 2 - Evolution of keywords in topics
# ----------------------------------------------------
@app.callback(
    Output('60min1_topic', 'figure'),
    [Input('opt-dropdown_60min_topics', 'value'),
     Input('opt-dropdown_60min', 'value')]
)
def update_fig5min_topics(selectedtopic, selectedevent):
    traces = []
    if selectedtopic:
        el5 = []
        topic5 = []

        list_of_files_5 = glob.glob('data/topics/60_*.json')
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
        df2 = tempdf[selectedtopic]
        # for k in range(len(df2)):
        #     # print(df2[k])
        #     df3 = pd.DataFrame(df2[k])
        #     df3.columns = ['key_strength', 'keyword']
        #     final_df3 = df3.sort_values(by=['keyword'])
        #     traces.append(
        #         go.Bar(
        #             x=[0.5, 1, 1.5, 2, 2.5],
        #             y=final_df3['key_strength'],
        #             name=final_df3['keyword'],
        #             opacity=0.5
        #         ))
        df3 = {}

        for timeslice in df2:
            ts = {e[1]: e[0] for e in timeslice}

            if len(df3) == 0:
                for word, p in ts.items():
                    df3[word] = [p]
            else:
                for word, p in ts.items():
                    df3[word].append(p)
        for word, p in df3.items():
            maxp = max(p)
            newp = [x / maxp for x in p]
            traces.append(
                go.Bar(
                    x=[10,20,30,40,50,60],
                    y=newp,
                    name=word,
                    opacity=0.5,

                ))
    return {
        'data': traces,
        'layout': {
            'title': 'Visualization of Keyword Evolution',
            'barmode': 'stack'
        },
    }
# --------------------------------------------------------------------------------------------------
