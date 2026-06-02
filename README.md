# Aggie Schedule Map

An interactive web application that transforms a static Texas A&M class schedule screenshot into a customized, optimized pedestrian navigation route across the College Station campus. Built using Python, Streamlit, EasyOCR, and the Open Source Routing Machine (OSRM) API.


---

 **[View the Live App on Streamlit Cloud](https://tamu-schedule-map.streamlit.app/)**

---

## Features
* **Automated Schedule Parsing:** Utilizes `EasyOCR` to scan uploaded schedule images (.png, .jpg, .jpeg) and extract official TAMU building abbreviations (e.g., *HECC*, *ZACH*, *ILCB*).
* **Sidewalk Routing:** Connects campus coordinates using the `OSRM` network engine, drawing realistic walking tracks that follow sidewalks, crosswalks, and plazas rather than straight "as-the-crow-flies" lines.
* **Interactive Mapping:** Powered by `Folium` to plot sequential classroom locations with clear markers, interactive popups, and auto-adjusting map bounds.
* **Trip Metrics Summary:** Automatically calculates total walking distances (in miles) and estimated travel durations (in minutes) between classes to help students plan their passing periods.
---

## Tech Stack & Architecture
* **Frontend UI:** Streamlit (with custom injected global CSS overrides)
* **Text Extraction (OCR):** EasyOCR (Computer Vision / Deep Learning engine)
* **Geospatial Mapping:** Folium (Native mapping sheets canvas)
* **Navigation Engine:** Open Source Routing Machine (OSRM) Project Foot API
* **Data Layer:** Pre-compiled static Python dictionary mapping official TAMU building markers to `[Latitude, Longitude]` coordinates.

---
Because this app relies on EasyOCR for text recognition, the very first time you process an image, the application will take an extra 1–2 minutes to pull down the English language text-detection machine learning weights model into its server cache. Subsequent runs will process instantly.

