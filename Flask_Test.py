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
print(accidents['CRASH DATE'])
accidents['CRASH YEAR']=accidents['CRASH DATE'].str[-4:]
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
acc_fig_layout = go.Layout(autosize=True, hovermode='closest', mapbox=dict(
        style= "carto-positron",
        center= dict( lon= -74, lat= 40.75),
        zoom= 9,
        layers=[dict(
            source = counties,
            type = 'fill',below = 'traces', color =  'green', opacity = 0.5)]),
    margin = dict(l=0, r=0, b=0, t=0))
available_indicators = accident_join_counts['school_dist'].unique()
d = {indicator: accident_join[accident_join['school_dist']==indicator] for indicator in available_indicators}
data_dict = {indicator: [go.Scattermapbox(lat=d[indicator]['LATITUDE'], lon=d[indicator]['LONGITUDE'], mode='markers', marker=dict(size=10),
                                                        text=d[indicator]['COLLISION_ID'])] for indicator in available_indicators}
fig_dict = {indicator: dict(data=data_dict[indicator], layout=acc_fig_layout) for indicator in available_indicators}
figs=list(fig_dict.values())
print(type(figs))
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
                                    colorscale="Viridis", zmin=1000, zmax=16500,
                                    marker_opacity=0.5, marker_line_width=0)]
accident_density_layout = go.Layout(mapbox = dict(
        style = "carto-positron",
        center = dict(lat= 40.75, lon= -74),
        zoom=9),
    margin = dict(l=0, r=0, b=0, t=0))
accident_density = dict(data = accident_density_data,layout = accident_density_layout)


df['id'] = df['Borough'].map(event_dictionary) 
accidents['id']=accidents['BOROUGH'].map(accidents_id_dict)
accident_counts = accidents.groupby('CONTRIBUTING FACTOR VEHICLE 1').count()['COLLISION_ID']
accident_counts.to_frame()
accident_counts = accident_counts.reset_index()
accident_counts.rename(columns = {'COLLISION_ID':'Accident_Counts'}, inplace = True) 
print(accident_counts)
line_data = go.Figure([go.Scatter(x=accident_counts['CONTRIBUTING FACTOR VEHICLE 1'], y=accident_counts['Accident_Counts'])])
line_fig = dict(data=line_data)
from plotly.offline import plot

locations_name = df['School Name / ID']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


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


acc_pt_data = [go.Scattermapbox(lat=accident_join['LATITUDE'], lon=accident_join['LONGITUDE'], mode='markers', marker=dict(size=10),
text=accidents['COLLISION_ID'])]

acc_fig_layout = go.Layout(autosize=True, hovermode='closest', mapbox=dict(
        style= "carto-positron",
        center= dict( lon= -74, lat= 40.75),
        zoom= 9,
        layers=[dict(
            source = counties,
            type = 'fill',below = 'traces', color =  'green', opacity = 0.5)]),
    margin = dict(l=0, r=0, b=0, t=0))
acc_fig = dict(data=acc_pt_data, layout=acc_fig_layout)


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
options=[{'label': i, 'value': i} for i in available_indicators]
print((options))

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout =html.Div([
    html.H1('Pedestrian Safety near New York City Schools'),
    html.Div([dcc.Graph(id='map', figure=fig),dcc.Graph(
                id='graph',
                figure = {'data': [{
                        'x': ['Bronx', 'Brooklyn','Manhattan','Queens','Staten Island'],
                        'y': [25, 46, 23,33,8],
                        'type': 'bar'
                    }]
                }),            dcc.Graph(
                id='Accident density',
                figure = accident_density),
            dcc.Dropdown(
                id='available_idc',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value = '11'
                )
    ,dcc.Graph(id='acc_map')
    
]) 
])



@app.callback (Output('acc_map', 'figure'),
            [Input('available_idc', 'value')])

def make_main_figure(indicator_selected):

    dff = d[indicator_selected]
    LAT_LIST = dff.LATITUDE.unique()
    LAT_LIST.sort()
    LON_LIST = dff.LONGITUDE.unique()
    LON_LIST.sort()
    center_lat = LAT_LIST[round(len(LAT_LIST)/2)]
    center_lon = LON_LIST[round(len(LON_LIST)/2)]
    acc_pt_data = [go.Scattermapbox(lat=dff['LATITUDE'], lon=dff['LONGITUDE'], mode='markers', marker=dict(size=10),
text=dff['COLLISION_ID'])]
    
    acc_fig_layout = go.Layout(autosize=True, hovermode='closest', mapbox=dict(
            style= "carto-positron",
            center= dict(lon= center_lon, lat= center_lat),
            zoom= 12.5,
            layers=[dict(
                source = counties,
                type = 'fill',below = 'traces', color =  'green', opacity = 0.5)]),
        margin = dict(l=0, r=0, b=0, t=0))
    acc_fig = dict(data=acc_pt_data, layout=acc_fig_layout)

    return acc_fig


            
if __name__ == '__main__':
    app.run_server(debug=False)