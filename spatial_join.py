# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 21:19:53 2019

@author: ASchwenker
"""
from plotly.offline import plot
import pandas as pd
import geopandas
import geopandas.tools
from shapely.geometry import Point
from urllib.request import urlopen
import json
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
from urllib.request import urlopen
import json
import geopandas
import geopandas.tools
from shapely.geometry import Point

accidents = pd.read_csv('https://raw.githubusercontent.com/aschwenker/Data-608-Final/master/Data/accidents_2018_2019.csv')
df = pd.read_csv('https://raw.githubusercontent.com/aschwenker/Data-608-Final/master/Data/Safe_Routes_to_Schools_-_Priority_Schools.csv')
with urlopen('https://raw.githubusercontent.com/aschwenker/Data-608-Final/master/Data/School%20Districts_GeoJason.json') as response:
    counties = json.load(response)
districts=geopandas.read_file('https://raw.githubusercontent.com/aschwenker/Data-608-Final/master/Data/School%20Districts_GeoJason.json')

df["geometry"] = df.apply(lambda row: Point(row["Longitude"], row["Latitude"]), axis=1)
del(df["Latitude"], df["Longitude"])

points = geopandas.GeoDataFrame(df, geometry="geometry")

points.crs = districts.crs
result = geopandas.tools.sjoin(points, districts, how="left")
print(result.index_right.head())
print(list(result))
counties_list = counties['features']
print(counties_list)
counties_list = [dict(item, **{'id':item['properties']['school_dist']}) for item in counties_list]
counties['features']=counties_list
result_counts = result.groupby('school_dist').count()['School Name / ID']
 
result_counts.to_frame()
result_counts = result_counts.reset_index()
result_counts.rename(columns = {'School Name / ID':'result_Counts'}, inplace = True)
print(list(result_counts))
print(result_counts)

fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=result_counts.school_dist, z=result_counts.result_Counts,
                                    colorscale="Viridis", zmin=0, zmax=11,
                                    marker_opacity=0.5, marker_line_width=0))
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=9.25, mapbox_center = {"lat": 40.75, "lon": -74})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
plot(fig)