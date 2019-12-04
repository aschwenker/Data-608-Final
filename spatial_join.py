# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 21:19:53 2019

@author: ASchwenker
"""
import pandas as pd
import geopandas
import geopandas.tools
from shapely.geometry import Point
from urllib.request import urlopen
import json

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