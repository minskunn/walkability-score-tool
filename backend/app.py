import osmnx as ox
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, box

def calculate_walkability_score(location, radius)
    return walkability_score{
    }

#Proximity to amenities
def get_amenities(location, radius)
    return #Number of amenities within the given radius

#Walkable streets (how to consider inclusivness eg. for elderly and disabled?)
def calculate_streets(location, radius)
    return 

#Public transportation
def get_transport(location, radius)
    return #The number of public transport stops within the given radius

#Amount of green space
def calculate_greenspace(location, radius)
    return #Amount of green space within the given radius

#Normalize a value to a 0–100 scale
def normalize(value, min_val=0, max_val=100):
    return 

#Calculate overall walkability score