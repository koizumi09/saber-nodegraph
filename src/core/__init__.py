import json
from os.path import splitext

#drawing_file = "scrapbook.excalidraw"
drawing_file = "main.excalidraw"

drawing = None

colors = {
    "white" : "#1e1e1e",
    "pink" : "#e03131",
    "blue" : "#1971c2",
    "green" : "#2f9e44",
    "brown" : "#f08c00"
}

color_code = {
    'node': {
        "function": colors['blue'],
        "expression": colors['green'],
        "variable": colors['white'],
    },
    'arrow': {
        "control_flow": colors['white'],
        "value_flow": colors['green']
    },
    'pin': {
        "parameter": colors['green'],
        "return": colors['blue'],
        "exec": colors['white']
    }
}

connector_shapes = [
    'arrow',
]

container_shapes = [
    'rectangle',
    'diamond',
    'ellipse'
]

all_shapes = container_shapes + connector_shapes

# TODO : Implement parsing of different excalidraw files like .excalidraw.md etc.
def read_drawing():
    global drawing

    with open(drawing_file, 'r') as file:
        file_content = file.read()
        drawing = json.loads(file_content)
        
    return drawing

def get_colors():
    # TODO : Read from a config file
    pass 

def get_color_code():
    # TODO : Read from a config file
    pass


def get_element_by_id(id):
    # Gets element... by id
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
        if element['strokeColor'] != color_code['node']['variable']:
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
