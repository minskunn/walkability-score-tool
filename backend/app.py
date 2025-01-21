import osmnx as ox
import geopandas as gpd
import pandas as pd
import requests
import os
from shapely.geometry import Point, box
from geopy.geocoders import Nominatim 
import certifi
import json  

from flask import Flask, request, jsonify
from flask_cors import CORS

# Set the SSL certificate path
os.environ['SSL_CERT_FILE'] = certifi.where()

app = Flask(__name__)
CORS(app, origins=["https://walkability-score.netlify.app"])

# Disable cache 
ox.settings.use_cache = False

def calculate_walkability_score(location, radius):
    school_and_workplace_count=get_school_and_work_amenities(location, radius)
    shopping_and_dining_count=get_shopping_and_dining(location, radius)
    healthcare_services_count=get_health_amenities(location, radius)
    walkable_streets = get_streets(location, radius)
    green_space = get_greenspaces(location, radius)
    public_transportation_accessibility = get_transport(location, radius)

    total_amenities_count = school_and_workplace_count + shopping_and_dining_count + healthcare_services_count

    # Calculate the weighted walkability score

    walkability_score = (
        0.40 * normalize(total_amenities_count) +
        0.30 * normalize(walkable_streets) +
        0.15 * normalize(green_space) +
        0.15 * normalize(public_transportation_accessibility)
    )
    # Prepare detailed breakdown for transparency and readility of the results
    details = {
        "proximity_to_school_and_workplace": school_and_workplace_count,
        "proximity_to_shopping_and_dining": shopping_and_dining_count,
        "proximity_to_healthcare": healthcare_services_count,
        "walkable_street_share": walkable_streets,
        "green_space": green_space,
        "public_transportation_accessibility": public_transportation_accessibility
    }

    return walkability_score, details

#Proximity of education and workspaces 
def get_school_and_work_amenities(location, radius):
    try:
        school_and_work_tags = {
            'amenity': ['kindergarten', 'school', 'university', 'college'],
            'office': True,
            'building': 'office'
        }

        # Retrieve the features using features_from_point
        school_and_work_amenities = ox.features_from_point(center_point=location, tags=school_and_work_tags, dist=radius)

        # A set to store unique names (to avoid duplicates)
        unique_school_and_work_amenities = set(school_and_work_amenities['name'].dropna())
        
         #Return the number of unique amenities
        return len(unique_school_and_work_amenities)
    except Exception as e:
        print(f"Error fetching education and workplace locations: {e}")
        return 0
            

#Amenities related to food and retail
def get_shopping_and_dining(location, radius):
    try:
        amenity_tags = {
            'amenity': [
                'bar',
                'cafe',
                'restaurant',
                'fast_food',
                'food_court'
            ],
            'shop': True
        }

        shopping_and_dining_locations = ox.features_from_point(center_point=location, tags=amenity_tags, dist=radius)

        # A set to store unique names (to avoid duplicates)
        unique_shopping_and_dining_locations = set(shopping_and_dining_locations['name'].dropna())

        return len(unique_shopping_and_dining_locations)
    except Exception as e:
        print(f"Error fetching shopping and dining locations: {e}")
        return 0


#Healthcare, amenities related to medical and health services
def get_health_amenities(location, radius):
    try:
        healthcare_tags = {
            'amenity': [
                'clinic',
                'dentist',
                'doctors',
                'hospital',
                'pharmacy'
            ]
        }

        healthcare_amenities = ox.features_from_point(
            center_point=location,
            tags=healthcare_tags,
            dist=radius
        )

        return len(healthcare_amenities)
    except Exception as e:
        print(f"Error fetching healthcare locations: {e}")
        return 0

#Calculate percentage of pedestrian-friendly streets of all the street in the radius area
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
    transport_stops = ox.features_from_point(
        location, 
        tags={
            'public_transport': 'station',
            'highway': 'bus_stop',
            'railway': ['station', 'subway_entrance', 'tram_stop']
        }, 
        dist=radius 
    )
    return len((transport_stops))  # The number of unique public transport stops within the given radius

#Surface area of green spaces
    
def get_greenspaces(location, radius):
    try:
        green_space_tags = {
            'leisure': ['park', 'playground'],
            'landuse': ['greenery', 'grass', 'recreation_ground']
        }
        green_spaces = ox.features_from_point(center_point=location, tags=green_space_tags, dist=radius)

        # Re-project to a projected CRS.
        green_spaces_projected = green_spaces.to_crs(epsg=3857)

        # Calculate the total surface area in square meters
        total_green_area_m2 = green_spaces_projected.geometry.area.sum()

        # Convert the total area to square kilometers
        total_green_area_km2 = total_green_area_m2 / 1_000_000  # m² to km²

        return total_green_area_km2
    except Exception as e:
        print(f"Error fetching green spaces: {e}")
        return 0.0
    


#Normalize a value to a 0–100 scale
def normalize(value, min_val=0, max_val=100):
    return min(max(0, (value - min_val) / (max_val - min_val) * 100), 100)


# Geocoder setup
geolocator = Nominatim(user_agent="walkability_score_tool")

@app.route('/walkability', methods=['POST'])
def walkability():
    """
    This is API endpoint to calculate walkability score.
    Takes an address as input, geocodes it to coordinates, 
    calculates normalized walkability score, and returns the score and metrics about the surroundings within the radius.
    """
    try:
        # Parse the JSON input
        data = request.get_json()
        address = data.get('address', None)
        radius = data.get('radius', 1200)

        if not address:
            return jsonify({'error': 'Enter a valid address'}), 400
        
        # Print the entire JSON input data
        print(json.dumps(data, indent=4))
        
        # Geocode the address to get coordinates
        location = geolocator.geocode(address)
        if not location:
            return jsonify({'error': 'Address not found'}), 404

        
        coordinates = (location.latitude, location.longitude)


        # Call the walkability score calculation function
        score, details = calculate_walkability_score(coordinates, radius)
        # Format the response as JSON
        response = {
            'address': address,
            'coordinates': {
                'latitude': location.latitude,
                'longitude': location.longitude
            },
             'walkability_score': round(score),
            'details': {
                'proximity_to_school_and_workplace': details['proximity_to_school_and_workplace'],
                'proximity_to_shopping_and_dining': details['proximity_to_shopping_and_dining'],
                'proximity_to_healthcare': details['proximity_to_healthcare'],
                'walkable_street_share': round(details['walkable_street_share'], 2),
                'green_space': details['green_space'],
                'public_transportation_accessibility': details['public_transportation_accessibility']
            }
        }
        return jsonify(response), 200
    
    except Exception as e:
        # Handle unexpected errors
        return jsonify({'error': str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

