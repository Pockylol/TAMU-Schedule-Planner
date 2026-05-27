import easyocr
import tkinter as tk
from tkinter import filedialog
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="torch")

building_directory = {
   "ACAD": "Academic Building",
    "AGLS": "Agriculture & Life Sciences Building",
    "AIEN": "AI Engineering Building",
    "ALLN": "Allen Building (Bush School & Political Science)",
    "ANTH": "Anthropology Building",
    "ARCA": "Langford Architecture Center Building A",
    "ARCB": "Langford Architecture Center Building B",
    "ARCC": "Langford Architecture Center Building C",
    "BICH": "Biochemistry / Biophysics Building",
    "BLOC": "Blocker Building",
    "BLTN": "Bolton Hall",
    "BSBE": "Biological Sciences Building East",
    "CHEM": "Chemistry Building",
    "CHEN": "Jack E. Brown Chemical Engineering Building",
    "CVLB": "Civil Engineering / Texas Transportation Institute Building",
    "EABA": "Engineering Activities Buildings A",
    "EABB": "Engineering Activities Buildings B",
    "EABC": "Engineering Activities Buildings C",
    "EDCT": "Harrington Education Tower",
    "ETB": "Emerging Technologies Building",
    "EVANS": "Sterling C. Evans Library",
    "FRAN": "Francis Hall",
    "HALB": "Halbouty Geosciences Building",
    "HEB": "Haynes Engineering Building",
    "HECC": "Harrington Education Center Classroom Building",
    "HELD": "Heldenfels Hall",
    "HPCT": "Heep Center (Soil & Crop Sciences)",
    "HRBB": "Bright Building",
    "ILCB": "Innovative Learning Classroom Building",
    "ILSB": "Interdisciplinary Life Sciences Building",
    "ILSQ": "Instructional Laboratory & Innovative Learning Building",
    "KLCT": "Kleberg Center (Animal & Food Sciences)",
    "LAAH": "Liberal Arts & Humanities Building",
    "MPHY": "Mitchell Physics Building",
    "MSC": "Memorial Student Center",
    "OMB": "O & M Building (Eller Oceanography & Meteorology)",
    "PSYC": "Psychology Building",
    "RECH": "Student Recreation Center",
    "SCC": "Student Computing Center",
    "SCTS": "Scoates Hall",
    "WCBA": "Wehner Building (Mays Business School)",
    "YMCA": "YMCA Building",
    "ZACH": "Zachry Engineering Education Complex"}

def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select an Image to Scan",filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.webp")])

    if not file_path:
        print("No file selected.")
        return 

    print(f"Selected file: {file_path}")

    return file_path



reader = easyocr.Reader(['en'], gpu = False)


def find_buildings(image_path):
    result = reader.readtext(image_path, detail = 0)
    buildings_found = []
    for word in result:    
        for abbreviation in building_directory:
            if abbreviation in word.upper():
                full_name = building_directory[abbreviation]
                buildings_found.append(full_name)

    return "\n".join(buildings_found)

    


if __name__ == "__main__":
    file_path = select_file()
    if file_path:
        text = find_buildings(file_path)
        print("\n")
        print("---TAMU Buildings Found---")
        print(text)
