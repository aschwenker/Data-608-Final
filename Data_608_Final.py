# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 11:50:55 2019

@author: ASchwenker
"""
from plotly.offline import plot
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
from urllib.request import urlopen
import json
import plotly.graph_objects as go

with urlopen('https://raw.githubusercontent.com/aschwenker/Data-608-Final/master/Data/School%20Districts_GeoJason.json') as response:
    counties = json.load(response)
All_SChool_URL = 'https://data.cityofnewyork.us/resource/9ck8-hj3u.json'
mapbox_access_token = 'pk.eyJ1IjoiYXNjaHdlbmtlcjY2OTAiLCJhIjoiY2szZDhybTFtMHVoMTNjcGk4MnozZDlmZyJ9.5dVGGTKgF6B8O9YlWjuXTw'

df = pd.read_csv('https://raw.githubusercontent.com/aschwenker/Data-608-Final/master/Data/Safe_Routes_to_Schools_-_Priority_Schools.csv')
site_lat = df.Latitude
print(site_lat)
site_lon = df.Longitude
locations_name = df['School Name / ID']
print(locations_name)
fig = go.Figure()

fig.add_trace(go.Scattermapbox(
        lat=site_lat,
        lon=site_lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=10,
            color='rgb(255, 0, 0)',
            opacity=0.7
        ),
        text=locations_name
    ))

fig.add_trace(go.Scattermapbox(
        lat=site_lat,
        lon=site_lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=8,
            color='rgb(242, 177, 172)',
            opacity=0.9
        ),
        text=locations_name
    ))
fig.update_layout(
        title='Safe Route Schools',
        autosize=True,
        hovermode='closest',
        showlegend=False,
mapbox = {
        'style': "stamen-terrain",
        'center': { 'lon': -74, 'lat': 40.75},
        'zoom': 9.25, 'layers': [{
            'source': counties,
            'type': "fill", 'below': "traces", 'color': "royalblue"}]},
    margin = {'l':0, 'r':0, 'b':0, 't':0})
       

plot(fig)


