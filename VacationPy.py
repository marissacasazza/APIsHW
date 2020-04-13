#!/usr/bin/env python
# coding: utf-8

# # VacationPy
# ----
# 
# #### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[5]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import gmaps
import os

# Import API key
from api_keys import g_key


# ### Store Part I results into DataFrame
# * Load the csv exported in Part I to a DataFrame

# In[6]:


data_csv = pd.read_csv(r'output_data\cities.csv')
data_csv


# ### Humidity Heatmap
# * Configure gmaps.
# * Use the Lat and Lng as locations and Humidity as the weight.
# * Add Heatmap layer to map.

# In[7]:


import gmaps.datasets
gmaps.configure(api_key=g_key)

# data = gmaps.datasets.load_dataset(data_csv)
# # maps = gmaps.Map()
# # maps.add_layer(gmaos.Heatmap(data=data))
# data


# In[8]:


# Store 'Lat' and 'Lng' into  locations 
locations = data_csv[["lat", "lon"]].astype(float)

# Convert Poverty Rate to float and store
# HINT: be sure to handle NaN values
#census_data_complete = census_data_complete.dropna()
humidity_rate = data_csv["hum"].astype(float)


# In[9]:


# Create a poverty Heatmap layer
fig = gmaps.figure()

heat_layer = gmaps.heatmap_layer(locations, weights=humidity_rate, 
                                 dissipating=False, max_intensity=100,
                                 point_radius = 2)

fig.add_layer(heat_layer)

fig


# ### Create new DataFrame fitting weather criteria
# * Narrow down the cities to fit weather conditions.
# * Drop any rows will null values.

# In[10]:


data_csv = data_csv.dropna()
data_csv


# ### Hotel Map
# * Store into variable named `hotel_df`.
# * Add a "Hotel Name" column to the DataFrame.
# * Set parameters to search for hotels with 5000 meters.
# * Hit the Google Places API for each city's coordinates.
# * Store the first Hotel result into the DataFrame.
# * Plot markers on top of the heatmap.

# In[11]:


data_csv["hotel_name"] = ""
data_csv


# In[12]:


# params dictionary to update each iteration
params = {
    "radius": 5000,
    "types": "lodging",
    "key": g_key
}

# Use the lat/lng we recovered to identify airports
for index, row in data_csv.iterrows():
    # get lat, lng from df
    lat = row["lat"]
    lon = row["lon"]

    # change location each iteration while leaving original params in place
    params["location"] = f"{lat},{lon}"

    # Use the search term: "International Airport" and our lat/lng
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    # make request and print url
    hotel_address = requests.get(base_url, params=params).json()
    
#     print the name_address url, avoid doing for public github repos in order to avoid exposing key
#hotel_address['results'][0]['name']

    # convert to json

    # print(json.dumps(name_address, indent=4, sort_keys=True))

    # Since some data may be missing we incorporate a try-except to skip any that are missing a data point.
    try:
        data_csv.loc[index, "hotel_name"] = hotel_address["results"][0]["name"]
    except (KeyError, IndexError):
        print("Missing field/result... skipping.")


# In[ ]:





# In[ ]:


# NOTE: Do not change any of the code in this cell

# Using the template add the hotel marks to the heatmap
info_box_template = """
<dl>
<dt>Name</dt><dd>{Hotel Name}</dd>
<dt>City</dt><dd>{City}</dd>
<dt>Country</dt><dd>{Country}</dd>
</dl>
"""
# Store the DataFrame Row
# NOTE: be sure to update with your DataFrame name
hotel_info = [info_box_template.format(**row) for index, row in hotel_address.iterrows()]
locations = hotel_df[["lat", "lng"]]


# In[ ]:


# Add marker layer ontop of heat map
fig = gmaps.figure()
heat_layer = gmaps.heatmap_layer(locations,
                                 dissipating=False,
                                 max_intensity=100)
marker_layer = gmaps.marker_layer(locations, info_box_content = hotel_info)
# Add marker layer ontop of heat map
fig.add_layer(heat_layer)
fig.add_layer(marker_layer)
# Display Map
fig


# Display Map

