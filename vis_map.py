import dash
import dash_core_components
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import random
from datetime import datetime
from dash.dependencies import Input, Output
from app import app

import glob
import os

import time
import json

# 5 min window
list_of_files_5 = glob.glob('data/events/5_*.json') # * means all if need specific format then *.csv

rgb_5 = pd.DataFrame()
el_5 = []
color_5 = []
data_5 = []

if(len(list_of_files_5)>0):
    latest_file_5 = max(list_of_files_5, key=os.path.getctime)
    # print(latest_file)
    # data = pd.read_csv(latest_file_5)

    with open(latest_file_5) as json_file:
        json_str = json.load(json_file)
    data_5 = json.loads(json_str)

    # event_list = data.Group.unique()
    el_5 = [e['event_name'] for e in data_5]

    color_5 = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(el_5))]
    
    rgb_5['Color'] = color_5
    rgb_5['Group'] = el_5

# # print(el)
# fdata = data[data.Group == el[0]]
# rgb = pd.DataFrame()
# reload_count = 0


# 10 min window
list_of_files_10 = glob.glob('data/events/10_*.json') # * means all if need specific format then *.csv
rgb_10 = pd.DataFrame()
el_10 = []
color_10 = []
data_10 = []
if(len(list_of_files_10)>0):
    latest_file_10 = max(list_of_files_10, key=os.path.getctime)
    # print(latest_file)
    # data = pd.read_csv(latest_file_5)

    with open(latest_file_10) as json_file:
        json_str = json.load(json_file)
    data_10 = json.loads(json_str)

    # event_list = data.Group.unique()
    el_10 = [e['event_name'] for e in data_10]

    color_10 = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(el_10))]
    
    rgb_10['Color'] = color_10
    rgb_10['Group'] = el_10


# 60 min window
list_of_files_60 = glob.glob('data/events/60_*.json') # * means all if need specific format then *.csv
rgb_60 = pd.DataFrame()
el_60 = []
color_60 = []
data_60 = []
if(len(list_of_files_10)>0):
    latest_file_60 = max(list_of_files_60, key=os.path.getctime)
    # print(latest_file)
    # data = pd.read_csv(latest_file_5)

    with open(latest_file_60) as json_file:
        json_str = json.load(json_file)
    data_60 = json.loads(json_str)

    # event_list = data.Group.unique()
    el_60 = [e['event_name'] for e in data_60]

    color_60 = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(el_60))]
    
    rgb_60['Color'] = color_60
    rgb_60['Group'] = el_60

##Data Pre-processing

# list_of_files = glob.glob('data/events/*') # * means all if need specific format then *.csv
# latest_file = max(list_of_files, key=os.path.getctime)
# print(latest_file)
# data = pd.read_csv(latest_file)
# event_list = data.Group.unique()
# el = event_list.tolist()
# print(el)
# fdata = data[data.Group == el[0]]
# rgb = pd.DataFrame()
# reload_count = 0

#-------------Lat Long-----------------------
# data[['Lat','Lon']] = data.Coordinates.str.split(",",expand=True)
# data['Lat'] = data['Lat'].str.strip('[')
# data['Lon'] = data['Lat'].str.strip(']')
# print(data)

#----------------Color-----------------------

# color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(len(event_list))])
#              for i in range(len(event_list))]
# rgb['Color'] = color
# rgb['Group'] = el

#----------------------------------------------

mapbox_access_token = "pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w"
latt = 50.98599
lonn = -3.148037
layoutmap = dict(
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
        center=dict(lon=lonn, lat=latt),
        zoom=4,
    )
)

def layout():

    # 5 min window
    list_of_files_5 = glob.glob('data/events/5_*.json') # * means all if need specific format then *.csv
    
    rgb_5 = pd.DataFrame()
    el_5 = []
    color_5 = []
    data_5 = []
    

    if(len(list_of_files_5)>0):
        latest_file_5 = max(list_of_files_5, key=os.path.getctime)
        # print(latest_file)
        # data = pd.read_csv(latest_file_5)

        with open(latest_file_5) as json_file:
            json_str = json.load(json_file)
        data_5 = json.loads(json_str)

        # event_list = data.Group.unique()
        el_5 = [e['event_name'] for e in data_5]

        color_5 = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(el_5))]
        
        rgb_5['Color'] = color_5
        rgb_5['Group'] = el_5

    # # print(el)
    # fdata = data[data.Group == el[0]]
    # rgb = pd.DataFrame()
    # reload_count = 0


    # 10 min window
    list_of_files_10 = glob.glob('data/events/10_*.json') # * means all if need specific format then *.csv
    rgb_10 = pd.DataFrame()
    el_10 = []
    color_10 = []
    data_10 = []
    
    

    if(len(list_of_files_10)>0):
        latest_file_10 = max(list_of_files_10, key=os.path.getctime)
        # print(latest_file)
        # data = pd.read_csv(latest_file_5)

        with open(latest_file_10) as json_file:
            json_str = json.load(json_file)
        data_10 = json.loads(json_str)

        # event_list = data.Group.unique()
        el_10 = [e['event_name'] for e in data_10]

        color_10 = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(el_10))]
        
        rgb_10['Color'] = color_10
        rgb_10['Group'] = el_10


    # 60 min window
    list_of_files_60 = glob.glob('data/events/60_*.json') # * means all if need specific format then *.csv
    rgb_60 = pd.DataFrame()
    el_60 = []
    color_60 = []
    data_60 = []
    
    
    if(len(list_of_files_10)>0):
        latest_file_60 = max(list_of_files_60, key=os.path.getctime)
        # print(latest_file)
        # data = pd.read_csv(latest_file_5)

        with open(latest_file_60) as json_file:
            json_str = json.load(json_file)
        data_60 = json.loads(json_str)

        # event_list = data.Group.unique()
        el_60 = [e['event_name'] for e in data_60]

        color_60 = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(el_60))]
        
        rgb_60['Color'] = color_60
        rgb_60['Group'] = el_60

    # # print(el)
    # fdata = data[data.Group == el[0]]
    # rgb = pd.DataFrame()
    # reload_count = 0

    

    return html.Div([
    dcc.Tabs([
        dcc.Tab(
            label='5 Minutes Window', children=[
            html.H1(children='Event Visualization'),

            html.Label('Select the events to be '),
            dcc.Dropdown(
                id='opt-dropdown',
                options=[{'label': opt, 'value': opt} for opt in el_5],
                value=[],
                multi=True
            ),
            html.Button(dcc.Link('Refresh', href='/vis_map')),
            dcc.Graph(id='map-disp',),
            html.Button(dcc.Link('Click for topic visualization for 5 Min window',  href='/page-1', className='b1')),
        ]),
        dcc.Tab(
            label='10 Minutes Window', children=[
            html.H1(children='Event Visualization'),

            html.Label('Select the events to be '),
            dcc.Dropdown(
                id='opt-dropdown1',
                options=[{'label': opt, 'value': opt} for opt in el_10],
                value=[],
                multi=True
            ),
            html.Button(dcc.Link('Refresh', href='/vis_map')),
            dcc.Graph(id='map-disp1',),
            html.Button(dcc.Link('Click for topic visualization for 10 Min window"', href='/page-2', className='b1')),
        ]),
        dcc.Tab(
            label='1 Hour Window', children=[
            html.H1(children='Event Visualization'),

            html.Label('Select the events to be '),
            dcc.Dropdown(
                id='opt-dropdown2',
                options=[{'label': opt, 'value': opt} for opt in el_60],
                value=[],
                multi=True
            ),
            html.Button(dcc.Link('Refresh', href='/vis_map')),
            dcc.Graph(id='map-disp2',),
            html.Button(dcc.Link('Click for topic visualization for 1 Hour window',     href='/page-3', className='b1')),
        ])
    ]),
    dcc.Interval(
            id='interval-component',
            interval=30*1000, # in milliseconds
            n_intervals=0
        ),
    dbc.Toast(
            "This toast is placed in the top right ",
            id="positioned-toast",
            header="Positioned toast",
            is_open=False,
            dismissable=True,
            icon="danger",
            # top: 66 positions the toast below the navbar
            style={"position": "fixed", "top": 66, "right": 10, "width": 350},
        )]
)

@app.callback(
    Output('opt-dropdown', 'disabled'),
    [Input('opt-dropdown', 'value')]
    # [dash.dependencies.State('ref', 'n_clicks')]
)
def disable_dropdown_one(val1):

    if len(val1) > 4:
        return True
    else:
        return False

@app.callback(
    Output('opt-dropdown1', 'disabled'),
    [Input('opt-dropdown1', 'value')]
)
def disable_dropdown_one(val1):

    if len(val1) > 4:
        return True
    else:
        return False

@app.callback(
    Output('opt-dropdown2', 'disabled'),
    [Input('opt-dropdown2', 'value')]
)
def disable_dropdown_one(val1):

    if len(val1) > 4:
        return True
    else:
        return False


@app.callback(
   Output('map-disp', 'figure'),
   [Input('opt-dropdown', 'value')])
def updatefigure(selectedevent):
    traces1 = []
    col = []
    
    # fdata_5 = pd.concat([pd.read_json(e['data']) for e in data_5 if e['event_name'] in selectedevent])
    # fdata1 = data_5[data_5['Group'].isin(selectedevent)]
    # year_data = data[data['Year'] == selectedyear]
    # print(year_data)

    # for l in range(len(fdata1)):
    #     for k in range(len(rgb_5)):
    #         if rgb_5.iloc[k,1] == fdata1.iloc[l,5]:
    #             col.append(rgb_5.iloc[k,0])

    # for i in range(len(fdata1)):
    #     traces1.append(
    #        go.Scattermapbox(
    #            lat=[fdata1.iloc[i,6]],
    #            lon=[fdata1.iloc[i,7]],
    #            mode='markers',
    #            marker=go.scattermapbox.Marker(
    #                size=14,
    #                color= col[i]
    #            ),
    #            text=[fdata1.iloc[i,5]]

    #    ))
    # # print(fdata1)

    for event in data_5:
        ename = event['event_name']

        if(ename in selectedevent):
            c  = rgb_5[rgb_5['Group']==ename].Color[0]    
            df = pd.read_json(event['data'])
            df[['Lon','Lat']] = df.Coordinates.str.split(",",expand=True)
            df['Lat'] = df['Lat'].str.strip(']')
            df['Lon'] = df['Lon'].str.strip('[')
            for index, row in df.iterrows():
                traces1.append(
                    go.Scattermapbox(
                        lat=[str(float(row.Lat))],
                        lon=[str(float(row.Lon))],
                        mode='markers',
                        marker=go.scattermapbox.Marker(
                            size=14,
                            color= c
                        ),
                        text=[ename]

                ))

    return {
           'data': traces1,
           'layout': layoutmap,
    }

@app.callback(
   Output('map-disp1', 'figure'),
   [Input('opt-dropdown1', 'value')])
def updatefigure(selectedevent):
    traces1 = []
    col = []

    # fdata1 = pd.concat([pd.read_json(e['data']) for e in data_5 if e['event_name'] in selectedevent])
    # fdata1 = data[data['Group'].isin(selectedevent)]
    # year_data = data[data['Year'] == selectedyear]
    # print(year_data)

    # for l in range(len(fdata1)):
    #     for k in range(len(rgb)):
    #         if rgb.iloc[k,1] == fdata1.iloc[l,5]:
    #             col.append(rgb.iloc[k,0])

    # for i in range(len(fdata1)):
    #     traces1.append(
    #        go.Scattermapbox(
    #            lat=[fdata1.iloc[i,6]],
    #            lon=[fdata1.iloc[i,7]],
    #            mode='markers',
    #            marker=go.scattermapbox.Marker(
    #                size=14,
    #                color= col[i]
    #            ),
    #            text=[fdata1.iloc[i,5]]

    #    ))
    # print(fdata1)

    for event in data_10:
        ename = event['event_name']

        if(ename in selectedevent):
            c  = rgb_10[rgb_10['Group']==ename].Color[0]    
            df = pd.read_json(event['data'])
            df[['Lon','Lat']] = df.Coordinates.str.split(",",expand=True)
            df['Lat'] = df['Lat'].str.strip('[')
            df['Lon'] = df['Lon'].str.strip(']')
            for index, row in df.iterrows():
                traces1.append(
                    go.Scattermapbox(
                        lat=[row.Lat],
                        lon=[row.Lon],
                        mode='markers',
                        marker=go.scattermapbox.Marker(
                            size=14,
                            color= c
                        ),
                        text=[ename]

                ))
    return {
           'data': traces1,
           'layout': layoutmap,
    }

@app.callback(
   Output('map-disp2', 'figure'),
   [Input('opt-dropdown2', 'value')])
def updatefigure(selectedevent):
    traces1 = []
    col = []

    # fdata1 = data[data['Group'].isin(selectedevent)]
    # year_data = data[data['Year'] == selectedyear]
    # print(year_data)

    # for l in range(len(fdata1)):
    #     for k in range(len(rgb)):
    #         if rgb.iloc[k,1] == fdata1.iloc[l,5]:
    #             col.append(rgb.iloc[k,0])

    # for i in range(len(fdata1)):
    #     traces1.append(
    #        go.Scattermapbox(
    #            lat=[fdata1.iloc[i,6]],
    #            lon=[fdata1.iloc[i,7]],
    #            mode='markers',
    #            marker=go.scattermapbox.Marker(
    #                size=14,
    #                color= col[i]
    #            ),
    #            text=[fdata1.iloc[i,5]]

    #    ))

    for event in data_60:
        ename = event['event_name']

        if(ename in selectedevent):
            c  = rgb_60[rgb_60['Group']==ename].Color[0]    
            df = pd.read_json(event['data'])
            df[['Lon','Lat']] = df.Coordinates.str.split(",",expand=True)
            df['Lat'] = df['Lat'].str.strip('[')
            df['Lon'] = df['Lon'].str.strip(']')
            for index, row in df.iterrows():
                traces1.append(
                    go.Scattermapbox(
                        lat=[row.Lat],
                        lon=[row.Lon],
                        mode='markers',
                        marker=go.scattermapbox.Marker(
                            size=14,
                            color= c
                        ),
                        text=[ename]

                ))
    # print(fdata1)
    return {
           'data': traces1,
           'layout': layoutmap,
    }


# @app.callback(
#    Output('map-disp3', 'figure'),
#    [Input('opt-dropdown3', 'value')])
# def updatefigure(selectedevent):
#     traces1 = []
#     col = []

#     fdata1 = data[data['Group'].isin(selectedevent)]
#     # year_data = data[data['Year'] == selectedyear]
#     # print(year_data)

#     for l in range(len(fdata1)):
#         for k in range(len(rgb)):
#             if rgb.iloc[k,1] == fdata1.iloc[l,5]:
#                 col.append(rgb.iloc[k,0])

#     for i in range(len(fdata1)):
#         traces1.append(
#            go.Scattermapbox(
#                lat=[fdata1.iloc[i,6]],
#                lon=[fdata1.iloc[i,7]],
#                mode='markers',
#                marker=go.scattermapbox.Marker(
#                    size=14,
#                    color= col[i]
#                ),
#                text=[fdata1.iloc[i,5]]

#        ))
#     # print(fdata1)
#     return {
#            'data': traces1,
#            'layout': layoutmap,
#     }


@app.callback(Output('positioned-toast', 'is_open'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    # print('opening toast',n )
    # global reload_count
    # reload_count +=1
    return True
