# Walkability Score Calculator

## Introduction

The **Walkability Score Calculator** is a tool designed to evaluate how pedestrian-friendly a location is by analyzing key features within a 1,200-meter radius — approximately the distance an average person can walk in 15 minutes.  

By entering an address, the calculator assesses the surrounding area, identifying:  
- Nearby **educational institutions, shops, offices, and healthcare services**.  
- The **percentage of streets reserved for pedestrians**.  
- The total **area of parks and green spaces**.  
- The **number of public transport stops** available.  

These factors are combined into an overall **walkability score**, weighted as follows:  
- **40%**: Proximity to amenities (schools, shops, offices, healthcare).  
- **30%**: Percentage of streets that are walkable.  
- **15%**: Area of green spaces.  
- **15%**: Public transport accessibility.  

The result is a clear, data-driven measure of how walkable an area is, helping users evaluate and compare locations easily.

---

## Features

- **Dynamic Input**: Enter any address, and the tool will fetch the relevant data.  
- **Detailed Metrics**: Breaks down the walkability score into individual components for better insights.   
- **Simple UI**: Designed for ease of use, whether you're a casual user or a professional urban planner.  

---

## How It Works

1. **Enter an Address**: Input an address into the search bar on the website.  
2. **Data Fetching**: The tool uses OpenStreetMap (OSM) data to analyze the area.  
3. **Score Calculation**:  
   - It identifies and quantifies the presence of amenities, parks, walkable streets, and transport stops.  
   - A weighted formula is applied to produce the final walkability score.  
4. **Results**:  
   - See the **overall score** as well as a breakdown of contributing factors.  

---

## Technologies Used

- **Frontend**:  
  - HTML, CSS, and JavaScript for a responsive and user-friendly interface.  
  - Deployed on **Netlify** for fast and reliable hosting.  
 
- **Backend**: 
The backend is built using **Python** (Flask) and relies on the following libraries:  
- **Mapping and Spatial Analysis**: `osmnx`, `geopandas`, `shapely`  
- **Data Handling**: `pandas`, `json`  
- **Location Services**: `geopy`  

- **Data Source**:  
  - The app relies on **OpenStreetMap (OSM)** for mapping and location data.  

---

**Rationale Behind the Weighting (40/30/15/15)**
- Proximity to Amenities (40%): This is the most important factor, reflecting the 15-minute city principle, where essential services and amenities should be accessible within a short walk.
- Walkable Streets (30%): For the 15-minute city principle to work, streets must be safe, pedestrian-friendly, and designed to be inclusive for all (including the elderly and disabled). This factor should have a high weight, given its direct impact on the comfort and safety of pedestrians.
- Amount of Green Space (15%): While green spaces are not central to the core concept of the 15-minute city, they enhance walkability by providing a more comfortable and enjoyable walking environment. Green spaces contribute significantly to well-being and quality of life.
- Public Transportation Accessibility (15%): Although outside the immediate scope of walking, public transport supports mobility for longer distances, contributing to overall accessibility.

## Explanation for Limiting Features to Those with Names
Limiting features to those with a name attribute improves data quality, avoids duplicates, and ensures relevance to the walkability analysis. Here's a concise breakdown:

Advantages

Avoiding Duplicates: Named features are less likely to overlap or represent the same entity multiple times, reducing overestimation of nearby amenities (e.g., distinguishing two "ABC High School" entries).
Higher Data Quality: Features with names are usually more complete and reliable in OpenStreetMap (OSM), while unnamed entries often lack context or specificity.
Relevance to Users: Named entities are more likely to represent functional, publicly accessible amenities, ensuring results align better with the tool’s purpose.
Improved Clarity: If displayed in results or maps, named features are easier for users to interpret and understand.

Trade-offs

Exclusion of Valid Features: Important but unnamed amenities (e.g., local schools) might be missed, particularly in areas with incomplete OSM data.
Urban Bias: Rural or less-mapped areas might have fewer named entries, introducing potential bias toward urbanized locations.
Dependence on OSM Quality: The approach relies on consistent tagging by mappers, which isn’t always guaranteed, potentially excluding relevant features.
