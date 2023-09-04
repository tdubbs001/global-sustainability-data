#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import folium 
from folium import Choropleth, Popup

data = pd.read_csv('global-data-on-sustainable-energy.csv')
data['Renewable energy share in the total final energy consumption (%)'].interpolate(method='linear', inplace=True)


#Now I am going to create a visualizaton of the amount of renewable energy in 2020 for each country.

renewable_energy_share_2019 = data[data['Year'] == 2019][['Entity', 'Renewable energy share in the total final energy consumption (%)']]

# Initialize the map
m = folium.Map(location=[0, 0], zoom_start=3)

# Add the choropleth layer
choro = Choropleth(
    geo_data="archive/countries.geojson",
    name='choropleth',
    data=renewable_energy_share_2019,
    columns=['Entity', 'Renewable energy share in the total final energy consumption (%)'],
    key_on='feature.properties.ADMIN',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2,
).add_to(m)

# Convert DataFrame to dictionary for quick lookup
renewable_dict = renewable_energy_share_2019.set_index('Entity')['Renewable energy share in the total final energy consumption (%)'].to_dict()


# Function to add popups
def add_popup(feature, **kwargs):
    country_name = feature['properties']['ADMIN']
    renewable_share = renewable_dict.get(country_name, 'Data not available')
    popup_text = f"{country_name}<br>Renewable Energy Share: {renewable_share}%"
    Popup(popup_text).add_to(kwargs['color_map'])

# # Add popups
import json

# Load GeoJSON file into a Python dictionary
with open("archive/countries.geojson", "r") as f:
    geo_json_data = json.load(f)

# Loop through features to add popups
for feature in geo_json_data['features']:
    country_name = feature['properties']['ADMIN']
    renewable_share = renewable_dict.get(country_name, 'Data not available')
    popup_text = f"""
<div style='width:200px;'>
    <h4 style='font-weight:bold;'>{country_name}</h4>
    <p>Renewable Energy Share of Total Energy Consumption: {renewable_share}%</p>
</div>
"""
    folium.GeoJson(
        feature,
        name=country_name,
        style_function=lambda feature: {
            'fillColor': 'grey',
            'color': 'black',
            'weight': 1,
            'dashArray': '5, 5'
        },
        highlight_function=lambda x: {'weight': 3, 'fillColor': '#666666'},
        smooth_factor=0.1,
        zoom_on_click=False,
    ).add_child(folium.Popup(popup_text)).add_to(m)

# Show the map
m.save('renewable_energy.html')
