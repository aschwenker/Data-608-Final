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

with urlopen('https://raw.githubusercontent.com/aschwenker/Data-608-Final/master/Data/School%20Districts_GeoJason.json') as distresponse:
    counties = json.load(distresponse)
print(counties)
Borough_URL = 'https://raw.githubusercontent.com/aschwenker/Data-608-Final/master/Data/Borough%20Boundaries_geojson.JSON'
with urlopen(Borough_URL) as response:
    boroughs = json.load(response)
print(boroughs)
features_list = boroughs['features']
features_list = [dict(item, **{'id':item['properties']['boro_code']}) for item in features_list]

counties_list = counties['features']
print(counties_list)
counties_list = [dict(item, **{'id':item['properties']['school_dist']}) for item in counties_list]
counties['features']=counties_list
print(len(features_list))
boroughs['features'] = features_list
for item in features_list:
    print(item['properties']['boro_code'],item['properties']['boro_name'],item['id']) 
All_SChool_URL = 'https://data.cityofnewyork.us/resource/9ck8-hj3u.json'
mapbox_access_token = 'pk.eyJ1IjoiYXNjaHdlbmtlcjY2OTAiLCJhIjoiY2szZDhybTFtMHVoMTNjcGk4MnozZDlmZyJ9.5dVGGTKgF6B8O9YlWjuXTw'

df = pd.read_csv('https://raw.githubusercontent.com/aschwenker/Data-608-Final/master/Data/Safe_Routes_to_Schools_-_Priority_Schools.csv')
site_lat = df.Latitude
print(site_lat)
site_lon = df.Longitude
locations_name = df['School Name / ID']
print(locations_name)
event_dictionary ={'Bronx' : '2', 'Staten Island' :'5', 'Brooklyn' : '3','Queens':'4','Manhattan':'1'} 

# Add a new column named 'Price' 
df['id'] = df['Borough'].map(event_dictionary) 

# Print the DataFrame 
counts = df.groupby('id').count()['School Name / ID']
counts.to_frame()
counts = counts.reset_index()
counts.rename(columns = {'School Name / ID':'counted'}, inplace = True) 

print(list(counts))
print(counts.counted)
      
fig = go.Figure()




fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=counts.id, z=counts.counted,
                                    colorscale="Viridis", zmin=0, zmax=46,
                                    marker_opacity=0.5, marker_line_width=0))
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=9.25, mapbox_center = {"lat": 40.75, "lon": -74})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
plot(fig)