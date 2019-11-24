# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 11:50:55 2019

@author: ASchwenker
"""
from plotly.offline import plot

import plotly.graph_objects as go
import pandas as pd

mapbox_access_token = 'pk.eyJ1IjoiYXNjaHdlbmtlcjY2OTAiLCJhIjoiY2szZDhybTFtMHVoMTNjcGk4MnozZDlmZyJ9.5dVGGTKgF6B8O9YlWjuXTw'
GEoJsonURL = pd.read_json('C:/Users/aschwenker/Documents/MA/Data-608-Final/Data/School Districts.geojson')
print(GEoJsonURL)

df = pd.read_csv('https://raw.githubusercontent.com/aschwenker/Data-608-Final/master/New%20folder%20(2)/Safe_Routes_to_Schools_-_Priority_Schools.csv')
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
            opacity=0.7
        ),
        text=locations_name
    ))
fig.update_layout(
mapbox = {
        'style': "stamen-terrain",
        'center': { 'lon': -74, 'lat': 40.75},
        'zoom': 9.25, 'layers': [{
            'source': GEoJsonURL,
            'type': "fill", 'below': "traces", 'color': "royalblue"}]},
    margin = {'l':0, 'r':0, 'b':0, 't':0})
       




plot(fig)


