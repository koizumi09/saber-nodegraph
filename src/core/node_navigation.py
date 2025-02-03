import core.coordinate_math as cm
from core import color_code, text_elements, drawing


# ------------------- Getters and Setters ---------------------------

def get_drawing():
    global drawing
    return drawing

def set_drawing(drawing_new):
    global drawing
    drawing = drawing_new

def get_text_elements():
    global text_elements
    return text_elements

def set_text_elements(text_elements_new):
    global text_elements
    text_elements = text_elements_new

# ------------------- Methods ---------------------------

def get_element_id_by_text(text):
    id = None

    for key in text_elements.keys():
        if text_elements[key] == text:
            id = key
            break

    if not id:
        return None

    for element in drawing["elements"]:
        if (element['boundElements']):
            for bound_element in element['boundElements']:
                if (bound_element['type'] == 'text' and bound_element['id'] == id):
                    return element["id"]
                
def get_element_by_id(id):
    for element in drawing["elements"]:
        if (element["id"] == id):
            return element
    return None
                
def next(element_id):
    element = get_element_by_id(element_id)
    if (element['boundElements']):
        for bound_element in element['boundElements']:
            if (bound_element['type'] == 'arrow'):
                arrow = get_element_by_id(bound_element['id'])
                if arrow['strokeColor'] == color_code['control_flow']:
                    if arrow['endBinding']['elementId'] != element_id:
                        return arrow['endBinding']['elementId']
    return None
    
def prev(element_id):
    element = get_element_by_id(element_id)
    if (element['boundElements']):
        for bound_element in element['boundElements']:
            if (bound_element['type'] == 'arrow'):
                arrow = get_element_by_id(bound_element['id'])
                if arrow['strokeColor'] == color_code['control_flow']:
                    if arrow['startBinding']['elementId'] != element_id:
                        return arrow['startBinding']['elementId']
    return None

def connected(element_id):
    element = get_element_by_id(element_id)
    if (element['boundElements']):
        for bound_element in element['boundElements']:
            if (bound_element['type'] == 'arrow'):
                arrow = get_element_by_id(bound_element['id'])
                if arrow['strokeColor'] == color_code['parameter_flow']:
                    if arrow['startBinding']['elementId'] == element_id:
                        return arrow['endBinding']['elementId']
                    else:
                        return arrow['startBinding']['elementId']
    return None

def get_group_element_ids(groupId):
    group_element_list = []
    for element in drawing["elements"]:
        if groupId in element["groupIds"]:
            group_element_list.append(element["id"])
    return group_element_list

def get_text(element_id):
    element = get_element_by_id(element_id)

    if not element['boundElements']:
        return None
    
    for bound_element in element['boundElements']:
        if bound_element['type'] == 'text':
            return text_elements[bound_element['id']]

def get_params(func_element_id):
    element = get_element_by_id(func_element_id)
    params = []

    print(f"    Getting Params for : {get_text(func_element_id)}")

    for inner_element in drawing["elements"]:
        if inner_element['type'] != 'rectangle':
            continue
        if not cm.is_inside(inner_element, element):
            continue
        if inner_element['strokeColor'] != color_code['parameter']:
            continue

        connected_element = connected(inner_element['id'])
        if connected_element:
            if get_element_type(connected_element) == 'function':
                function_element = get_outer_element(connected_element)
                print(f"Outer Element : {get_text(function_element)}")
                function_element_return = run_function(function_element)
                params.append(function_element_return)

            if get_element_type(connected_element) == 'literal':
                param = get_text(connected_element)
                param = eval(param)
                params.append(param)

    return params

def is_nested(element_id):
    element = get_element_by_id(element_id)
    nested = False

    for inner_element in drawing["elements"]:
        if not cm.is_inside(inner_element, element):
            continue
        nested = True
        break

    return nested

def get_outer_element(element_id):
    inner_element = get_element_by_id(element_id)
    
    for element in drawing["elements"]:
        if element['type'] != 'rectangle':
            continue
        if get_element_type(element_id) != 'function':
            continue
        if not cm.is_inside(inner_element, element):
            continue
        return element['id']
        
    return None

def get_inner_elements(element_id):
    element = get_element_by_id(element_id)
    inner_elements = []

    for inner_element in drawing["elements"]:
        if not cm.is_inside(inner_element, element):
            continue
        inner_elements.append(inner_element['id'])

    return inner_elements

def get_element_type(element_id):
    element = get_element_by_id(element_id)

    color = element['strokeColor']

    for key in color_code.keys():
        if color == color_code[key]:
            return key
        
def run_function(element_id):
    
    element = get_element_by_id(element_id)
    if element['strokeColor'] != color_code['function']:
        return None

    function = get_text(element_id)

    print(f"Function : {get_text(element_id)}")
    params = get_params(element_id)


    if "." in function:
        module, function = function.rsplit(".", 1) 
        function = getattr(eval(module), function)
    else:
        function = eval(function)

    return function(*params)





