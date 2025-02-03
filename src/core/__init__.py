from core import markdown_parsers as mp
from os.path import splitext
text_elements = None
drawing = None

white = "#1e1e1e"
pink = "#e03131"
blue = "#1971c2"
green = "#2f9e44"
brown = "#f08c00"

color_code = {
    "in-built": white,
    "function": blue,
    "expression": green,
    "parameter": green,
    "variable": white,
    "return": blue,
    "control_flow": white,
    "parameter_flow": green
}

def read_drawing():

    global text_elements
    global drawing 

    with open("main.excalidraw", 'r') as file:
        file_content = file.read()
        #text_elements = mp.parse_text_elements(file_content)
        #drawing = mp.parse_drawing(file_content)
        drawing = mp.parse_json(file_content)
        pass

def get_element_by_id(id):
    for element in drawing["elements"]:
        if (element["id"] == id):
            return element
    return None

def get_start():
    for element in drawing["elements"]:
        if (element["type"] != "text"):
            continue
        if (element['text'] != "Start"):
            continue
        return element['containerId']
    return None

def get_imports():
    return get_frame_elements("Imports")

def get_globals():
    globals = []
    for element in get_frame_elements("Globals"):
        if element['strokeColor'] != color_code['variable']:
            continue
        globals.append(element)
    return globals
    

def get_frame_elements(frame_name: str):
    for element in drawing["elements"]:
        if (element["type"] != "frame"):
            continue
        if (element['name'] != frame_name):
            continue
        frame_id = element['id']
        break

    frame_elements = []
    for element in drawing["elements"]:
        if (element['frameId'] != frame_id):
            continue
        if (element['type'] != 'rectangle'):
            continue
        frame_elements.append(element)

    return frame_elements


read_drawing()