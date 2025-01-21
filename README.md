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
- **Interactive Map Integration**: Highlights nearby amenities and pedestrian-friendly streets.  
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
   - View nearby points of interest on an interactive map.

---

## Technologies Used

- **Frontend**:  
  - HTML, CSS, and JavaScript for a responsive and user-friendly interface.  
  - Deployed on **Netlify** for fast and reliable hosting.  

- **Backend**:  
  - Python (Flask) handles API requests and processes the data.  
  - Hosted on **Render** for scalability and performance.  

- **Data Source**:  
  - The app relies on **OpenStreetMap (OSM)** for mapping and location data.  

---
