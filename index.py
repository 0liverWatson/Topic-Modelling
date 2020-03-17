import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import urllib.parse as urlparse
from urllib.parse import parse_qs

from app import app
import vis_map, vis_topic
import glob
import os
import sys
import subprocess


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])


index_page = html.Div([
     html.H3('Start Page'),
     html.Br(),
     html.H2('Real-time topic modelling of Disruptive Events from twitter and their Visualization'),
     html.H6("""This application shows the geo location of live streaming of disruptive tweets corresponding to disruptive events of United Kingdom. 
               Furthermore, for each event, we can visualize the top ten bursting topics over a window of 5min, 10 min, 1ht, 4hr and 8hr along
                    with the important kewqords associated to each topic of each event with its contribution score to the bursting topic."""),
     html.H3("Instructions to run the application"),
     html.H6("- Click on the START button to start the application"),
     html.H6("- Click on the buttons of respective time windows for display of tweets on geomap for disruptive events, once they turn green"),
     html.Button('STARTPROG',id='start_prog'),
     html.Br(),
     html.Br(),
     html.Button(dcc.Link('Show Data', href='/vis_map'),id='button-next-actual',hidden='hidden'),
     html.Button('Show Data', id='button-next',hidden=False, disabled=True), 
     dcc.Interval(
            id='interval-check',
            interval=5*1000, # in milliseconds
            n_intervals=0
        ),
    html.Div(id='output')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/vis_map':
        return vis_map.layout()
    # elif pathname.startswith('/vis_topic'):
    #     parsed = urlparse.urlparse(pathname)
    #     print(pathname)
    #     print(parsed)
    #     return vis_topic.layout(parse_qs(parsed.query)['win'])
    elif pathname == '/page-1':
        return vis_topic.layout_page1()
    elif pathname == '/page-2':
        return vis_topic.layout_page2
    elif pathname == '/page-3':
        return vis_topic.layout_page3
    else:
        return index_page

@app.callback(Output('button-next-actual', 'hidden'),
              [Input('interval-check', 'n_intervals')])
def update_metrics(n):
    flag = 'hidden'
    
    list_of_files = glob.glob('data/events/*.json')
    if len(list_of_files)>0:
        flag = False
    
    return flag

@app.callback(Output('button-next', 'hidden'),
              [Input('interval-check', 'n_intervals')])
def update_metrics(n):
    flag = False
    
    list_of_files = glob.glob('data/events/*.json')
    if len(list_of_files)>0:
        flag = 'hidden'
    
    return flag
    


@app.callback(
    Output('output', 'children'),
    [Input('start_prog', 'n_clicks')])
def clicks(n_clicks):
    if n_clicks:
        # subprocess.call("python backend/Main.py",)
        
        if n_clicks == 1:
            subprocess.Popen([sys.executable, 'backend/Main.py'], creationflags = subprocess.CREATE_NEW_CONSOLE)
        return 'Application started to collect tweets'

if __name__ == '__main__':
    app.run_server(debug=True)