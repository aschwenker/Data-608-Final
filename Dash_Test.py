# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 21:24:19 2019

@author: ASchwenker
"""

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
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

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
data = [go.Scattermapbox(lat=df['Latitude'], lon=df['Longitude'], mode='markers', marker=dict(size=10),
text=df['School Name / ID'])]

layout = go.Layout(autosize=True, hovermode='closest', mapbox=dict(
        style= "stamen-terrain",
        center= dict( lon= -74, lat= 40.75),
        zoom= 9.25))
fig = dict(data=data, layout=layout)

app.layout = html.Div([
dcc.Graph(id='graph', figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=False)