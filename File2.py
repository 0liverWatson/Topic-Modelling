import dash
import dash_core_components
import dash_core_components as dcc
import dash_html_components
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go

#Data Pre-processing
#from dash_core_components import Input
#from dash_html_components import Output
from dash.dependencies import Input, Output

data = pd.read_csv("C:/Users/Subhashree/Documents/data.csv")
event_list = data.Group.unique()
el = event_list.tolist()
#--------------------------------
fdata = data[data.Group == 'Bush Fire']
traces = []
for i in range(len(fdata)):
        traces.append(
            go.Scattermapbox(
                lat=[fdata.iloc[i,6]],
                lon=[fdata.iloc[i,7]],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=14
                ),
                text=[fdata.iloc[i,4]]
            )
        )
#--------------------------------


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
    #legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview",
    showlegend = False,
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(lon=-55.3781, lat=3.4360),
        zoom=1,
    ),
)


app.layout = html.Div(children=[
    html.H1(children='Event Visualization'),

    html.Label('Select the Window size'),
    dcc.RadioItems(
        options=[
            {'label': '5 Minutes', 'value': '5min'},
            {'label': '10 Minutes', 'value': '10min'},
            {'label': '1 Hour', 'value': '1hr'},
            {'label': '4 Hours', 'value': '4hr'},
            {'label': '8 Hours', 'value': '8hr'}
        ],
        value='5min'
    ),

    html.Label('Select the events to be '),
        dcc.Dropdown(
            id='opt-dropdown',
            options=[{'label': opt, 'value': opt} for opt in el]
        ),


    dcc.Graph(id='map-disp',
              figure = {
                  'data': traces,
#                      [
#
#                        go.Scattermapbox(
#                           lat=['45.5017'],
#                           lon=['-73.5673'],
#                           mode='markers',
#                           marker=go.scattermapbox.Marker(size=14),
#                           text=['Montreal'],
#                        )
#                     ],
                  'layout':layout
                           }
    )

])

#@app.callback(
#    Output('map-disp', 'figure'),
#    [Input('opt-dropdown', 'value')] )
#def updateMap(selectedevent):
#    fdata = data[data.Group == selectedevent]
#    traces = []
#    for i in range(len(fdata)):
#        traces.append(
#            go.Scattermapbox(
#                lat=[fdata.iloc[i,6]],
#                lon=[fdata.iloc[i,7]],
#                mode='markers',
#                marker=go.scattermapbox.Marker(
#                    size=14
#                ),
#                text=[fdata.iloc[i,5]]

#        ))

#        return {
#            'data': [
#
#                     go.Scattermapbox(
#                           lat=['45.5017'],
#                           lon=['-73.5673'],
#                           mode='markers',
#                           marker=go.scattermapbox.Marker(size=14),
#                           text=['Montreal'],)
#                     ],
#            'layout': layout,
#        }


if __name__ == '__main__':
    app.run_server(debug=True)
