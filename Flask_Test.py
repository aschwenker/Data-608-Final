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
df = pd.read_csv('https://raw.githubusercontent.com/aschwenker/Data-608-Final/master/Data/Safe_Routes_to_Schools_-_Priority_Schools.csv')
accidents = pd.read_csv('https://raw.githubusercontent.com/aschwenker/Data-608-Final/master/Data/accidents_2018_2019.csv')
print(list(accidents))
# Create the dictionary 
event_dictionary ={'Bronx' : '2', 'Staten Island' :'5', 'Brooklyn' : '3','Queens':'4','Manhattan':'1'} 
accidents_id_dict ={'BRONX' : '2', 'STATEN ISLAND' :'5', 'BROOKLYN' : '3','QUEENS':'4','MANHATTAN':'1'} 

# Add a new column named 'Price' 
df['id'] = df['Borough'].map(event_dictionary) 
accidents['id']=accidents['BOROUGH'].map(accidents_id_dict)
accident_counts = accidents.groupby('id').count()['COLLISION_ID']
accident_counts.to_frame()
accident_counts = accident_counts.reset_index()
accident_counts.rename(columns = {'COLLISION_ID':'Accident_Counts'}, inplace = True) 
print(accident_counts)
site_lat = df.Latitude
site_lon = df.Longitude
locations_name = df['School Name / ID']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

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

Borough_URL = 'https://raw.githubusercontent.com/aschwenker/Data-608-Final/master/Data/Borough%20Boundaries_geojson.JSON'
with urlopen(Borough_URL) as response:
    boroughs = json.load(response)
features_list = boroughs['features']
features_list = [dict(item, **{'id':item['properties']['boro_code']}) for item in features_list]
boroughs['features'] = features_list
event_dictionary ={'Bronx' : '2', 'Staten Island' :'5', 'Brooklyn' : '3','Queens':'4','Manhattan':'1'} 
# Add a new column named 'Price' 
df['id'] = df['Borough'].map(event_dictionary) 
# Print the DataFrame 
counts = df.groupby('id').count()['School Name / ID']
counts.to_frame()
counts = counts.reset_index()
counts.rename(columns = {'School Name / ID':'counted'}, inplace = True) 

choro_map_data = [go.Choroplethmapbox(geojson=boroughs, locations=accident_counts.id, z=accident_counts.Accident_Counts,
                                    colorscale="Viridis", zmin=9000, zmax=88000,
                                    marker_opacity=0.5, marker_line_width=0)]
choro_map_layout = go.Layout(mapbox = dict(
        style = "carto-positron",
        center = dict(lat= 40.75, lon= -74),
        zoom=9.25))
choro_map = dict(data = choro_map_data,layout = choro_map_layout)


app.layout = html.Div([
    html.H1('Dash Tabs component demo'),
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Safe Route Schools Map', value='tab-1-example'),
        dcc.Tab(label='Distribution of Safe Route Schools By Borough', value='tab-2-example'),
        dcc.Tab(label='Tab 3', value='tab-3-example'),
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
                        'x': ['Bronx', 'Manhattan','Queens','Staten Island'],
                        'y': [25, 46, 23,33,8],
                        'type': 'bar'
                    }]
                })
        ])
    elif tab == 'tab-3-example':
        return html.Div([
            html.H3('Tab 3'),
            dcc.Graph(
                id='choro map',
                figure = choro_map)
        ])


if __name__ == '__main__':
    app.run_server(debug=False)