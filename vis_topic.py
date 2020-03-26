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
import copy
from io import BytesIO
from wordcloud import WordCloud
import base64

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

# #60 minutes window
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
    ),
    dcc.Graph(id='5min1_event'),
    dcc.Graph(id='5min1_topic'),
    dcc.RadioItems(id='radio5',
                       labelStyle={'display': 'inline-block'}
                       ),
    html.Div([
        dcc.Graph(id='5min1_keyword')
    ], style={'display': 'inline-block', 'width': '49%'}),
    html.Div([
        html.Img(id="image_wc5"),
        html.Label(
            'Word Cloud of the selected topic : Visual representation of words in the topic using corresponding distributions over the window'),

    ], style={'display': 'inline-block', 'width': '49%'}),
])

layout_page2 = html.Div([
    html.H2('Evolution of topics and keywords over the 10 Minutes window'),
    html.Button('Click to see the list of events', id="but1"),
    html.H4(id='head1'),
    dcc.Dropdown(
        id='opt-dropdown_10min'
    ),
    dcc.Graph(id='10min1_event'),
    dcc.Graph(id='10min1_topic'),
    dcc.RadioItems(id='radio10',
                       labelStyle={'display': 'inline-block'}
                       ),
    html.Div([
        dcc.Graph(id='10min1_keyword')
    ], style={'display': 'inline-block', 'width': '49%'}),
    html.Div([
        html.Img(id="image_wc10"),
        html.Label(
            'Word Cloud of the selected topic : Visual representation of words in the topic using corresponding distributions over the window'),

    ], style={'display': 'inline-block', 'width': '49%'}),
])

layout_page3 = html.Div([
    html.H2('Evolution of topics and keywords over the 60 Minutes window'),
    html.Button('Click to see the list of events', id="but1"),
    html.H4(id='head1'),
    dcc.Dropdown(
        id='opt-dropdown_60min'
    ),
    dcc.Graph(id='60min1_event'),
    dcc.Graph(id='60min1_topic'),
    dcc.RadioItems(id='radio60',
                       labelStyle={'display': 'inline-block'}
                       ),
    html.Div([
        dcc.Graph(id='60min1_keyword')
    ], style={'display': 'inline-block', 'width': '49%'}),
    html.Div([
        html.Img(id="image_wc60"),
        html.Label(
            'Word Cloud of the selected topic : Visual representation of words in the topic using corresponding distributions over the window'),
    ], style={'display': 'inline-block', 'width': '49%'}),
])

def plot_wordcloud(data):
    d = {a: x for a, x in data.values}
    wc = WordCloud(background_color='white', width=480, height=360)
    wc.fit_words(d)
    return wc.to_image()
#-----------WORD CLOUD-------------------------------------------------------------
@app.callback(Output('image_wc5', 'src'),
              [Input('image_wc5', 'id'),
               Input('5min1_event', 'clickData'),
               Input('opt-dropdown_5min', 'value')
               ])
def make_image(b,clickData,selectedevent):
    selected_topic = json.loads(json.dumps(json.loads(json.dumps(clickData))['points']))[0]['curveNumber']
    traces = []
    el5 = []
    topic5 = []
    #
    list_of_files_5 = glob.glob('data/topics/5_*.json')
    latest_file_5 = max(list_of_files_5, key=os.path.getctime)
    #
    with open(latest_file_5) as json_file:
        json_str = json.load(json_file)
    data_5 = json.loads(json_str)
    #
    for i in data_5:
        if (i['event_name'] == selectedevent):
            el5.append(i['event_name'])
            topic5.append(i['topics'])
    df = pd.DataFrame([el5, topic5]).T
    #
    tempdf = df[1][0]
    df2 = tempdf[selected_topic]

    tp = []
    for timeslice in df2:
        for wordspair in timeslice:
            tp.append(wordspair[1])
    mylist = list(set(tp))

    empty_dict = []
    empty_dict = dict.fromkeys(mylist)

    temp_list = []

    for timeslice in df2:
        empty_dict = []
        empty_dict = dict.fromkeys(mylist)
        for wordspair in timeslice:
            if wordspair[1] in mylist:
                empty_dict[wordspair[1]] = wordspair[0]
        for i in empty_dict:
            if empty_dict[i] is None:
                empty_dict[i] = 0
        temp_list.append(copy.deepcopy(empty_dict))

    new_dict = {}
    for word in mylist:
        new_dict[word] = []

    for item in temp_list:
        for word, p in item.items():
            new_dict[word].append(p)

    dict2 = {}
    for key in new_dict:
        dict2[key] = sum(new_dict[key])

    kk = list(dict2.keys())
    kk1 = list(dict2.values())

    dfm = pd.DataFrame({'word': kk, 'freq': kk1})
    img = BytesIO()
    plot_wordcloud(data=dfm).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())
#----------------WC:10min--------------------------------------------------------------
@app.callback(Output('image_wc10', 'src'),
              [Input('image_wc10', 'id'),
               Input('10min1_event', 'clickData'),
               Input('opt-dropdown_10min', 'value')
               ])
def make_image(b,clickData,selectedevent):
    selected_topic = json.loads(json.dumps(json.loads(json.dumps(clickData))['points']))[0]['curveNumber']
    traces = []
    el5 = []
    topic5 = []
    #
    list_of_files_5 = glob.glob('data/topics/10_*.json')
    latest_file_5 = max(list_of_files_5, key=os.path.getctime)
    #
    with open(latest_file_5) as json_file:
        json_str = json.load(json_file)
    data_5 = json.loads(json_str)
    #
    for i in data_5:
        if (i['event_name'] == selectedevent):
            el5.append(i['event_name'])
            topic5.append(i['topics'])
    df = pd.DataFrame([el5, topic5]).T
    #
    tempdf = df[1][0]
    df2 = tempdf[selected_topic]

    tp = []
    for timeslice in df2:
        for wordspair in timeslice:
            tp.append(wordspair[1])
    mylist = list(set(tp))

    empty_dict = []
    empty_dict = dict.fromkeys(mylist)

    temp_list = []

    for timeslice in df2:
        empty_dict = []
        empty_dict = dict.fromkeys(mylist)
        for wordspair in timeslice:
            if wordspair[1] in mylist:
                empty_dict[wordspair[1]] = wordspair[0]
        for i in empty_dict:
            if empty_dict[i] is None:
                empty_dict[i] = 0
        temp_list.append(copy.deepcopy(empty_dict))

    new_dict = {}
    for word in mylist:
        new_dict[word] = []

    for item in temp_list:
        for word, p in item.items():
            new_dict[word].append(p)

    dict2 = {}
    for key in new_dict:
        dict2[key] = sum(new_dict[key])

    kk = list(dict2.keys())
    kk1 = list(dict2.values())

    dfm = pd.DataFrame({'word': kk, 'freq': kk1})
    img = BytesIO()
    plot_wordcloud(data=dfm).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

#----------------------WC:60------------------------------------------------------------
@app.callback(Output('image_wc60', 'src'),
              [Input('image_wc60', 'id'),
               Input('60min1_event', 'clickData'),
               Input('opt-dropdown_60min', 'value')
               ])
def make_image(b,clickData,selectedevent):
    selected_topic = json.loads(json.dumps(json.loads(json.dumps(clickData))['points']))[0]['curveNumber']
    traces = []
    el5 = []
    topic5 = []
    #
    list_of_files_5 = glob.glob('data/topics/60_*.json')
    latest_file_5 = max(list_of_files_5, key=os.path.getctime)
    #
    with open(latest_file_5) as json_file:
        json_str = json.load(json_file)
    data_5 = json.loads(json_str)
    #
    for i in data_5:
        if (i['event_name'] == selectedevent):
            el5.append(i['event_name'])
            topic5.append(i['topics'])
    df = pd.DataFrame([el5, topic5]).T
    #
    tempdf = df[1][0]
    df2 = tempdf[selected_topic]

    tp = []
    for timeslice in df2:
        for wordspair in timeslice:
            tp.append(wordspair[1])
    mylist = list(set(tp))

    empty_dict = []
    empty_dict = dict.fromkeys(mylist)

    temp_list = []

    for timeslice in df2:
        empty_dict = []
        empty_dict = dict.fromkeys(mylist)
        for wordspair in timeslice:
            if wordspair[1] in mylist:
                empty_dict[wordspair[1]] = wordspair[0]
        for i in empty_dict:
            if empty_dict[i] is None:
                empty_dict[i] = 0
        temp_list.append(copy.deepcopy(empty_dict))

    new_dict = {}
    for word in mylist:
        new_dict[word] = []

    for item in temp_list:
        for word, p in item.items():
            new_dict[word].append(p)

    dict2 = {}
    for key in new_dict:
        dict2[key] = sum(new_dict[key])

    kk = list(dict2.keys())
    kk1 = list(dict2.values())

    dfm = pd.DataFrame({'word': kk, 'freq': kk1})
    img = BytesIO()
    plot_wordcloud(data=dfm).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())
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
    # my_colors = [  ## add the standard plotly colors
    #     '#85C1E9',
    #     '#858FE9',
    #     '#AD85E9',
    #     '#DF85E9',
    #     '#E985C1',
    #     '#E9858F',
    #     '#E98D85',
    #     '#E98D85',
    #     '#E1E985',
    #     '#AFE985'
    # ]
    el5 = []
    strength5 = []
    traces=[]
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

    strength5_new = list(map(list, zip(*strength5[0])))

    print(len(strength5_new))
    for i, vals in enumerate(strength5_new):
        traces.append(
            go.Scatter(
                x=[1, 2, 3, 4, 5, 6],
                y=vals,
                type='scatter',
                mode='markers',
                line=dict(width=0.5),
                stackgroup='one',
                fill='tonexty',
                name=i,
                opacity=1,
                marker=dict(size = 15)

            ))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={
                'title': 'Time slice',
                'type': 'linear'

            },
            yaxis={
                'title': 'Strength of Topics',
                'type': 'linear'

            },
            title='Visualization of Topics Evolution ( The strength of a topic over the time slices are to be inferred only by the coloured area of the topic respectively )',
            hovermode='closest',
            clickmode='event+select'
        )

    }

@app.callback(
    Output('5min1_topic', 'figure'),
    [Input('5min1_event', 'clickData'),
    Input('opt-dropdown_5min', 'value')])
def display_click_data(clickData,selectedevent):
    selected_topic = json.loads(json.dumps(json.loads(json.dumps(clickData))['points']))[0]['curveNumber']
    # print(m)
    # print(selectedevent)
    traces = []
    el5 = []
    topic5 = []
    #
    list_of_files_5 = glob.glob('data/topics/5_*.json')
    latest_file_5 = max(list_of_files_5, key=os.path.getctime)
    #
    with open(latest_file_5) as json_file:
        json_str = json.load(json_file)
    data_5 = json.loads(json_str)
    #
    for i in data_5:
        if (i['event_name'] == selectedevent):
            el5.append(i['event_name'])
            topic5.append(i['topics'])
    df = pd.DataFrame([el5, topic5]).T
    #
    tempdf = df[1][0]
    df2 = tempdf[selected_topic]

    tp = []
    for timeslice in df2:
        for wordspair in timeslice:
            tp.append(wordspair[1])
    mylist = list(set(tp))

    empty_dict = []
    empty_dict = dict.fromkeys(mylist)

    temp_list = []

    for timeslice in df2:
        empty_dict = []
        empty_dict = dict.fromkeys(mylist)
        for wordspair in timeslice:
            if wordspair[1] in mylist:
                empty_dict[wordspair[1]] = wordspair[0]
        for i in empty_dict:
            if empty_dict[i] is None:
                empty_dict[i] = 0
        temp_list.append(copy.deepcopy(empty_dict))

    new_dict = {}
    for word in mylist:
        new_dict[word] = []

    for item in temp_list:
        for word, p in item.items():
            new_dict[word].append(p)

    for word, p in new_dict.items():
        # maxp = max(p)
        # newp = [x / maxp for x in p]
        traces.append(
            go.Bar(
                x=[1, 2, 3, 4, 5],
                y=p,
                name=word,
                opacity=1,
                # marker=dict(color='MediumPurple')
            ))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={
                'title': 'Time slice',
                'type': 'linear'

            },
            yaxis={
                'title': 'Distribution of keywords',
                'type': 'linear'

            },
            title='Visualization of Distribution of keywords ( The distribution of a keyword on a time slice is to be inferred only by the respective coloured area on the bar for the keyword )',
            barmode='stack',
            colorway=['#C62828', '#AD1457', '#6A1B9A','#4527A0','#283593','#1565C0','#0277BD','#00838F','#00695C','#2E7D32','#558B2F','#9E9D24','#F9A825','#FF8F00','#EF6C00','#D84315','#4E342E','#424242','#37474F','#000000']
            # colorway ='BluYl_4'
        )
    }

@app.callback(
    Output('radio5', 'options'),
    [Input('5min1_event', 'clickData'),
     Input('opt-dropdown_5min', 'value')]
)
def radio_options5(clickData,selectedevent):
    selected_topic = json.loads(json.dumps(json.loads(json.dumps(clickData))['points']))[0]['curveNumber']
    traces = []
    el5 = []
    topic5 = []
    #
    list_of_files_5 = glob.glob('data/topics/5_*.json')
    latest_file_5 = max(list_of_files_5, key=os.path.getctime)
    #
    with open(latest_file_5) as json_file:
        json_str = json.load(json_file)
    data_5 = json.loads(json_str)
    #
    for i in data_5:
        if (i['event_name'] == selectedevent):
            el5.append(i['event_name'])
            topic5.append(i['topics'])
    df = pd.DataFrame([el5, topic5]).T
    #
    tempdf = df[1][0]
    df2 = tempdf[selected_topic]

    tp = []
    for timeslice in df2:
        for wordspair in timeslice:
            tp.append(wordspair[1])
    mylist = list(set(tp))
    return [{'label': opt, 'value': opt} for opt in mylist]

#5min1_keyword
@app.callback(
    Output('5min1_keyword', 'figure'),
    [Input('opt-dropdown_5min', 'value'),
     Input('5min1_event', 'clickData'),
     Input('radio5', 'value')]
)

def keyword_plot5(selectedevent,clickData, selectedkeyword):
    selected_topic = json.loads(json.dumps(json.loads(json.dumps(clickData))['points']))[0]['curveNumber']
    traces = []
    el5 = []
    topic5 = []
    #
    list_of_files_5 = glob.glob('data/topics/5_*.json')
    latest_file_5 = max(list_of_files_5, key=os.path.getctime)
    #
    with open(latest_file_5) as json_file:
        json_str = json.load(json_file)
    data_5 = json.loads(json_str)
    #
    for i in data_5:
        if (i['event_name'] == selectedevent):
            el5.append(i['event_name'])
            topic5.append(i['topics'])
    df = pd.DataFrame([el5, topic5]).T
    #
    tempdf = df[1][0]
    df2 = tempdf[selected_topic]

    tp = []
    for timeslice in df2:
        for wordspair in timeslice:
            tp.append(wordspair[1])
    mylist = list(set(tp))

    empty_dict = []
    empty_dict = dict.fromkeys(mylist)

    temp_list = []

    for timeslice in df2:
        empty_dict = []
        empty_dict = dict.fromkeys(mylist)
        for wordspair in timeslice:
            if wordspair[1] in mylist:
                empty_dict[wordspair[1]] = wordspair[0]
        for i in empty_dict:
            if empty_dict[i] is None:
                empty_dict[i] = 0
        temp_list.append(copy.deepcopy(empty_dict))

    new_dict = {}
    for word in mylist:
        new_dict[word] = []

    for item in temp_list:
        for word, p in item.items():
            new_dict[word].append(p)
    keyword_val = new_dict[selectedkeyword]
    print(keyword_val)
    traces.append(
        go.Scatter(
            x=[1, 2, 3, 4, 5],
            y=keyword_val,
            mode='lines+markers',
            name=selectedkeyword

        ))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={
                'title': 'Time slice',
                'type': 'linear'

            },
            yaxis={
                'title': 'Strength of Keyword',
                'type': 'linear'

            },
            title='Visualization of Keyword Evolution'
        )

    }
# For 10 minutes window
# ----------------------------------------------------------------------------------------
# Callback for Fig 1 - Evolution of topics in an event
# ----------------------------------------------------

# @app.callback(
#     Output('head1', 'value'),
#     [Input('but1', 'n_clicks')]
# )
# def but1_click(n):
#     if n:
#         return 'List of Bursting Events ( Select one to view the topic evolution )'

@app.callback(
    Output('opt-dropdown_10min', 'options'),
    [Input('but1', 'n_clicks')]
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
    # my_colors = [  ## add the standard plotly colors
    #     '#85C1E9',
    #     '#858FE9',
    #     '#AD85E9',
    #     '#DF85E9',
    #     '#E985C1',
    #     '#E9858F',
    #     '#E98D85',
    #     '#E98D85',
    #     '#E1E985',
    #     '#AFE985'
    # ]
    el5 = []
    strength5 = []
    traces=[]
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

    strength5_new = list(map(list, zip(*strength5[0])))

    print(len(strength5_new))
    for i, vals in enumerate(strength5_new):
        traces.append(
            go.Scatter(
                x=[1,2,3,4,5,6],
                y=vals,
                type='scatter',
                mode='markers',
                line=dict(width=0.5),
                stackgroup='one',
                fill='tonexty',
                name=i,
                opacity=1,
                marker=dict(size = 15)

            ))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={
                'title': 'Time slice',
                'type': 'linear'

            },
            yaxis={
                'title': 'Strength of Topics',
                'type': 'linear'

            },
            title='Visualization of Topics Evolution ( The strength of a topic over the time slices are to be inferred only by the coloured area of the topic respectively )',
            hovermode='closest',
            clickmode='event+select'
        )

    }

@app.callback(
    Output('10min1_topic', 'figure'),
    [Input('10min1_event', 'clickData'),
    Input('opt-dropdown_10min', 'value')])
def display_click_data(clickData,selectedevent):
    selected_topic = json.loads(json.dumps(json.loads(json.dumps(clickData))['points']))[0]['curveNumber']
    # print(m)
    # print(selectedevent)
    traces = []
    el5 = []
    topic5 = []
    #
    list_of_files_5 = glob.glob('data/topics/10_*.json')
    latest_file_5 = max(list_of_files_5, key=os.path.getctime)
    #
    with open(latest_file_5) as json_file:
        json_str = json.load(json_file)
    data_5 = json.loads(json_str)
    #
    for i in data_5:
        if (i['event_name'] == selectedevent):
            el5.append(i['event_name'])
            topic5.append(i['topics'])
    df = pd.DataFrame([el5, topic5]).T
    #
    tempdf = df[1][0]
    df2 = tempdf[selected_topic]

    tp = []
    for timeslice in df2:
        for wordspair in timeslice:
            tp.append(wordspair[1])
    mylist = list(set(tp))

    empty_dict = []
    empty_dict = dict.fromkeys(mylist)

    temp_list = []

    for timeslice in df2:
        empty_dict = []
        empty_dict = dict.fromkeys(mylist)
        for wordspair in timeslice:
            if wordspair[1] in mylist:
                empty_dict[wordspair[1]] = wordspair[0]
        for i in empty_dict:
            if empty_dict[i] is None:
                empty_dict[i] = 0
        temp_list.append(copy.deepcopy(empty_dict))

    new_dict = {}
    for word in mylist:
        new_dict[word] = []

    for item in temp_list:
        for word, p in item.items():
            new_dict[word].append(p)

    for word, p in new_dict.items():
        # maxp = max(p)
        # newp = [x / maxp for x in p]
        traces.append(
            go.Bar(
                x=[1,2,3,4,5,6],
                y=p,
                name=word,
                opacity=1,
                # marker=dict(color='MediumPurple')
            ))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={
                'title': 'Time slice',
                'type': 'linear'

            },
            yaxis={
                'title': 'Distribution of keywords',
                'type': 'linear'

            },
            title='Visualization of Distribution of keywords ( The distribution of a keyword on a time slice is to be inferred only by the respective coloured area on the bar for the keyword )',
            barmode='stack',
            colorway=['#C62828', '#AD1457', '#6A1B9A','#4527A0','#283593','#1565C0','#0277BD','#00838F','#00695C','#2E7D32','#558B2F','#9E9D24','#F9A825','#FF8F00','#EF6C00','#D84315','#4E342E','#424242','#37474F','#000000']
            # colorway ='BluYl_4'
        )
    }

@app.callback(
    Output('radio10', 'options'),
    [Input('10min1_event', 'clickData'),
     Input('opt-dropdown_10min', 'value')]
)
def radio_options5(clickData,selectedevent):
    selected_topic = json.loads(json.dumps(json.loads(json.dumps(clickData))['points']))[0]['curveNumber']
    traces = []
    el5 = []
    topic5 = []
    #
    list_of_files_5 = glob.glob('data/topics/10_*.json')
    latest_file_5 = max(list_of_files_5, key=os.path.getctime)
    #
    with open(latest_file_5) as json_file:
        json_str = json.load(json_file)
    data_5 = json.loads(json_str)
    #
    for i in data_5:
        if (i['event_name'] == selectedevent):
            el5.append(i['event_name'])
            topic5.append(i['topics'])
    df = pd.DataFrame([el5, topic5]).T
    #
    tempdf = df[1][0]
    df2 = tempdf[selected_topic]

    tp = []
    for timeslice in df2:
        for wordspair in timeslice:
            tp.append(wordspair[1])
    mylist = list(set(tp))
    return [{'label': opt, 'value': opt} for opt in mylist]

#5min1_keyword
@app.callback(
    Output('10min1_keyword', 'figure'),
    [Input('opt-dropdown_10min', 'value'),
     Input('10min1_event', 'clickData'),
     Input('radio10', 'value')]
)

def keyword_plot5(selectedevent,clickData, selectedkeyword):
    selected_topic = json.loads(json.dumps(json.loads(json.dumps(clickData))['points']))[0]['curveNumber']
    traces = []
    el5 = []
    topic5 = []
    #
    list_of_files_5 = glob.glob('data/topics/10_*.json')
    latest_file_5 = max(list_of_files_5, key=os.path.getctime)
    #
    with open(latest_file_5) as json_file:
        json_str = json.load(json_file)
    data_5 = json.loads(json_str)
    #
    for i in data_5:
        if (i['event_name'] == selectedevent):
            el5.append(i['event_name'])
            topic5.append(i['topics'])
    df = pd.DataFrame([el5, topic5]).T
    #
    tempdf = df[1][0]
    df2 = tempdf[selected_topic]

    tp = []
    for timeslice in df2:
        for wordspair in timeslice:
            tp.append(wordspair[1])
    mylist = list(set(tp))

    empty_dict = []
    empty_dict = dict.fromkeys(mylist)

    temp_list = []

    for timeslice in df2:
        empty_dict = []
        empty_dict = dict.fromkeys(mylist)
        for wordspair in timeslice:
            if wordspair[1] in mylist:
                empty_dict[wordspair[1]] = wordspair[0]
        for i in empty_dict:
            if empty_dict[i] is None:
                empty_dict[i] = 0
        temp_list.append(copy.deepcopy(empty_dict))

    new_dict = {}
    for word in mylist:
        new_dict[word] = []

    for item in temp_list:
        for word, p in item.items():
            new_dict[word].append(p)
    keyword_val = new_dict[selectedkeyword]
    print(keyword_val)
    traces.append(
        go.Scatter(
            x=[1,2,3,4,5,6],
            y=keyword_val,
            mode='lines+markers',
            name=selectedkeyword

        ))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={
                'title': 'Time slice',
                'type': 'linear'

            },
            yaxis={
                'title': 'Strength of Keyword',
                'type': 'linear'

            },
            title='Visualization of Keyword Evolution'
        )

    }
# For 60 minutes window
# ----------------------------------------------------------------------------------------
# Callback for Fig 1 - Evolution of topics in an event
# ----------------------------------------------------
#
# @app.callback(
#     Output('head1', 'value'),
#     [Input('but1', 'n_clicks')]
# )
# def but1_click(n):
#     if n:
#         return 'List of Bursting Events ( Select one to view the topic evolution )'

@app.callback(
    Output('opt-dropdown_60min', 'options'),
    [Input('but1', 'n_clicks')]
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
    # my_colors = [  ## add the standard plotly colors
    #     '#85C1E9',
    #     '#858FE9',
    #     '#AD85E9',
    #     '#DF85E9',
    #     '#E985C1',
    #     '#E9858F',
    #     '#E98D85',
    #     '#E98D85',
    #     '#E1E985',
    #     '#AFE985'
    # ]
    el5 = []
    strength5 = []
    traces=[]
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

    strength5_new = list(map(list, zip(*strength5[0])))

    print(len(strength5_new))
    for i, vals in enumerate(strength5_new):
        traces.append(
            go.Scatter(
                x=[10, 20, 30, 40, 50, 60],
                y=vals,
                type='scatter',
                mode='markers',
                line=dict(width=0.5),
                stackgroup='one',
                fill='tonexty',
                name=i,
                opacity=1,
                marker=dict(size = 15)

            ))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={
                'title': 'Time slice',
                'type': 'linear'

            },
            yaxis={
                'title': 'Strength of Topics',
                'type': 'linear'

            },
            title='Visualization of Topics Evolution ( The strength of a topic over the time slices are to be inferred only by the coloured area of the topic respectively )',
            hovermode='closest',
            clickmode='event+select'
        )

    }

@app.callback(
    Output('60min1_topic', 'figure'),
    [Input('60min1_event', 'clickData'),
    Input('opt-dropdown_60min', 'value')])
def display_click_data(clickData,selectedevent):
    selected_topic = json.loads(json.dumps(json.loads(json.dumps(clickData))['points']))[0]['curveNumber']
    # print(m)
    # print(selectedevent)
    traces = []
    el5 = []
    topic5 = []
    #
    list_of_files_5 = glob.glob('data/topics/60_*.json')
    latest_file_5 = max(list_of_files_5, key=os.path.getctime)
    #
    with open(latest_file_5) as json_file:
        json_str = json.load(json_file)
    data_5 = json.loads(json_str)
    #
    for i in data_5:
        if (i['event_name'] == selectedevent):
            el5.append(i['event_name'])
            topic5.append(i['topics'])
    df = pd.DataFrame([el5, topic5]).T
    #
    tempdf = df[1][0]
    df2 = tempdf[selected_topic]

    tp = []
    for timeslice in df2:
        for wordspair in timeslice:
            tp.append(wordspair[1])
    mylist = list(set(tp))

    empty_dict = []
    empty_dict = dict.fromkeys(mylist)

    temp_list = []

    for timeslice in df2:
        empty_dict = []
        empty_dict = dict.fromkeys(mylist)
        for wordspair in timeslice:
            if wordspair[1] in mylist:
                empty_dict[wordspair[1]] = wordspair[0]
        for i in empty_dict:
            if empty_dict[i] is None:
                empty_dict[i] = 0
        temp_list.append(copy.deepcopy(empty_dict))

    new_dict = {}
    for word in mylist:
        new_dict[word] = []

    for item in temp_list:
        for word, p in item.items():
            new_dict[word].append(p)

    for word, p in new_dict.items():
        # maxp = max(p)
        # newp = [x / maxp for x in p]
        traces.append(
            go.Bar(
                x=[10, 20, 30, 40, 50,60],
                y=p,
                name=word,
                opacity=1,
                # marker=dict(color='MediumPurple')
            ))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={
                'title': 'Time slice',
                'type': 'linear'

            },
            yaxis={
                'title': 'Distribution of keywords',
                'type': 'linear'

            },
            title='Visualization of Distribution of keywords ( The distribution of a keyword on a time slice is to be inferred only by the respective coloured area on the bar for the keyword )',
            barmode='stack',
            colorway=['#C62828', '#AD1457', '#6A1B9A','#4527A0','#283593','#1565C0','#0277BD','#00838F','#00695C','#2E7D32','#558B2F','#9E9D24','#F9A825','#FF8F00','#EF6C00','#D84315','#4E342E','#424242','#37474F','#000000']
            # colorway ='BluYl_4'
        )
    }

@app.callback(
    Output('radio60', 'options'),
    [Input('60min1_event', 'clickData'),
     Input('opt-dropdown_60min', 'value')]
)
def radio_options5(clickData,selectedevent):
    selected_topic = json.loads(json.dumps(json.loads(json.dumps(clickData))['points']))[0]['curveNumber']
    traces = []
    el5 = []
    topic5 = []
    #
    list_of_files_5 = glob.glob('data/topics/60_*.json')
    latest_file_5 = max(list_of_files_5, key=os.path.getctime)
    #
    with open(latest_file_5) as json_file:
        json_str = json.load(json_file)
    data_5 = json.loads(json_str)
    #
    for i in data_5:
        if (i['event_name'] == selectedevent):
            el5.append(i['event_name'])
            topic5.append(i['topics'])
    df = pd.DataFrame([el5, topic5]).T
    #
    tempdf = df[1][0]
    df2 = tempdf[selected_topic]

    tp = []
    for timeslice in df2:
        for wordspair in timeslice:
            tp.append(wordspair[1])
    mylist = list(set(tp))
    return [{'label': opt, 'value': opt} for opt in mylist]

#5min1_keyword
@app.callback(
    Output('60min1_keyword', 'figure'),
    [Input('opt-dropdown_60min', 'value'),
     Input('60min1_event', 'clickData'),
     Input('radio60', 'value')]
)

def keyword_plot5(selectedevent,clickData, selectedkeyword):
    selected_topic = json.loads(json.dumps(json.loads(json.dumps(clickData))['points']))[0]['curveNumber']
    traces = []
    el5 = []
    topic5 = []
    #
    list_of_files_5 = glob.glob('data/topics/60_*.json')
    latest_file_5 = max(list_of_files_5, key=os.path.getctime)
    #
    with open(latest_file_5) as json_file:
        json_str = json.load(json_file)
    data_5 = json.loads(json_str)
    #
    for i in data_5:
        if (i['event_name'] == selectedevent):
            el5.append(i['event_name'])
            topic5.append(i['topics'])
    df = pd.DataFrame([el5, topic5]).T
    #
    tempdf = df[1][0]
    df2 = tempdf[selected_topic]

    tp = []
    for timeslice in df2:
        for wordspair in timeslice:
            tp.append(wordspair[1])
    mylist = list(set(tp))

    empty_dict = []
    empty_dict = dict.fromkeys(mylist)

    temp_list = []

    for timeslice in df2:
        empty_dict = []
        empty_dict = dict.fromkeys(mylist)
        for wordspair in timeslice:
            if wordspair[1] in mylist:
                empty_dict[wordspair[1]] = wordspair[0]
        for i in empty_dict:
            if empty_dict[i] is None:
                empty_dict[i] = 0
        temp_list.append(copy.deepcopy(empty_dict))

    new_dict = {}
    for word in mylist:
        new_dict[word] = []

    for item in temp_list:
        for word, p in item.items():
            new_dict[word].append(p)
    keyword_val = new_dict[selectedkeyword]
    print(keyword_val)
    traces.append(
        go.Scatter(
            x=[10, 20, 30, 40, 50,60],
            y=keyword_val,
            mode='lines+markers',
            name=selectedkeyword

        ))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={
                'title': 'Time slice',
                'type': 'linear'

            },
            yaxis={
                'title': 'Strength of Keyword',
                'type': 'linear'

            },
            title='Visualization of Keyword Evolution'
        )

    }

