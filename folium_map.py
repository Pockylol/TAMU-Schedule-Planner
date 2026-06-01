from buildings import CAMPUS_BUILDINGS
import json
import requests
import folium 
import os

places = dict(list(CAMPUS_BUILDINGS.items())[:3])

def get_folium_map(center_point = (30.612392556898126, -96.34156870472945), points: dict = None, zoom_level: int = 14):
    if points is None:
        points = places

    folium_map = folium.Map(location= [center_point[0], center_point[1]], zoom_start=zoom_level)

    for code, info in points.items():
        name = info["name"]  # Extracts long name
        coords = info["coords"]  # Extracts (lat, lon) tuple

        # Folium accepts the tuple directly for location
        folium.Marker(location=coords, popup=name).add_to(folium_map)

    return folium_map

my_map = get_folium_map()

script_dir = os.path.dirname(os.path.abspath(__file__))
map_path = os.path.join(script_dir, "map.html")
my_map.save(map_path)
print(f"Map saved to {map_path}")
