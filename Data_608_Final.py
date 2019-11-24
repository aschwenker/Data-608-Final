# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 11:50:55 2019

@author: ASchwenker
"""
from plotly.offline import plot

import plotly.graph_objects as go
import pandas as pd

mapbox_access_token = 'pk.eyJ1IjoiYXNjaHdlbmtlcjY2OTAiLCJhIjoiY2szZDhybTFtMHVoMTNjcGk4MnozZDlmZyJ9.5dVGGTKgF6B8O9YlWjuXTw'

df = pd.read_csv('https://raw.githubusercontent.com/aschwenker/Data-608-Final/master/Safe_Routes_to_Schools_-_Priority_Schools.csv')
site_lat = df.Latitude
site_lon = df.Longitude
locations_name = df['School Name / ID']

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
        text=locations_name,
        hoverinfo='text'
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
        hoverinfo='none'
    ))

fig.update_layout(
    title='Safe Route Schools',
    autosize=True,
    hovermode='closest',
    showlegend=False,
    mapbox=go.layout.Mapbox(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=40.75,
            lon=-74
        ),
        pitch=0,
        zoom=9.25,
        style='light'
    ),
)

plot(fig)