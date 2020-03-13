import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go
import flask
import random
from datetime import datetime

app = dash.Dash(
    __name__,
    external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
)
app.config.suppress_callback_exceptions = True
#---------------------------------------------------------------------------------------
#---------------Viz 1 - Map part----------------------------

#Data Pre-processing

data = pd.read_csv('https://raw.githubusercontent.com/SubhshreeMangaraj/Topic-Modelling/master/data.csv')
event_list = data.Group.unique()
el = event_list.tolist()
fdata = data[data.Group == 'Bush Fire']
rgb = pd.DataFrame()

#----------------Color-----------------------

color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(len(event_list))])
             for i in range(len(event_list))]
rgb['Color'] = color
rgb['Group'] = el

# Create global chart template
mapbox_access_token = "pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w"

layout_map = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    # legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview",
    showlegend = False,
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(lon=-55.3781, lat=3.4360),
        zoom=2,
    )
)
#---------------------------------------------------------------------------------------
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

#4 hr window
event_list4 = pd.read_csv("https://raw.githubusercontent.com/SubhshreeMangaraj/Topic-Modelling/master/DS/4hr/eventlist_4hr.csv")
el4 = event_list4.Events.unique()
el4 = el4.tolist()

#8 hr window
event_list8 = pd.read_csv("https://raw.githubusercontent.com/SubhshreeMangaraj/Topic-Modelling/master/DS/8hr/eventlist_8hr.csv")
el8 = event_list8.Events.unique()
el8 = el8.tolist()


traces =[]

url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

layout_index = html.Div([
    html.H2('Real-time topic modelling of Disruptive Events from twitter and their Visualization'),
    html.H6("""This application shows the geo location of live streaming of disruptive tweets corresponding to disruptive events of United Kingdom. 
              Furthermore, for each event, we can visualize the top ten bursting topics over a window of 5min, 10 min, 1ht, 4hr and 8hr along
               with the important kewqords associated to each topic of each event with its contribution score to the bursting topic."""),
    html.H3("Instructions to run the application"),
    html.H6("- Click on the START button to start the application"),
    html.H6("- Click on the buttons of respective time windows for display of tweets on geomap for disruptive events, once they turn green"),
    html.Button(dcc.Link('START"', href='/start')),
    html.Br(),
    html.Br(),
    html.Button(dcc.Link('5 Minutes"',  href='/page-1', className='b1')),
    html.Button(dcc.Link('10 Minutes"', href='/page-2', className='b1')),
    html.Button(dcc.Link('1 Hour"',     href='/page-3', className='b1')),
    html.Button(dcc.Link('4 Hours"',    href='/page-4', className='b1')),
    html.Button(dcc.Link('8 Hours"',    href='/page-5', className='b1')),
    html.Br()
])

# layout_page_2 = html.Div(
#     dcc.Tabs([
#       dcc.Tab(label='5 Minutes Window', children=[
#           html.Label('List of Bursting Events ( Select one to view the topic evolution ) '),
#           dcc.Dropdown(
#               id='opt-dropdown_5min',
#               options=[{'label': opt, 'value': opt} for opt in el5]
#           ),
#           dcc.Graph(id='5min1_event'),
#           html.Label('List of Bursting Topics ( Select one to view the keyword evolution ) '),
#           dcc.Dropdown(
#               id='opt-dropdown_5min_topics'
#           ),
#           dcc.Graph(id='5min1_topic')
#       ]),
#       dcc.Tab(label='10 Minutes Window', children=[
#           html.Label('List of Bursting Events ( Select one to view the topic evolution ) '),
#           dcc.Dropdown(
#               id='opt-dropdown_10min',
#               options=[{'label': opt, 'value': opt} for opt in el10]
#           ),
#           dcc.Graph(id='10min1_event'),
#           html.Label('List of Bursting Topics ( Select one to view the keyword evolution ) '),
#           dcc.Dropdown(
#               id='opt-dropdown_10min_topics'
#           ),
#           dcc.Graph(id='10min1_topic')
#       ]),
#       dcc.Tab(label='1 Hour Window', children=[
#           html.Label('List of Bursting Events ( Select one to view the topic evolution) '),
#           dcc.Dropdown(
#               id='opt-dropdown_1hr',
#               options=[{'label': opt, 'value': opt} for opt in el1]
#           ),
#           dcc.Graph(id='1hr1_event'),
#           html.Label('List of Bursting Topics ( Select one to view the keyword evolution) '),
#           dcc.Dropdown(
#               id='opt-dropdown_1hr_topics'
#           ),
#           dcc.Graph(id='1hr1_topic')
#       ]),
#       dcc.Tab(label='4 Hour Window', children=[
#
#           html.Label('List of Bursting Events ( Select one to view the topic evolution) '),
#           dcc.Dropdown(
#               id='opt-dropdown_4hr',
#               options=[{'label': opt, 'value': opt} for opt in el4]
#           ),
#           dcc.Graph( id = '4hr1_event'),
#           html.Label('List of Bursting Topics ( Select one to view the keyword evolution) '),
#           dcc.Dropdown(
#               id='opt-dropdown_4hr_topics'
#           ),
#           dcc.Graph( id = '4hr1_topic')
#
#       ]),
#       dcc.Tab(label='8 Hour Window', children=[
#
#           html.Label('List of Bursting Events ( Select one to view the topic evolution) '),
#           dcc.Dropdown(
#               id='opt-dropdown_8hr',
#               options=[{'label': opt, 'value': opt} for opt in el8]
#           ),
#           dcc.Graph( id = '8hr1_event'),
#           html.Label('List of Bursting Topics ( Select one to view the keyword evolution) '),
#           dcc.Dropdown(
#               id='opt-dropdown_8hr_topics'
#           ),
#           dcc.Graph( id = '8hr1_topic')
#       ])
# ])
# )

layout_page_1 = html.Div([
    html.H2('Geo-Tagging of tweets corresponding to disruptive events for 5 window size'),
    html.H4('Select the events'),
    dcc.Dropdown(
        id='opt-dropdown1',
        options=[{'label': opt, 'value': opt} for opt in el],
        value=['Bush Fire'],
        multi=True
    ),

    dcc.Graph(id='map-disp1', ),
    html.H4('Click on the "VIZ 2" button to proceed to topic modelling visualization'),
    html.Button(dcc.Link('VIZ 2"', href='/page-11')),
])

layout_page_2 = html.Div([
    html.H2('Geo-Tagging of tweets corresponding to disruptive events for 10 Minutes window size'),
    html.H4('Select the events'),
    dcc.Dropdown(
        id='opt-dropdown1',
        options=[{'label': opt, 'value': opt} for opt in el],
        value=['Bush Fire'],
        multi=True
    ),

    dcc.Graph(id='map-disp1', ),
    html.H4('Click on the "VIZ 2" button to proceed to topic modelling visualization'),
    html.Button(dcc.Link('VIZ 2"',  href='/page-22')),
])

layout_page_3 = html.Div([
    html.H2('Geo-Tagging of tweets corresponding to disruptive events for 1 Hour window size'),
    html.H4('Select the events'),
    dcc.Dropdown(
        id='opt-dropdown1',
        options=[{'label': opt, 'value': opt} for opt in el],
        value=['Bush Fire'],
        multi=True
    ),

    dcc.Graph(id='map-disp1', ),
    html.H4('Click on the "VIZ 2" button to proceed to topic modelling visualization'),
    html.Button(dcc.Link('VIZ 2"',  href='/page-33')),
])

layout_page_4 = html.Div([
    html.H2('Geo-Tagging of tweets corresponding to disruptive events for 4 Hours window size'),
    html.H4('Select the events'),
    dcc.Dropdown(
        id='opt-dropdown1',
        options=[{'label': opt, 'value': opt} for opt in el],
        value=['Bush Fire'],
        multi=True
    ),

    dcc.Graph(id='map-disp1', ),
    html.H4('Click on the "VIZ 2" button to proceed to topic modelling visualization'),
    html.Button(dcc.Link('VIZ 2"',  href='/page-44')),
])

layout_page_5 = html.Div([
    html.H2('Geo-Tagging of tweets corresponding to disruptive events for 8 Hours window size'),
    html.H4('Select the events'),
    dcc.Dropdown(
        id='opt-dropdown1',
        options=[{'label': opt, 'value': opt} for opt in el],
        value=['Bush Fire'],
        multi=True
    ),

    dcc.Graph(id='map-disp1', ),
    html.H4('Click on the "VIZ 2" button to proceed to topic modelling visualization'),
    html.Button(dcc.Link('VIZ 2"',  href='/page-55')),
])

#---------------Topic modelling visualization----------------------------------------------
layout_page_11 = html.Div([
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

layout_page_22 = html.Div([
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

layout_page_33 = html.Div([
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

layout_page_44 = html.Div([
    html.H2('Evolution of top bursty topics over the 4 Hours window'),
    html.H4('List of Bursting Events ( Select one to view the topic evolution ) '),
    dcc.Dropdown(
          id='opt-dropdown_4hr',
          options=[{'label': opt, 'value': opt} for opt in el4]
      ),
      dcc.Graph( id = '4hr1_event'),
      html.H4('List of Bursting Topics ( Select one to view the keyword evolution) '),
      dcc.Dropdown(
          id='opt-dropdown_4hr_topics'
      ),
      dcc.Graph( id = '4hr1_topic')
])

layout_page_55 = html.Div([
    html.H2('Evolution of top bursty topics over the 8 Hours window'),
    html.H4('List of Bursting Events ( Select one to view the topic evolution ) '),
    dcc.Dropdown(
          id='opt-dropdown_8hr',
          options=[{'label': opt, 'value': opt} for opt in el8]
      ),
      dcc.Graph( id = '8hr1_event'),
      html.H4('List of Bursting Topics ( Select one to view the keyword evolution) '),
      dcc.Dropdown(
          id='opt-dropdown_8hr_topics'
      ),
      dcc.Graph( id = '8hr1_topic')
])
#---------------------------------------------------------------------------------------------------
layout_start = html.Div([
    html.H2('Page 2'),
    dcc.Dropdown(
        id='page-2-dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='page-2-display-value'),
    html.Br(),
    dcc.Link('Navigate to "/"', href='/'),
    html.Br(),
    dcc.Link('Navigate to "/page-1"', href='/page-1'),
])



def serve_layout():
    if flask.has_request_context():
        return url_bar_and_content_div
    return html.Div([
        url_bar_and_content_div,
        layout_index,
        layout_page_1,
        layout_page_2,
        layout_page_11,
        layout_page_22,
        layout_page_33,
        layout_page_44,
        layout_page_55
    ])


app.layout = serve_layout

#-----------------------MAP VIZ 1 CALLBACKS----------------------------
@app.callback(
   Output('map-disp', 'figure'),
   [Input('opt-dropdown', 'value'),
    Input('year-slider', 'value')] )
def updatefigure(selectedevent, selectedyear):
    traces1 = []
    col = []

    year_data = data[data['Year'] == selectedyear]
    fdata1 = year_data[year_data['Group'].isin(selectedevent)]
    # year_data = data[data['Year'] == selectedyear]
    # print(year_data)

    for l in range(len(fdata1)):
        for k in range(len(rgb)):
            if rgb.iloc[k,1] == fdata1.iloc[l,5]:
                col.append(rgb.iloc[k,0])

    for i in range(len(fdata1)):
        traces1.append(
           go.Scattermapbox(
               lat=[fdata1.iloc[i,6]],
               lon=[fdata1.iloc[i,7]],
               mode='markers',
               marker=go.scattermapbox.Marker(
                   size=14,
                   color= col[i]
               ),
               text=[fdata1.iloc[i,5]]

       ))
    # print(fdata1)
    return {
           'data': traces1,
           'layout': layout_map,
    }


@app.callback(
   Output('map-disp1', 'figure'),
   [Input('opt-dropdown1', 'value')])
def updatefigure(selectedevent):
    traces1 = []
    col = []

    fdata1 = data[data['Group'].isin(selectedevent)]
    # year_data = data[data['Year'] == selectedyear]
    # print(year_data)

    for l in range(len(fdata1)):
        for k in range(len(rgb)):
            if rgb.iloc[k,1] == fdata1.iloc[l,5]:
                col.append(rgb.iloc[k,0])

    for i in range(len(fdata1)):
        traces1.append(
           go.Scattermapbox(
               lat=[fdata1.iloc[i,6]],
               lon=[fdata1.iloc[i,7]],
               mode='markers',
               marker=go.scattermapbox.Marker(
                   size=14,
                   color= col[i]
               ),
               text=[fdata1.iloc[i,5]]

       ))
    # print(fdata1)
    return {
           'data': traces1,
           'layout': layout_map,
    }

@app.callback(
   Output('map-disp2', 'figure'),
   [Input('opt-dropdown2', 'value')])
def updatefigure(selectedevent):
    traces1 = []
    col = []

    fdata1 = data[data['Group'].isin(selectedevent)]
    # year_data = data[data['Year'] == selectedyear]
    # print(year_data)

    for l in range(len(fdata1)):
        for k in range(len(rgb)):
            if rgb.iloc[k,1] == fdata1.iloc[l,5]:
                col.append(rgb.iloc[k,0])

    for i in range(len(fdata1)):
        traces1.append(
           go.Scattermapbox(
               lat=[fdata1.iloc[i,6]],
               lon=[fdata1.iloc[i,7]],
               mode='markers',
               marker=go.scattermapbox.Marker(
                   size=14,
                   color= col[i]
               ),
               text=[fdata1.iloc[i,5]]

       ))
    # print(fdata1)
    return {
           'data': traces1,
           'layout': layout_map,
    }


@app.callback(
   Output('map-disp3', 'figure'),
   [Input('opt-dropdown3', 'value')])
def updatefigure(selectedevent):
    traces1 = []
    col = []

    fdata1 = data[data['Group'].isin(selectedevent)]
    # year_data = data[data['Year'] == selectedyear]
    # print(year_data)

    for l in range(len(fdata1)):
        for k in range(len(rgb)):
            if rgb.iloc[k,1] == fdata1.iloc[l,5]:
                col.append(rgb.iloc[k,0])

    for i in range(len(fdata1)):
        traces1.append(
           go.Scattermapbox(
               lat=[fdata1.iloc[i,6]],
               lon=[fdata1.iloc[i,7]],
               mode='markers',
               marker=go.scattermapbox.Marker(
                   size=14,
                   color= col[i]
               ),
               text=[fdata1.iloc[i,5]]

       ))
    # print(fdata1)
    return {
           'data': traces1,
           'layout': layout_map,
    }
#----------------------------------------------------------------------
# Index callbacks
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/page-1":
        return layout_page_1
    elif pathname == "/page-2":
        return layout_page_2
    elif pathname == "/page-3":
        return layout_page_3
    elif pathname == "/page-4":
        return layout_page_4
    elif pathname == "/page-5":
        return layout_page_5
    elif pathname == "/start":
        return layout_start
    elif pathname == "/page-22":
        return layout_page_22
    elif pathname == "/page-11":
        return layout_page_11
    elif pathname == "/page-33":
        return layout_page_33
    elif pathname == "/page-33":
        return layout_page_33
    elif pathname == "/page-44":
        return layout_page_44
    elif pathname == "/page-55":
        return layout_page_55
    else:
        return layout_index


# Page 1 callbacks
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




# For 4 hours window
#----------------------------------------------------------------------------------------
#Callback for Fig 1 - Evolution of topics in an event
#----------------------------------------------------
@app.callback(
   Output('4hr1_event', 'figure'),
   [Input('opt-dropdown_4hr', 'value')]
)
def update_fig4hr(selectedevent):

    #val = str + "/4hr/events/window_4hr_" +selectedevent + ".csv";

    myTuple = (str11, "/4hr/events/window_4hr_", selectedevent, ".csv")
    x = "".join(myTuple)
    val = x

    topic_list_4hr1 = pd.read_csv(val);
    dd = topic_list_4hr1.drop(columns=['year']);
    traces = [];
    number_of_colors = 20
    for (columnName, columnData) in dd.iteritems():
        traces.append(
            go.Scatter(
                x=[0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4],
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
    dash.dependencies.Output("opt-dropdown_4hr_topics", "options"),
    [dash.dependencies.Input('opt-dropdown_4hr', 'value')],
)
def update_options(selectedevent):
    #val = str + "/4hr/events/window_4hr_" + selected_event + ".csv";

    myTuple = (str11, "/4hr/events/window_4hr_", selectedevent, ".csv")
    x = "".join(myTuple)
    val = x

    dd = pd.read_csv(val);
    dd = dd.drop(columns=['year']);
    top4 = dd;
    top4 = list(top4.columns)
    return [{'label': opt, 'value': opt} for opt in top4]

#Callback for fig 2 - Evolution of keywords in topics
#----------------------------------------------------
@app.callback(
   Output('4hr1_topic', 'figure'),
   [Input('opt-dropdown_4hr_topics', 'value'),
    Input('opt-dropdown_4hr', 'value')]
)
def update_fig4hr_topics(selectedtopic,selectedevent):

    #val = str + "/4hr/topics/window_4hr_" + selectedevent + "_" + selectedtopic + ".csv";

    myTuple = (str11, "/4hr/topics/window_4hr_", selectedevent, "_", selectedtopic, ".csv")
    x = "".join(myTuple)
    val = x

    topic_list_4hr1 = pd.read_csv(val);
    dd = topic_list_4hr1.drop(columns=['year']);
    traces = [];
    number_of_colors = 20
    for (columnName, columnData) in dd.iteritems():
        traces.append(
            go.Bar(
                x=[0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4],
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



# For 8 hours window
#----------------------------------------------------------------------------------------
#Callback for Fig 1 - Evolution of topics in an event
#----------------------------------------------------
@app.callback(
   Output('8hr1_event', 'figure'),
   [Input('opt-dropdown_8hr', 'value')]
)
def update_fig8hr(selectedevent):

    #val = str + "/8hr/events/window_8hr_" +selectedevent + ".csv";

    myTuple = (str11, "/8hr/events/window_8hr_", selectedevent, ".csv")
    x = "".join(myTuple)
    val = x

    topic_list_8hr1 = pd.read_csv(val);
    dd = topic_list_8hr1.drop(columns=['year']);
    traces = [];
    number_of_colors = 20
    for (columnName, columnData) in dd.iteritems():
        traces.append(
            go.Scatter(
                x=[0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8],
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
    dash.dependencies.Output("opt-dropdown_8hr_topics", "options"),
    [dash.dependencies.Input('opt-dropdown_8hr', 'value')],
)
def update_options(selectedevent):
    #val = str + "/8hr/events/window_8hr_" + selected_event + ".csv";

    myTuple = (str11, "/8hr/events/window_8hr_", selectedevent, ".csv")
    x = "".join(myTuple)
    val = x

    dd = pd.read_csv(val);
    dd = dd.drop(columns=['year']);
    top8 = dd;
    top8 = list(top8.columns)
    return [{'label': opt, 'value': opt} for opt in top8]

#Callback for fig 2 - Evolution of keywords in topics
#----------------------------------------------------
@app.callback(
   Output('8hr1_topic', 'figure'),
   [Input('opt-dropdown_8hr_topics', 'value'),
    Input('opt-dropdown_8hr', 'value')]
)
def update_fig8hr_topics(selectedtopic,selectedevent):

    #val = str + "/8hr/topics/window_8hr_" + selectedevent + "_" + selectedtopic + ".csv";

    myTuple = (str11, "/8hr/topics/window_8hr_", selectedevent, "_", selectedtopic, ".csv")
    x = "".join(myTuple)
    val = x

    topic_list_8hr1 = pd.read_csv(val);
    dd = topic_list_8hr1.drop(columns=['year']);
    traces = [];
    number_of_colors = 20
    for (columnName, columnData) in dd.iteritems():
        traces.append(
            go.Bar(
                x=[0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8],
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


# Page 2 callbacks
@app.callback(Output('page-2-display-value', 'children'),
              [Input('page-2-dropdown', 'value')])
def display_value(value):
    print('display_value')
    return 'You have selected "{}"'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True,dev_tools_ui=False, dev_tools_props_check=False)