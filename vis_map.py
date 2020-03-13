import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import random
from app import app

import time 


time.sleep(100)
print("asd")
#---------------------------------------------------------------------------------------
#---------------Viz 1 - Map part----------------------------

#Data Pre-processing
data = pd.read_csv('DS/data.csv')
event_list = data.Group.unique()
el = event_list.tolist()
fdata = data[data.Group == 'Bush Fire']
rgb = pd.DataFrame()

#----------------Color-----------------------

color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(len(event_list))])
             for i in range(len(event_list))]
rgb['Color'] = color
rgb['Group'] = el

layout = html.Div([
    html.H3('Map Page'),
    dcc.Dropdown(
        id='app-1-dropdown',
        options=[
            {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
                'NYC', 'MTL', 'LA'
            ]
        ]
    ),
    html.Div(id='app-1-display-value'),
    dcc.Link('Go to Topic', href='/vis_topic')
])


@app.callback(
    Output('app-1-display-value', 'children'),
    [Input('app-1-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)