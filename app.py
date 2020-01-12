import dash
import dash_core_components
import dash_core_components as dcc
import dash_html_components
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import random

#Data Pre-processing
#from dash_core_components import Input
#from dash_html_components import Output
from dash.dependencies import Input, Output

data = pd.read_csv('C:/Users\Rohan Das\Documents\Rohan_Docs\Study\Semester 3\Kmd_project\Data\Topic-Modelling-master/data.csv')
event_list = data.Group.unique()
el = event_list.tolist()
#-------------------------------------------
fdata = data[data.Group == 'Bush Fire']

traces = []
rgb = pd.DataFrame()
temp = []
#----------------Color-----------------------
# for j in range(len(event_list)):
#         temp.append(random.randint(0, 255))
#
# rgb['Color'] = temp
# rgb['Group'] = el

color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(len(event_list))]
rgb['Color'] = color
rgb['Group'] = el
# print(rgb)

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
    # legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview",
    showlegend = False,
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(lon=-55.3781, lat=3.4360),
        zoom=2,
    ),
    transition={'duration': 500},
)


app.layout = html.Div(children=[
    html.H1(children='Event Visualization'),

    dcc.Graph(id='map-disp',
              figure={
                  'data': traces,
                  'layout': layout
              }
    ),

    # html.Label('Select the Window size'),
    # dcc.RadioItems(
    #     options=[
    #         {'label': '5 Minutes', 'value': '5min'},
    #         {'label': '10 Minutes', 'value': '10min'},
    #         {'label': '1 Hour', 'value': '1hr'},
    #         {'label': '4 Hours', 'value': '4hr'},
    #         {'label': '8 Hours', 'value': '8hr'}
    #     ],
    #     value='5min'
    # ),

    html.Label('Select the events to be '),
        dcc.Dropdown(
            id='opt-dropdown',
            options=[{'label': opt, 'value': opt} for opt in el],
            value=['Bush Fire'],
            multi=True
        ),

])

@app.callback(
   Output('map-disp', 'figure'),
   [Input('opt-dropdown', 'value')] )
def updatefigure(selectedevent):
    traces1 = []
    col = []
    # fdata1.append(data[data['Group'] == selectedevent.values[0]])
    # for j in range(len(selectedevent)):
    #     ev = selectedevent[j]
    #     fdata1= data[data.Group == ev]
    #     print(selectedevent[j])

    fdata1 = data[data['Group'].isin(selectedevent)]
    for l in range(len(fdata1)):
        for k in range(len(rgb)):
            if rgb.iloc[k,1] == fdata1.iloc[l,5]:
                col.append(rgb.iloc[k,0])
    # print(col)

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
           'layout': layout,
    }


if __name__ == '__main__':
    app.run_server(debug=True)
