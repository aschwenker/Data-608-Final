# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 19:53:49 2019

@author: ASchwenker
"""

import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/aschwenker/Data-608-Final/master/Data/School%20Districts_GeoJason.json') as response:
    counties = json.load(response)
df = pd.read_csv('https://raw.githubusercontent.com/aschwenker/Data-608-Final/master/Data/Safe_Routes_to_Schools_-_Priority_Schools.csv')
site_lat = df.Latitude
print(site_lat)
site_lon = df.Longitude
locations_name = df['School Name / ID']
print(locations_name)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

print(df.groupby('Borough').count()[['School Name / ID']])
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

data = [go.Scattermapbox(lat=df['Latitude'], lon=df['Longitude'], mode='markers', marker=dict(size=10),
text=df['School Name / ID'])]

fig_layout = go.Layout(autosize=True, hovermode='closest', mapbox=dict(
        style= "stamen-terrain",
        center= dict( lon= -74, lat= 40.75),
        zoom= 9.25,
        layers=[dict(
            source = counties,
            type = 'fill',below = 'traces', color =  'pink')]))
fig = dict(data=data, layout=fig_layout)




app.layout = html.Div([
    html.H1('Dash Tabs component demo'),
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Tab One', value='tab-1-example'),
        dcc.Tab(label='Tab Two', value='tab-2-example'),
    ]),
    html.Div(id='tabs-content-example')
])


@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return html.Div([
            html.H3('Tab content 1'),
            dcc.Graph(id='map', figure=fig)
            ])
    elif tab == 'tab-2-example':
        return html.Div([
            html.H3('Tab content 2'),
            dcc.Graph(
                id='graph',
                figure = {'data': [{
                        'x': ['Bronx', 'Manhattan','Queens','Staten Island'],
                        'y': [25, 46, 23,33,8],
                        'type': 'bar'
                    }]
                })
        ])


if __name__ == '__main__':
    app.run_server(debug=False)