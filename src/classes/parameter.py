from core import color_code, drawing, get_element_by_id
from classes.element import Element

class Parameter(Element):
    def __init__(self, element_id):
        Element.__init__(self, element_id)
        
        if not self.validate_parameter(element_id):
            raise ValueError("Parameter not valid!")
        
        self.type = 'parameter'

    def validate_parameter(self, element_id):
        e = get_element_by_id(element_id)
        
        if e['type'] != 'rectangle':
            raise ValueError("Parameters can only be elements of 'type': 'rectangle'.")
        
        if e['strokeColor'] != color_code['parameter']:
            raise ValueError("Invalid stroke color for parameter")
        
        if not len(self.outer(get_first=False)):
            raise Exception("Parameter not inside a node!")

        return True
    
    def source(self):
        for bound_element in self.data['boundElements']:
            # Ignore if bound element is not an arrow
            if (bound_element['type'] != 'arrow'):
                continue
            
            arrow = get_element_by_id(bound_element['id'])

            if not arrow:
                continue
            
            # Ignore if arrow is not a flow control arrow
            if arrow['strokeColor'] != color_code['parameter_flow']:
                continue
            
            target = arrow['startBinding']['elementId']

            # If arrow's head isn't pointing to itself.
            # This is done because the arrow is a bound element for both the element it starts at and ends at. 
            if target == self.data['id']:
                continue
            
            return target
        
        return None
    
class ExecPin(Element):
    def __init__(self, element_id):
        Element.__init__(self, element_id)

        if not self.validate_parameter(element_id):
            raise ValueError("Return not valid!")
        
        self.type = 'return_value'

    def validate_parameter(self, element_id):
        e = get_element_by_id(element_id)
        if e['type'] != 'rectangle':
            raise ValueError("Exec pins can only be elements of 'type': 'rectangle'.")
        
        if e['strokeColor'] != color_code['in-built']:
            raise ValueError("Invalid stroke color for exec pin!")
        
        if not len(self.outer(get_first=False)):
            raise Exception("Exec pin not inside a node!")

        return True
    
    def next(self):
        for bound_element in self.data['boundElements']:
            if (bound_element['type'] != 'arrow'):
                continue
            
            arrow = get_element_by_id(bound_element['id'])
            if not arrow:
                continue

            # Ignore if arrow is not a flow control arrow
            if arrow['strokeColor'] != color_code['control_flow']:
                continue
            
            target = arrow['endBinding']['elementId']

            # If arrow's tail isn't pointing to itself 
            # This is done because the arrow is a bound element for both the element it starts at and ends at. 
            if target != self.data['id']:
                return target
            
        return None
    # def next(self):
    #     for bound_element in self.data['boundElements']:
    #         if (bound_element['type'] != 'arrow'):
    #             continue
            
    #         arrow = get_element_by_id(bound_element['id'])

    #         # Ignore if arrow is not a flow control arrow
    #         if arrow['strokeColor'] != color_code['parameter_flow']:
    #             continue
            
    #         target = arrow['endBinding']['elementId']

    #         # If arrow's tail isn't pointing to itself 
    #         # This is done because the arrow is a bound element for both the element it starts at and ends at. 
    #         if target != self.data['id']:
    #             return target
            
    #     return None

