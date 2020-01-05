import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

#Data Pre-processing
data = pd.read_csv("C:/Users/Subhashree/Documents/data.csv")
event_list = data.Group.unique()
el = event_list.tolist()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Create global chart template
mapbox_access_token = "pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w"

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview",
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(lon=-78.05, lat=42.54),
        zoom=7,
    ),
)

app.layout = html.Div(children=[
    html.H1(children='Event Visualization'),

    #html.Div(children='''
     #   Dash: A web application framework for Python.
    #'''),

    html.Label('Select the Window size'),
        dcc.RadioItems(
            options=[
                {'label': '5 Minutes',  'value': '5min'},
                {'label': '10 Minutes', 'value': '10min'},
                {'label': '1 Hour',     'value': '1hr'},
                {'label': '4 Hours',    'value': '4hr'},
                {'label': '8 Hours',    'value': '8hr'}
            ],
            value='5min'
    ),

    html.Label('Select the events to be '),
        dcc.Dropdown(
            id='opt-dropdown',
            options=[{'label': opt, 'value': opt} for opt in el],
            multi=True
        ),


    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
