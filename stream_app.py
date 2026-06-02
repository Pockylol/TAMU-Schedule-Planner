import os
import re
import easyocr
import requests
import streamlit as st
import folium
from streamlit_folium import st_folium
from buildings import CAMPUS_BUILDINGS

st.set_page_config(page_title="Aggie Schedule Map", layout="centered")

if "route_map" not in st.session_state:
    st.session_state.route_map = None
if "route_summary" not in st.session_state:
    st.session_state.route_summary = None
if "last_uploaded_file" not in st.session_state:
    st.session_state.last_uploaded_file = None


st.markdown("""
    <style>
    .stApp { 
        background-color: #500000; 
    }
    
    .main .block-container {
        padding-top: 6rem !important;
        padding-bottom: 6rem !important;
        display: flex !important;
        justify-content: center !important;
    }
    
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #333333 !important;
        padding: 40px !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 22px rgba(0, 0, 0, 0.3) !important;
        width: 100% !important;
        max-width: 700px !important;
        box-sizing: border-box !important;
    }        
    
    div[data-testid="stBaseButton-secondary"] {
        background-color: #F0F2F6 !important; 
        color: #262730 !important;           
        border: 1px solid rgba(49, 51, 63, 0.2) !important; 
    }            
            
    div[data-testid="stBaseButton-secondary"]:hover {
        background-color: #999ba1 !important; 
        border: 1px solid #500000 !important;  
        color: #500000 !important;
        opacity: 1 !important;
                    
    }
    
    .card-wrapper {
        background-color: #262730 !important;
        padding: 40px !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 22px rgba(0, 0, 0, 0.3) !important;
        width: 100% !important;
        max-width: 700px !important;
        box-sizing: border-box !important;
    }
    
    .card-wrapper label[data-testid="stWidgetLabel"] {
        color: #333333 !important;
    }
    
    .route-summary-card {
        background-color: #262730 !important;
        border-left: 5px solid #500000 !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
        border-radius: 6px !important;
    }
    
    </style>
""", unsafe_allow_html=True)

def find_coords(image_bytes):

    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(image_bytes, detail=0)
    full_text = " ".join(result).upper()    
    
    match_pattern = r'\b(' + '|'.join(CAMPUS_BUILDINGS.keys()) + r')\b'
    matched_abbrs = re.findall(match_pattern, full_text)
    
    seen = set()
    matched_buildings = []
    
    for abbr in matched_abbrs:
        if abbr not in seen:
            seen.add(abbr)
            building_info = CAMPUS_BUILDINGS[abbr]
            matched_buildings.append({
                "abbr": abbr,
                "name": building_info["name"],
                "coords": building_info["coords"] 
            })
    return matched_buildings


def get_walking_route(stops_list, metadata_list):

    base_url = "https://routing.openstreetmap.de/routed-foot/trip/v1/foot/"
    formatted_coords = [f"{pt[1]},{pt[0]}" for pt in stops_list]
    loc_string = ";".join(formatted_coords)


    params = {"overview": "full", 
              "geometries": "geojson", 
              "steps": "true", 
              "source": "any",
            "destination": "any"}
    
    url = f"{base_url}{loc_string}"

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("code") == "Ok":
            trip = data["trips"][0]
            distance_miles = round(trip["distance"]/ 1609.34, 2)
            duration_minutes = round(trip["duration"]/60,1)
            geometry = trip["geometry"]["coordinates"]
            
            summary_info = {
                "distance_miles": distance_miles,
                "duration_minutes": duration_minutes,
                "stops": [f"{item['name']} ({item['abbr']})" for item in metadata_list],
                "single": False
            }

            folium_geometry = [[coord[1], coord[0]] for coord in geometry]

            folium_map = folium.Map(location= stops_list[0], zoom_start=15)
            popup_text = f"Distance: {distance_miles} mi, Duration: {duration_minutes} min"
            popup = folium.Popup(popup_text, max_width=300)
            folium.PolyLine(locations= folium_geometry, color = 'maroon', weight = 5, popup = popup).add_to(folium_map)
            
            for index, building in enumerate(metadata_list):
                
                coords = building["coords"]
                building_name = building["name"]
                building_abbr = building["abbr"]

                label = f" {building_name} ({building_abbr})"

                if index == 0:
                    label = f"{building_name} ({building_abbr})"

                folium.Marker(
                    location=coords,
                    popup=label,
                    icon=folium.Icon(color="darkred", icon="info-sign"),
                ).add_to(folium_map)
                
            return folium_map._repr_html_(), summary_info
        
        else:
            st.error(f"OSRM API Error: {data.get('code')}")
            return None, None
    except requests.exceptions.RequestException as e:
        st.error(f"HTTP Request failed: {e}")
        return None, None



def render_output_display():
    if st.session_state.route_map is not None:
        summary = st.session_state.route_summary
        
        if summary and not summary.get("single", False):
            stops_html_list = "".join([f"<li style='color: #333333 !important;'>{stop}</li>" for stop in summary["stops"]])
            
            st.markdown(f"""
                <div class="route-summary-card">
                    <h3 style="color: #500000 !important; margin-top: 0;">Route Directions Summary</h3>
                    <p style="text-align: left; margin-bottom: 5px; color: #333333 !important;"><b> Estimated Duration:</b> {summary['duration_minutes']} minutes</p>
                    <p style="text-align: left; margin-bottom: 5px; color: #333333 !important;"><b> Total Distance:</b> {summary['distance_miles']} miles</p>
                    <p style="text-align: left; margin-bottom: 5px; color: #333333 !important;"><b> Buildings Found:</b></p>
                    <ul>
                        {stops_html_list}
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        
        st.components.v1.html(st.session_state.route_map, width=620, height=500)


with st.container():
    #st.markdown('<div class="center-card">', unsafe_allow_html=True)
    st.markdown('<h1 style="color: #FFFFFF; text-align: center; margin-bottom: 10px;">Aggie Schedule Map</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #FFFFFF; text-align: center; margin-bottom: 25px;">Upload a screenshot of class schedule from Howdy or Aggie Schedule Builder to generate route.</p>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choose your schedule screenshot...", type=["png", "jpg", "jpeg"])

    if uploaded_file != st.session_state.last_uploaded_file:
        st.session_state.route_map = None
        st.session_state.route_summary = None
        st.session_state.last_uploaded_file = uploaded_file

    if uploaded_file is not None:
        search_button = st.button("Generate Campus Walking Route")

        if search_button:
            with st.spinner("Finding buildings..."):
                image_bytes = uploaded_file.read()
                detected_buildings = find_coords(image_bytes)
                    
            if detected_buildings:
                st.success(f"Successfully found {len(detected_buildings)} campus buildings!")
                stops_coordinates = [item["coords"] for item in detected_buildings]            
                    
                if len(stops_coordinates) > 1:
                    final_map, summary = get_walking_route(stops_coordinates, detected_buildings)
                        
                    if final_map and summary:
                        st.session_state.route_map = final_map
                        st.session_state.route_summary = summary

                else:
                    single_map = folium.Map(location=stops_coordinates[0], zoom_start=16)
                    folium.Marker(
                        location=stops_coordinates[0], 
                        popup=detected_buildings[0]['name'],
                        icon =folium.Icon(color="darkred", icon="info-sign")
                    ).add_to(single_map)
                    st.session_state.route_map = single_map._repr_html_()
                    st.session_state.route_summary = {"single": True}
            else:
                st.error("No valid TAMU building abbreviations detected in the image file.")

        render_output_display()
    
         