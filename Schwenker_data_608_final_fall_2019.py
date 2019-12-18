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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def find_lat(dff):
    LAT_LIST = dff.LATITUDE.unique()
    LAT_LIST.sort()
    center_lat = LAT_LIST[round(len(LAT_LIST)/2)]
    return(center_lat)
def find_lon(dff):
    LON_LIST = dff.LONGITUDE.unique()
    LON_LIST.sort()
    center_lon = LON_LIST[round(len(LON_LIST)/2)]   
    return(center_lon) 
    
#LOAD DATA
#LOAD AS GEOJSON TO MANIPULATE THE FEATURE ID
with urlopen('https://raw.githubusercontent.com/aschwenker/Data-608-Final/master/Data/School%20Districts_GeoJason.json') as distict_response:
    school_districts_geojson = json.load(distict_response)
Borough_URL = 'https://raw.githubusercontent.com/aschwenker/Data-608-Final/master/Data/Borough%20Boundaries_geojson.JSON'
with urlopen(Borough_URL) as borough_response:
    boroughs = json.load(borough_response)    
#LOAD INTO GDF FOR SPATIAL JOINS    
districts=geopandas.read_file('https://raw.githubusercontent.com/aschwenker/Data-608-Final/master/Data/School%20Districts_GeoJason.json')

#LOAD CSV DATA 
df = pd.read_csv('https://raw.githubusercontent.com/aschwenker/Data-608-Final/master/Data/Safe_Routes_to_Schools_-_Priority_Schools.csv')
accidents = pd.read_csv("https://raw.githubusercontent.com/aschwenker/Data-608-Final/master/Data/Accidents_ped.csv")

#GET ITEM FROM FEATURES TO ASSIGN AS ID
school_districts_geojson_list = school_districts_geojson['features']
school_districts_geojson_list = [dict(item, **{'id':item['properties']['school_dist']}) for item in school_districts_geojson_list]
school_districts_geojson['features']=school_districts_geojson_list    

boroughs_geojson_features_list = boroughs['features']
boroughs_geojson_features_list = [dict(item, **{'id':item['properties']['boro_code']}) for item in boroughs_geojson_features_list]
boroughs['features'] = boroughs_geojson_features_list

#GET JUST YEAR
accidents['CRASH YEAR']=accidents['CRASH DATE'].str[-4:]
# Create the dictionary to associate borough name and numeric identifier
event_dictionary ={'Bronx' : '2', 'Staten Island' :'5', 'Brooklyn' : '3','Queens':'4','Manhattan':'1'} 
accidents_id_dict ={'BRONX' : '2', 'STATEN ISLAND' :'5', 'BROOKLYN' : '3','QUEENS':'4','MANHATTAN':'1'} 

#create geom for accidents from lat lot
accidents['label']= accidents['CRASH YEAR']+" " +accidents['CONTRIBUTING FACTOR VEHICLE 1']
accidents["geometry"] = accidents.apply(lambda row: Point(row["LONGITUDE"], row["LATITUDE"]), axis=1)
accidents_points = geopandas.GeoDataFrame(accidents, geometry="geometry")
#set CRS
accidents_points.crs = districts.crs
#find distict of school by spatial join
accident_join = geopandas.tools.sjoin(accidents_points, districts, how="left")
#get count of accidents by district for density map
accident_join_counts = accident_join.groupby('school_dist').count()['COLLISION_ID']
accident_join_counts.to_frame()
accident_join_counts = accident_join_counts.reset_index()
accident_join_counts.rename(columns = {'COLLISION_ID':'Accident_Counts'}, inplace = True)

#CREATE GEOMETRY FOR SCHOOLS AND GDF
df["geometry"] = df.apply(lambda row: Point(row["Longitude"], row["Latitude"]), axis=1)
school_points = geopandas.GeoDataFrame(df, geometry="geometry")
#set CRS
school_points.crs = districts.crs
#find distict of school by spatial join
schools_with_dist = geopandas.tools.sjoin(school_points, districts, how="left")
#get count of schools by district for density map
result_counts = schools_with_dist.groupby('school_dist').count()['School Name / ID']
result_counts.to_frame()
result_counts = result_counts.reset_index()
result_counts.rename(columns = {'School Name / ID':'result_Counts'}, inplace = True)

#PRE FILTER DATA BEFORE INITIALIZING APP, SAVE PROCESSING TIME BY NOT FILTER EACH SELECTION    
available_indicators = accident_join_counts['school_dist'].unique()
#CREATE DICTIONARY OF ALL DFS AFTER FILTER {id:DF}
d = {indicator: accident_join[accident_join['school_dist']==indicator] for indicator in available_indicators}
schools_dict = {indicator: schools_with_dist[schools_with_dist['school_dist']==indicator] for indicator in available_indicators}

# DICTIONARY OF DATA FOR MAP LAYERS

data_dict = {indicator: [go.Scattermapbox(lat=d[indicator]['LATITUDE'], lon=d[indicator]['LONGITUDE'],name = 'Accidents', mode='markers', marker=dict(size=10),
                                                        text=d[indicator]['label']),go.Scattermapbox(lat=schools_dict[indicator]['Latitude'], lon=schools_dict[indicator]['Longitude'],name = 'Identified Schools', mode='markers', marker=dict(size=14,color='LightSkyBlue'),
text=schools_dict[indicator]['School Name / ID'])] for indicator in available_indicators}
layout_dict = {indicator:    go.Layout(autosize=True, hovermode='closest', mapbox=dict(
            style= "carto-positron",
            center= dict(lon= find_lon(d[indicator]), lat= find_lat(d[indicator])),
            zoom= 12.5,
            layers=[dict(
                source = school_districts_geojson,
                type = 'fill',below = 'traces', color =  'green', opacity = 0.5)]),
        margin = dict(l=0, r=0, b=0, t=0)) for indicator in available_indicators}
#CREATE DICTIONARY OF FIGURES FOR EACH LAYER
   
fig_dict = {indicator: dict(data=data_dict[indicator], layout=layout_dict[indicator]) for indicator in available_indicators}
#CREATE LIST OF ALL FIGURES

#display density for accidents by borough
accident_density_data = [go.Choroplethmapbox(geojson=school_districts_geojson, locations=accident_join_counts.school_dist, z=accident_join_counts.Accident_Counts,
                                    colorscale="Viridis", zmin=1000, zmax=16500,
                                    marker_opacity=0.5, marker_line_width=0)]
accident_density_layout = go.Layout(mapbox = dict(
        style = "carto-positron",
        center = dict(lat= 40.75, lon= -74),
        zoom=9),
    margin = dict(l=0, r=0, b=0, t=0))
accident_density = dict(data = accident_density_data,layout = accident_density_layout)



accident_counts = accidents.groupby('CRASH YEAR').count()['COLLISION_ID']
accident_counts.to_frame()
accident_counts = accident_counts.reset_index()
accident_counts.rename(columns = {'COLLISION_ID':'Accident_Counts'}, inplace = True) 
print(accident_counts)
line_data = go.Figure([go.Scatter(x=accident_counts['CRASH YEAR'], y=accident_counts['Accident_Counts'])])
line_fig = dict(data=line_data)

# SCHOOLS AND DISTRICTS 

data = [go.Scattermapbox(lat=df['Latitude'], lon=df['Longitude'], mode='markers', marker=dict(size=10),
text=df['School Name / ID'])]

fig_layout = go.Layout(autosize=True, hovermode='closest', mapbox=dict(
        style= "carto-positron",
        center= dict( lon= -74, lat= 40.75),
        zoom= 9,
        layers=[dict(
            source = school_districts_geojson,
            type = 'fill',below = 'traces', color =  'green', opacity = 0.5)]),
    margin = dict(l=0, r=0, b=0, t=0))
fig = dict(data=data, layout=fig_layout)



#INITIALIZE APP
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout =html.Div([html.Div([
    html.H1('Pedestrian Safety near New York City Schools')]),
    html.Div([html.H2('In 2013 DOT analyzed citywide crash data and school data in order to identify a new group of 135 public, private and parochial elementary and middle schools Priority Schools. Each Priority Schools receives an individualized planning study which determines both short-term and long-term measures to improve safety.'),
                      dcc.Graph(id='map', figure=fig)]),
    html.Div([html.H2('Selected Schools Distribution By Borough'),
              dcc.Graph(
                id='graph',
                figure = {'data': [{
                        'x': ['Bronx', 'Brooklyn','Manhattan','Queens','Staten Island'],
                        'y': [25, 46, 23,33,8],
                        'type': 'bar'
                    }]
                })]),
    html.Div([
      html.H2('Accident Density By School District'),
      dcc.Graph(id='Accident density',
                figure = accident_density)]),
      html.Div([html.H2('Accident and Schools Filtered By School District'),
                html.H3('Select Your School District Below'),
            dcc.Dropdown(
                id='available_idc',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value = '10'
                ),
                    dcc.Graph(id='acc_map')
                    ])
            ])

@app.callback (Output('acc_map', 'figure'),
            [Input('available_idc', 'value')])

def make_main_figure(indicator_selected):
    acc_fig = fig_dict[indicator_selected]
    return acc_fig           
if __name__ == '__main__':
    app.run_server(debug=False)