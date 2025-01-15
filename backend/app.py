import osmnx as ox
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, box
from geopy.geocoders import Nominatim 
from flask import Flask

app = Flask(__name__)


# Disable cache 
ox.settings.use_cache = False

def calculate_walkability_score(location, radius):
    proximity_to_amenities = get_amenities(location, radius)
    proximity_to_shopping = get_shopping_and_dining(location, radius)
    proximimity_to_healthcare = get_health_amenities(location, radius)
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
    # Prepare detailed breakdown for transparency and readility of the results
    details = {
        "proximity_to_amenities": proximity_to_amenities,
        "proximity_to_shopping_and_dining": proximity_to_shopping,
        "proximity_to_healthcare": proximimity_to_healthcare,
        "walkable_street_share": walkable_streets,
        "green_space": green_space,
        "public_transportation_accessibility": public_transportation_accessibility
    }

    return walkability_score, details

#Proximity of education and workspaces 
def get_amenities(location, radius):
    try:
        # List of educational tags to check separately
        education_tags = ['kindergarten', 'school', 'university']
        education_and_workplace_locations = []

        # Query each educational tag
        for tag in education_tags:
            stops = ox.features_from_point(location, tags={'amenity': tag}, dist=radius)
            education_and_workplace_locations.extend(stops)

        # Query the office spaces
        office_stops = ox.features_from_point(location, tags={'office': True}, dist=radius)
        education_and_workplace_locations.extend(office_stops)

        return len(education_and_workplace_locations)  # The total number of unique education and workplaces 
    except Exception as e:
        print(f"Error fetching education and workplace locations: {e}")
        return 0

#Amenities related to food and retail
def get_shopping_and_dining(location, radius):
    try:
        # Create a list of tags for other dining-related amenities
        dining_tags = [
            {'amenity': 'bar'},
            {'amenity': 'cafe'},
            {'amenity': 'restaurant'},
            {'amenity': 'fast_food'},
            {'amenity': 'food_court'}
        ]

        shopping_locations = []

        # Query all 'shop' locations
        shop_tag = {'shop': True}
        shop_locations = ox.features_from_point(location, tags=shop_tag, dist=radius)
        shopping_locations.extend(shop_locations)

        # Query for other dining-related amenities
        for tag in dining_tags:
            locations = ox.features_from_point(location, tags=tag, dist=radius)
            shopping_locations.extend(locations)

        return len(shopping_locations)  # The total number of shopping and dining locations
    except Exception as e:
        print(f"Error fetching shopping and dining locations: {e}")
        return 0

#Healthcare, amenities related to medical and health services

def get_health_amenities(location, radius):
    tags = {
        'amenity': [
            'clinic',
            'dentist',
            'doctors',
            'hospital',
            'pharmacy'
        ]
    }

    healthcare_amenities = ox.features_from_point(
        location,
        tags=tags,
        dist=radius
    )

    return len(healthcare_amenities)


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
            {'highway': 'bus_stop'},
            {'railway': 'station'},
            {'railway': 'subway_entrance'},
            {'railway': 'tram_stop'}
        ]

        transport_stops = []
        for tag in transport_tags:
            stops = ox.features_from_point(location, tags=tag, dist=radius)
            transport_stops.extend(stops)

        return len(transport_stops)  # The number of unique public transport stops within the given radius
    except Exception as e:
        print(f"Error fetching public transport stops: {e}")
        return 0

#Amount of green space (the number, not squaremeters, to be modified)
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


# Geocoder setup
geolocator = Nominatim(user_agent="walkability_score_tool")

@app.route('/walkability', methods=['POST'])
def walkability():
    """
    API endpoint to calculate walkability score.
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
        # Geocode the address to get coordinates
        location = geolocator.geocode(address)
        if not location:
            return jsonify({'error': 'Address not found'}), 404
        
        coordinates = (location.latitude, location.longitude)

        # Call the walkability calculation function
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
                'proximity_to_amenities': details['proximity_to_amenities'],
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

