import osmnx as ox
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, box


def calculate_walkability_score(location, radius):
    proximity_to_amenities = get_amenities(location, radius)
    walkable_streets = get_streets(location, radius)
    green_space = get_greenspaces(location, radius)
    public_transportation_accessibility = get_transport(location, radius)

    # Calculate the weighted walkability score
    walkability_score = (
        0.40 * normalize(proximity_to_amenities) +
        0.30 * normalize(walkable_streets) +
        0.15 * normalize(green_space) +
        0.15 * normalize(public_transportation_accessibility)
    )
    # Prepare detailed breakdown for transparency
    details = {
        "proximity_to_amenities": proximity_to_amenities,
        "walkable_street_share": walkable_streets,
        "green_space": green_space,
        "public_transportation_accessibility": public_transportation_accessibility
    }

    return walkability_score, details

#Proximity to amenities
def get_amenities(location, radius):
    amenities = ox.features_from_point(
        location,
        tags={'amenity': True},
        dist=radius
    )
    return len(amenities) #Number of amenities within the given radius

    #Calculate percentage of pedestrian-friendly streets

def get_streets(location, radius):
    G = ox.graph_from_point(location, dist=radius, network_type='walk') 
    
    total_street_length = 0
    pedestrian_friendly_length = 0

    for u, v, data in G.edges(data=True):
        total_street_length += data.get('length', 0)  # Total length of all streets
        if data.get('highway') in ['footway', 'pedestrian', 'path']:
            pedestrian_friendly_length += data.get('length', 0)  # Length of walkable streets
    
    # Actual percentage calc
    walkable_street_score = (pedestrian_friendly_length / total_street_length) * 100 if total_street_length > 0 else 0

    return walkable_street_score

    #Amount of unique public transport stops within the radius

def get_transport(location, radius):
    try:
        transport_tags = [
            {'public_transport': 'station'}, 
            {'building': 'train_station'}
        ]

        transport_stops = []
        for tag in transport_tags:
            stops = ox.features_from_point(location, tags=tag, dist=radius)
            transport_stops.extend(stops)

        return len(transport_stops)  # The number of unique public transport stops within the given radius
    except Exception as e:
        print(f"Error fetching public transport stops: {e}")
        return 0

#Amount of green space
def get_greenspaces(location, radius):
    green_spaces = ox.features_from_point(
        location,
        tags={'leisure': 'park','leisure': 'playground','landuse': 'greenery','landuse': 'recreation_ground'},  
        dist=radius
    )
    return len(green_spaces) #Return the area of green space 

#Normalize a value to a 0–100 scale
def normalize(value, min_val=0, max_val=100):
    return min(max(0, (value - min_val) / (max_val - min_val) * 100), 100)

location = (59.9227, 10.6793)  # Example coordinates in Lysaker
score, details = calculate_walkability_score(location, radius=1200)
print("Walkability Score:", round(score))

# Display the detailed metrics with descriptions first
print("\nDetails:")
print(f"- {details['proximity_to_amenities']} amenities within the area.")
print(f"- {round(details['walkable_street_share'])}% of total streets are walkable.")
print(f"- {details['green_space']} green spaces accessible in the radius.")
print(f"- {details['public_transportation_accessibility']} public transport stops nearby.")


