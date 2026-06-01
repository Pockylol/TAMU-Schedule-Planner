import folium
import requests
from folium_map import get_folium_map
from buildings import CAMPUS_BUILDINGS
import os


def get_walking_route(stop_list):

    # Public OSRM API demo endpoint for foot profile
    base_url = "https://routing.openstreetmap.de/routed-foot/trip/v1/foot/"

    formatted_coords = [f"{pt[1]},{pt[0]}" for pt in stop_list]
    loc_string = ";".join(formatted_coords)


    params = {"overview": "full", "geometries": "geojson", "steps": "true", "source": "any",
        "destination": "any"}
    url = f"{base_url}{loc_string}"

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("code") == "Ok":
            trip = data["trips"][0]
            distance_miles = round(trip["distance"]/ 1609, 2)
            duration_minutes = round(trip["duration"]/60,1)
            geometry = trip["geometry"]["coordinates"]
            
            waypoints = data["waypoints"]
            sorted_waypoints = sorted(waypoints, key=lambda x: x["waypoint_index"])


            print(f"Status: Trip Found Successfully")
            print(f"Distance: {distance_miles} miles")
            print(f"Duration: {duration_minutes} minutes")
           
            folium_geometry = [[coord[1], coord[0]] for coord in geometry]

            
            folium_map = folium.Map(location= stop_list[0], zoom_start=14)
            popup_text = f"Distance: {distance_miles} mi, Duration: {duration_minutes} min"
            popup = folium.Popup(popup_text, max_width=300)
            folium.PolyLine(locations= folium_geometry, color = 'maroon', weight = 5, popup = popup).add_to(folium_map)
            
            for original_index, wp in enumerate(waypoints):
                visit_order = (wp["waypoint_index"] + 1)  # Add 1 so labels read Stop 1, Stop 2...
                coords = stop_list[original_index]

                label = f"Stop  #{visit_order}"
                if wp["waypoint_index"] == 0:
                    label = f"Start Here (Stop {visit_order})"
                    
                folium.Marker(location=coords,popup=label,icon=folium.Icon(color="darkred", icon="info-sign"),).add_to(folium_map)
            
            script_dir = os.path.dirname(os.path.abspath(__file__))
            map_path = os.path.join(script_dir, "route_map.html")
            folium_map.save(map_path)
            print(f"Route map saved to {map_path}")

            return 
        else:
            print(f"API Error: {data.get('code')}")

            return None
    except requests.exceptions.RequestException as e:

        print(f"HTTP Request failed: {e}")

        return None
    
stops = [(30.62303908680081, -96.33848659816275), (30.622928306006003, -96.33943452327294)
,(30.621307975737594, -96.34037866085333)]

route_json = get_walking_route(stops)




