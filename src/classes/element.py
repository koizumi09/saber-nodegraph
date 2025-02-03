from core import color_code, drawing, get_element_by_id
from math import dist

class Element:
    def __init__(self, element_id):
        self.id = element_id

        if not self.validate_element():
            raise ValueError("Element not a valid node!")
        
        self.data = get_element_by_id(element_id)
        self.grouped_elements = self._find_grouped_elements()
        if self._has_text():
            self.text = self._get_text()
   

    # ---------- Validation ----------- #
    def validate_element(self):
        # For an element to be a node, it needs to satisfy the following conditions :
        # 1. It should be a rectangle.
        # 2. It should have a color corresponding to function or literal
        # 3. It should have text
        element = get_element_by_id(self.id)

        if not element:
            return False
        
        if element['strokeColor'] not in color_code.values():
            raise ValueError("Element stroke color not in color code library!")

        return True
    
    # ------------ Geometry --------------- #
    def get_corners(self):
        oo = (self.data['x'], self.data['y'])
        oy = (self.data['x'] + self.data['width'], self.data['y'])
        xy = (self.data['x'] + self.data['width'], self.data['y'] + self.data['height'])
        xo = (self.data['x'], self.data['y'] + self.data['height'])

        return [oo, oy, xo, xy]
    
    def is_inside(self, container):
        # if isinstance(container, Element):
        #     raise TypeError("Container isn't a valid element class object.")
        
        target = self.get_corners()
        container = container.get_corners()

        x_bound = (container[0][0], container[1][0])
        y_bound = (container[0][1], container[3][1])

        if target[0][0] < x_bound[0]:
            return False
        if target[1][0] > x_bound[1]:
            return False
        if target[0][1] < y_bound[0]:
            return False
        if target[3][1] > y_bound[1]:
            return False
        
        return True
    
    def __get_closest_nesting(self, containers):
        target_corners = self.get_corners()
        first = True
        min = None
        for container in containers:
            corners = container.get_corners()
            for i in range(0, len(corners)):
                difference = dist(corners[i], target_corners[i])
                if first:
                    first = False
                    min = difference
                    min_container = container
                if difference < min:
                    min = difference
                    min_container = container
        
        if min != None:
            return min_container
        else:
            return None
    
    def outer(self, get_first = True):
        containers = []

        for e in drawing['elements']:
            if e['id'] == self.id:
                continue
            if e['type'] not in ['rectangle']:
                continue

            e = Element(e['id'])

            if self.is_inside(e) and e.data['type'] == 'rectangle':
                containers.append(e)
        
        if get_first:
            return self.__get_closest_nesting(containers)
        else:
            return containers

    def inner(self, get_first = False):
        inner_elements = []

        for e in drawing["elements"]:
            if e['id'] == self.id:
                continue
            if e['type'] not in ['rectangle', 'text']:
                continue

            e = Element(e['id'])

            if e.is_inside(self):
                inner_elements.append(e)

        if get_first:
            return self.__get_closest_nesting(inner_elements)
        else:
            return inner_elements

    # ------------- Grouping --------------------- #
    def _find_grouped_elements(self):
        grouped_elements = {}
        for group_id in self.data['groupIds']:
            grouped_elements[group_id] = []
            for element in drawing['elements']:
                if group_id in element['groupIds']:
                    grouped_elements[group_id].append(element['id'])

        return grouped_elements
    
    # -------------------- Text -------------------- #    
    def _has_text(self):
        if not hasattr(self, 'data'):
            bound_elements = get_element_by_id(self.id)['boundElements']
        else:
            if self.data['boundElements']:
                bound_elements = self.data['boundElements']
            else :
                bound_elements = []

        has_text = False

        for bound_element in bound_elements:
            if bound_element['type'] == 'text':
                has_text = True

        if not self.grouped_elements:
            return has_text
        
        for group in self.grouped_elements.keys():
            has_text_element = False
            has_other_element = False
            if len(self.grouped_elements[group]) == 2:
                for element_id in self.grouped_elements[group]:
                    element = get_element_by_id(element_id)
                    if element['type'] == 'text':
                         has_text_element = True
                    else:
                        has_other_element = True
                if has_text_element and has_other_element:
                    has_text = True

        return has_text   
    
    def _get_text(self):

        if self.data['boundElements']:
            for bound_element in self.data['boundElements']:
                if bound_element['type'] == 'text':
                    text_element = get_element_by_id(bound_element['id'])
                    if text_element['rawText']:
                        return text_element['rawText']
                    else:
                        return text_element['text']
                
            
        for group in self.grouped_elements.keys():
            has_text_element = False
            has_other_element = False
            text = ""
            if len(self.grouped_elements[group]) == 2:
                for element_id in self.grouped_elements[group]:
                    element = get_element_by_id(element_id)
                    if element['type'] == 'text':
                        has_text_element = True
                        text_element = get_element_by_id(element['id'])
                        text = text_element['rawText']
                    else:
                        has_other_element = True
                if has_text_element and has_other_element:
                    return text
        return ""
    
    def is_type(self, type_name):
        if type(type_name) == str:
            if self.data['strokeColor'] == color_code[type_name]:
                return True
            else:
                return False
            
        type_name_list = []
        for t in type_name:
            type_name_list.append(color_code[t])

        if self.data['strokeColor'] in type_name_list:
            return True
        else:
            return False
            
    