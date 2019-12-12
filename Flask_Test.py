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
import geopandas
import geopandas.tools
from shapely.geometry import Point


with urlopen('https://raw.githubusercontent.com/aschwenker/Data-608-Final/master/Data/School%20Districts_GeoJason.json') as response:
    counties = json.load(response)
    
    
districts=geopandas.read_file('https://raw.githubusercontent.com/aschwenker/Data-608-Final/master/Data/School%20Districts_GeoJason.json')
counties_list = counties['features']
print(counties_list)
counties_list = [dict(item, **{'id':item['properties']['school_dist']}) for item in counties_list]
counties['features']=counties_list    
Borough_URL = 'https://raw.githubusercontent.com/aschwenker/Data-608-Final/master/Data/Borough%20Boundaries_geojson.JSON'
with urlopen(Borough_URL) as response:
    boroughs = json.load(response)
print(boroughs)
features_list = boroughs['features']
features_list = [dict(item, **{'id':item['properties']['boro_code']}) for item in features_list]
print(len(features_list))
boroughs['features'] = features_list
for item in features_list:
    print(item['properties']['boro_code'],item['properties']['boro_name'])
#get priority schools
df = pd.read_csv('https://raw.githubusercontent.com/aschwenker/Data-608-Final/master/Data/Safe_Routes_to_Schools_-_Priority_Schools.csv')
accidents = pd.read_csv("https://raw.githubusercontent.com/aschwenker/Data-608-Final/master/Data/Accidents_ped.csv")
print(list(accidents))
# Create the dictionary 
event_dictionary ={'Bronx' : '2', 'Staten Island' :'5', 'Brooklyn' : '3','Queens':'4','Manhattan':'1'} 
accidents_id_dict ={'BRONX' : '2', 'STATEN ISLAND' :'5', 'BROOKLYN' : '3','QUEENS':'4','MANHATTAN':'1'} 
#create geom for 

accidents["geometry"] = accidents.apply(lambda row: Point(row["LONGITUDE"], row["LATITUDE"]), axis=1)
accidents_points = geopandas.GeoDataFrame(accidents, geometry="geometry")
#set CRS
accidents_points.crs = districts.crs
#find distict of school by spatial join
accident_join = geopandas.tools.sjoin(accidents_points, districts, how="left")
#get count of schools by district for density map
accident_join_counts = accident_join.groupby('school_dist').count()['COLLISION_ID']
accident_join_counts.to_frame()
accident_join_counts = accident_join_counts.reset_index()
accident_join_counts.rename(columns = {'COLLISION_ID':'Accident_Counts'}, inplace = True)
print((accident_join_counts))
#SCHOOL
df["geometry"] = df.apply(lambda row: Point(row["Longitude"], row["Latitude"]), axis=1)
school_points = geopandas.GeoDataFrame(df, geometry="geometry")
#set CRS
school_points.crs = districts.crs
#find distict of school by spatial join
result = geopandas.tools.sjoin(school_points, districts, how="left")
#get count of schools by district for density map
result_counts = result.groupby('school_dist').count()['School Name / ID']
result_counts.to_frame()
result_counts = result_counts.reset_index()
result_counts.rename(columns = {'School Name / ID':'result_Counts'}, inplace = True)
print((result_counts))
#display density
accident_density_data = [go.Choroplethmapbox(geojson=counties, locations=accident_join_counts.school_dist, z=accident_join_counts.Accident_Counts,
                                    colorscale="Viridis", zmin=0, zmax=11,
                                    marker_opacity=0.5, marker_line_width=0)]
accident_density_layout = go.Layout(mapbox = dict(
        style = "carto-positron",
        center = dict(lat= 40.75, lon= -74),
        zoom=9),
    margin = dict(l=0, r=0, b=0, t=0))
accident_density = dict(data = accident_density_data,layout = accident_density_layout)


df['id'] = df['Borough'].map(event_dictionary) 
accidents['id']=accidents['BOROUGH'].map(accidents_id_dict)
accident_counts = accidents.groupby('id').count()['COLLISION_ID']
accident_counts.to_frame()
accident_counts = accident_counts.reset_index()
accident_counts.rename(columns = {'COLLISION_ID':'Accident_Counts'}, inplace = True) 
print(accident_counts)
locations_name = df['School Name / ID']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

data = [go.Scattermapbox(lat=df['Latitude'], lon=df['Longitude'], mode='markers', marker=dict(size=10),
text=df['School Name / ID'])]

fig_layout = go.Layout(autosize=True, hovermode='closest', mapbox=dict(
        style= "carto-positron",
        center= dict( lon= -74, lat= 40.75),
        zoom= 9,
        layers=[dict(
            source = counties,
            type = 'fill',below = 'traces', color =  'green', opacity = 0.5)]),
    margin = dict(l=0, r=0, b=0, t=0))
fig = dict(data=data, layout=fig_layout)

Borough_URL = 'https://raw.githubusercontent.com/aschwenker/Data-608-Final/master/Data/Borough%20Boundaries_geojson.JSON'
with urlopen(Borough_URL) as response:
    boroughs = json.load(response)
features_list = boroughs['features']
features_list = [dict(item, **{'id':item['properties']['boro_code']}) for item in features_list]
boroughs['features'] = features_list
df['id'] = df['Borough'].map(event_dictionary) 
# Print the DataFrame 
counts = df.groupby('id').count()['School Name / ID']
counts.to_frame()
counts = counts.reset_index()
counts.rename(columns = {'School Name / ID':'counted'}, inplace = True) 
print(counts)
choro_map_data = [go.Choroplethmapbox(geojson=boroughs, locations=accident_counts.id, z=accident_counts.Accident_Counts,
                                    colorscale="Viridis", zmin=1000, zmax=16500,
                                    marker_opacity=0.5, marker_line_width=0)]
choro_map_layout = go.Layout(mapbox = dict(
        style = "carto-positron",
        center = dict(lat= 40.75, lon= -74),
        zoom=9),
    margin = dict(l=0, r=0, b=0, t=0))
choro_map = dict(data = choro_map_data,layout = choro_map_layout)

app.layout = html.Div([
    html.H1('Dash Tabs component demo'),
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Safe Route Schools Map', value='tab-1-example'),
        dcc.Tab(label='Distribution of Safe Route Schools By Borough', value='tab-2-example'),
        dcc.Tab(label='Accident Density By Borough', value='tab-3-example')
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
            html.H3('Count of Safe Route Schools By Borough'),
            dcc.Graph(
                id='graph',
                figure = {'data': [{
                        'x': ['Bronx', 'Brooklyn','Manhattan','Queens','Staten Island'],
                        'y': [25, 46, 23,33,8],
                        'type': 'bar'
                    }]
                })
        ])

    elif tab == 'tab-3-example':
        return html.Div([
            html.H3('Accident Density By Borough'),
            dcc.Graph(
                id='Accident density',
                figure = accident_density)
        ])


if __name__ == '__main__':
    app.run_server(debug=False)