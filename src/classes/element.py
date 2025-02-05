from core import colors, color_code, container_shapes, connector_shapes, drawing, get_element_by_id
from math import dist



class Element:
    """The base class for all elements in the drawing.

    Attributes :
        data (dict) : Dict from parsed JSON data of an excalidraw element.
        shape (str) : Shape of the element. Eg - 'rectangle', 'arrow' etc.
        color (str) : stroke color of the element. Must be defined in colors and color_code
        text (str) : Bound or grouped text of the element. If no text is detected, it defaults to None.
        type (str) : Element type based on usage - 'function', 'variable', 'control_flow' etc. Defined in color_code.
        grouped_elements (dict) : Key (str) - Group ID, Value (list) - List of all the element IDs of elements in the group, except self.
        bound_elements (list) : Element IDs of all the elements bound to this element

    Methods :
        Refer to method docstrings
    """

    def __init__(self, element_id):
        self.id = element_id

        data = get_element_by_id(self.id)
        
        if not data:
            self = None
            return 
            raise ValueError(f"[Element Id : {self.id}] Element Id not found in Drawing!")
            
        self.data = data

        self.grouped_elements = self.__set_grouped_elements()
        self.bound_elements = self.__set_bound_elements()
        
        self.shape = self.__set_shape()
        self.color = self.__set_color()
        self.text = self.__set_text()

        self.type = self.__set_type()

        
        
    # Geometry - Finding elements that are inside this element, or which element this element is inside of.

    def __get_corners(self):
        """ Get the absolute coordinates of the corners of this element

        Returns:
            list: [top_left, top_right, bottom_left, bottom_right]
        """
        oo = (self.data['x'], self.data['y'])
        oy = (self.data['x'] + self.data['width'], self.data['y'])
        xo = (self.data['x'], self.data['y'] + self.data['height'])
        xy = (self.data['x'] + self.data['width'], self.data['y'] + self.data['height'])
        
        return [oo, oy, xo, xy]
    
    def is_inside(self, container):
        """Check if self is geometrically inside container.

        Args:
            container (str or Element): Element object or string with Element ID

        Returns:
            bool
        """
        if not isinstance(container, Element):
            container = Element(container)

        target = self.__get_corners()
        container = container.__get_corners()

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
        """From a list of containers that self is inside, return the first nested container.
        Eg. If x is in y, and y is in z, x's container list will be [y, z]. This function will
        find and return y

        Args:
            containers (_type_): _description_

        Returns:
            _type_: _description_
        """
        target_corners = self.__get_corners()
        first = True
        min = None
        for container in containers:
            if not isinstance(container, Element):
                container = Element(container)
            corners = container.__get_corners()
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

            if self.is_inside(e):
                containers.append(e.id)
        
        if get_first:
            return self.__get_closest_nesting(containers)
        else:
            return containers

    def inner(self, get_first = False):
        inner_elements = []

        for e in drawing["elements"]:
            if e['id'] == self.id:
                continue
            if e['type'] not in ['rectangle']:
                continue
            if e['frameId']:
                continue

            e = Element(e['id'])

            if e.is_inside(self):
                inner_elements.append(e.id)

        if get_first:
            return self.__get_closest_nesting(inner_elements)
        else:
            return inner_elements

    # Initialization and Validation Methods 

    # Group Detection
    def __set_grouped_elements(self):
        """Retuns a dict with group ID as key and all the element IDs in that group as value.

        Returns:
            dict of list: Key- GroupID , Value- List of all the element IDs in that group.
        """
        if not self.data['groupIds']:
            return {}
        
        grouped_elements = {}
        
        for group_id in self.data['groupIds']:
            grouped_elements[group_id] = []
            for element in drawing['elements']:
                if group_id in element['groupIds']:
                    # Ignore element if it is itself, to avoid circular referencing
                    if element['id'] == self.id:
                        continue
                    grouped_elements[group_id].append(element['id'])

        return grouped_elements
    
    def __set_bound_elements(self):
        """Retuns a dict with group ID as key and all the element IDs in that group as value.
        NOTE : Ignores 'text' type objects because they're handled by __set_text() method

        Returns:
            dict of list: Key- GroupID , Value- List of all the element IDs in that group.
        """
        if not self.data['boundElements']:
            return []
        
        bound_elements = []
        
        for b in self.data['boundElements']:
            # Ignore element if it is itself, to avoid circular referencing
            if b['id'] == self.id:
                continue
            if b['type'] == 'text':
                continue
            bound_elements.append(b['id'])

        return bound_elements
     
    # Text
    def __has_text(self):
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
    
    def __set_text(self):
        """Returns the associated text with the element. 
        If element has bound text, it will be returned. 
        Else, if element is in a group with a single text element, it will be returned.

        Returns:
            str: Detected text
        """

        # Look for bound text element first
        if self.data['boundElements']:
            for bound_element in self.data['boundElements']:
                if bound_element['type'] == 'text':
                    text_element = get_element_by_id(bound_element['id'])
                    if text_element['rawText']:
                        return text_element['rawText']
                    else:
                        return text_element['text']
                
        # If no bound text element is found, look for a group where the only 
        # members are this element and a text element.
        for group in self.grouped_elements.keys():

            if len(self.grouped_elements[group]) == 1:
                for element_id in self.grouped_elements[group]:
                    element = get_element_by_id(element_id)
                    if element['type'] == 'text':
                        text_element = get_element_by_id(element['id'])

                        if text_element['rawText']:
                            return text_element['rawText']
                        else:
                            return text_element['text']
                
        return ""
    
    # Basic Properties
    def __set_color(self):
        """Validate and set the color property of this element

        Returns:
            str: Color if its valid
        """
        if self.data['strokeColor'] not in colors.values():
            raise ValueError(f"""[Element Id : {self.id}] Invalid Element Color! \n
                             Please pick a color from the following : {colors}\n
                             Or include your color in the color code""")
        
        return self.data['strokeColor']
    
    def __set_shape(self):
        """Validate and set the shape property of this element

        Returns:
            str: Shape if its valid
        """
        allowed_elements = container_shapes + connector_shapes
        if self.data['type'] not in allowed_elements:
            raise ValueError(f"""[Element Id : {self.id}] Invalid Element Type - {self.data['type']}. \n
                             Allowed drawing elements : {allowed_elements}\n
                             Or include your color in the color code""")
        return self.data['type']
    
    # Type
    def __set_type(self):
        """Called on __init__. Returns the type of this element based 
        on its shape, color and if it has text.

        Returns:
            str: Computed type of the element
        """
        if self.shape in container_shapes:
            if self.__has_text():
                for key in color_code['node'].keys():
                    if self.color == color_code['node'][key]:
                        return key
            else:
                for key in color_code['pin'].keys():
                    if self.color == color_code['pin'][key]:
                        return key       

        if self.shape in connector_shapes:
            for key in color_code['arrow'].keys():
                if self.color == color_code['arrow'][key]:
                    return key
    
            