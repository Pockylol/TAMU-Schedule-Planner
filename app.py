import os 
import re
import easyocr
from flask import Flask, render_template, request, redirect, url_for
from buildings import CAMPUS_BUILDINGS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'schedule_img' not in request.files:
            return redirect(request.url)
        
        file = request.files['schedule_img']
        if file.filename == '':
            return redirect(request.url)
            
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            
            detected_route = find_coords(file_path)
            
            if not detected_route:
                return redirect(request.url)
            
            return render_template('map.html', route=detected_route)

def find_coords(image_path):
    reader = easyocr.Reader(['en'], gpu = False)

   
    result = reader.readtext(image_path, detail=0)
    full_text = " ".join(result).upper()    
    
    extracted_text = full_text
    
   
    match_pattern = r'\b(' + '|'.join(CAMPUS_BUILDINGS.keys()) + r')\b'
    matched_abbrs = re.findall(match_pattern, extracted_text)
    
    seen = set()
    route_coordinates = []
    
    for abbr in matched_abbrs:
        if abbr not in seen:
            seen.add(abbr)
            
            building_info = CAMPUS_BUILDINGS[abbr]
            
            route_coordinates.append({
                "abbr": abbr,
                "name": building_info["name"],
                "coords": building_info["coords"] 
            })
            
    return route_coordinates


if __name__ == '__main__':
    # Force creation of the upload folder path
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Launch the web server
    app.run(debug=True)


