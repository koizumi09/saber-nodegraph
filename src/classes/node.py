from core import color_code, get_element_by_id, get_imports, get_globals
from classes.element import Element
from classes.parameter import Parameter, ExecPin
from libraries.control_flow_library import *
from importlib import import_module

import_elements = get_imports()

for import_element in import_elements:
    import_element = Element(import_element['id'])
    exec(import_element.text)

class Node(Element):
    def __init__(self, element_id):
        Element.__init__(self, element_id)

        if not self.validate_node(element_id):
            raise ValueError("Element not a valid node!")
        
        self.param_pins = self.__has_multiple_exec_pins()
        if self.__get_exec_pins():
            self.exec_pins = self.__get_exec_pins()
        
        self.type = self.get_type()

    # ---------- Navigation ----------- #
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
    
    def previous(self):
        for bound_element in self.data['boundElements']:
            # Ignore if bound element is not an arrow
            if (bound_element['type'] != 'arrow'):
                continue

            arrow = get_element_by_id(bound_element['id'])
            
            # Ignore if arrow is not a flow control arrow
            if arrow['strokeColor'] != color_code['control_flow']:
                continue
            
            target = arrow['startBinding']['elementId']

            # If arrow's head isn't pointing to itself.
            # This is done because the arrow is a bound element for both the element it starts at and ends at. 
            if target != self.data['id']:
                return target
            
            
        return None

    # ---------- Validation ----------- #
    def validate_node(self, element_id):
        # For an element to be a node, it needs to satisfy the following conditions :
        # 1. It should be a rectangle.
        # 2. It should have a color corresponding to function or expression
        # 3. It should have text
        element = get_element_by_id(element_id)

        if element['type'] != 'rectangle':
            raise ValueError("Nodes can only be elements of 'type': 'rectangle'.")
        
        if element['strokeColor'] not in [color_code['function'], color_code['expression'], color_code['in-built']]:
            raise ValueError("Node is not the right color for function or expression")
        
        if not self._has_text():
             raise ValueError("Node has no bound text!")
        
        return True

    # ---------- Text ----------- #
    
                
    # ---------- Type Identification ----------- #
    def get_type(self):
        # TODO : Better implementation
        if not hasattr(self, "type"):
            if self.data['strokeColor'] == color_code['function']:
                return 'function'
            if self.data['strokeColor'] == color_code['expression']:
                return 'expression'
            if self.data['strokeColor'] == color_code['in-built']:
                if hasattr(self, 'exec_pins'):
                    return 'in-built'
                else:
                    return 'variable'
    
        return self.type

    
    def __get_param_pins(self):
        param_pins = []
        for e in self.inner():
            if e.is_type('parameter') and e.data['type'] == 'rectangle':
                param_pins.append(Parameter(e.data['id']))
        return param_pins
    
    def get_params(self):
        params = []

        # print(f"Getting Params for : {self.text}")

        for param_pin in self.__get_param_pins():
            if not param_pin.source():
                continue
            source_element = Element(param_pin.source())
            if source_element.is_type('function'):
                func_element = Node(source_element.outer().id)
                params.append(func_element.run_function())

            if source_element.is_type('expression'):
                expression_element = Expression(source_element.id)
                params.append(eval(expression_element.value))

            if source_element.is_type('variable'):
                variable_element = Variable(source_element.id)
                params.append(eval(variable_element.value))

        #print(f"{self.text} Params : {params}")
        return params
    
    def __has_multiple_exec_pins(self):
        if hasattr(self, "exec_pins"):
            return True
    
        pin_counter = 0
        for e in self.inner():
            if e.data['strokeColor'] == color_code['in-built'] and e.data['type'] == 'rectangle':
                pin_counter += 1
            if pin_counter >= 2:
                break
        if pin_counter >= 2:
            return True
        else:
            return False

    def __get_exec_pins(self):
        exec_pins = []
        for e in self.inner():
            if e.data['strokeColor'] == color_code['in-built'] and e.data['type'] == 'rectangle':
                exec_pins.append(ExecPin(e.data['id']))
        return exec_pins
    
    def run_function(self):
        if self.text == "Start":
            self.next_node = Node(self.next())
            return None

        if self.type == 'variable':
            variable = Variable(self.id)
            self.next_node = Node(variable.next())
            return variable.value

        params = self.get_params()

        if "." in self.text:
            module, function = self.text.rsplit(".", 1) 
            module = import_module(module)
            function = getattr(module, function)
        else:
            function = eval(self.text)

        return_value = function(*params)

        if self.__has_multiple_exec_pins():
            for exec_pin in self.exec_pins:
                if eval(exec_pin._get_text()) == return_value:
                    next_element = Element(exec_pin.next())
                    if next_element.is_type(['function', 'variable']):
                        self.next_node = Node(next_element.id)

            
        else:
            self.next_node = self.next()

        return return_value

class Variable(Element):
    def __init__(self, element_id):
        Element.__init__(self, element_id)

        if not self.validate_node(element_id):
            raise ValueError("Element not a valid Variable!")
        
        self.value = self.__get_value()
        if not self.sink():
            if self.value and type(self.value) == str:
                self.value = eval(self.value)
            self.update_variable()
        
        if self.text not in globals(): 
            if self.value:
                self.value = eval(self.value)
            self.update_variable()

    # ---------- Navigation ----------- #
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
    
    def sink(self):
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
            
            target = arrow['endBinding']['elementId']

            # If arrow's head isn't pointing to itself.
            # This is done because the arrow is a bound element for both the element it starts at and ends at. 
            if target == self.data['id']:
                continue
            
            return target
        
        return None
    
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

    # ---------- Validation ----------- #
    def validate_node(self, element_id):
        # For an element to be a node, it needs to satisfy the following conditions :
        # 1. It should be a rectangle.
        # 2. It should have a color corresponding to function or literal
        # 3. It should have text
        element = get_element_by_id(element_id)

        if element['type'] != 'rectangle':
            raise ValueError("Nodes can only be elements of 'type': 'rectangle'.")
        
        if element['strokeColor'] not in [color_code['in-built']]:
            raise ValueError("Node is not the right color for function or literal")
        
        if not self._has_text():
             raise ValueError("Node has no bound text!")
        
        return True

    def __get_value(self):
      
        # CASE : When global variable == name of this node doesn't exist
        if self.text not in globals(): 
            # When no source is detected, initialize global with None
            if not self.source():
                return None
            # When source is detected, initialize global with source.value
            else:
                source = Element(self.source())
                if source.is_type('expression'):
                    source = Expression(source.id)
                    return f"{source.value}"
            
        # CASE : When global variable == name of this node already exist
        if self.text in globals():
            # When no source is detected, value is what is stored in the global variable
            if not self.source():
                return f"{globals()[self.text]}"
            # When no source is detected, value is calculated recursively by traversing the branch to the end
            else:
                if globals()[self.text] == None:
                    globals()[self.text] = ""

                # if self doesn't have a sink (i.e. it is the last element in a chain), then the value is overwritten
                if not self.sink():
                    source = Element(self.source())
                    if source.is_type('expression'):
                        source = Expression(source.id)
                        return f"{source.value}"
                    if source.is_type('function'):
                        source = Node(source.outer().id)
                        return f"{source.run_function()}"
                    if source.is_type('variable'):
                        source = Variable(source.id)
                        return f"{source.value}" 
                # if self has a sink (i.e. it is not the last element in a chain), then the value is 
                else :
                    source = Element(self.source())
                    if source.is_type('expression'):
                        source = Expression(source.id)
                        return f"{source.value} {globals()[self.text]}"
                    if source.is_type('function'):
                        source = Node(source.outer().id)
                        return f"{source.run_function()} {globals()[self.text]}"
                    if source.is_type('variable'):
                        source = Variable(source.id)
                        return f"{source.value} {globals()[self.text]}"   

        return None
    
    def update_variable(self):
        globals()[self.text] = self.value

class Expression(Element):
    def __init__(self, element_id):
        Element.__init__(self, element_id)

        if not self.validate_node(element_id):
            raise ValueError("Element not a valid Expression!")
        
        self.value = self.__get_value()
        

    # ---------- Navigation ----------- #
    def next(self):
        for bound_element in self.data['boundElements']:
            if (bound_element['type'] != 'arrow'):
                continue
            
            arrow = get_element_by_id(bound_element['id'])
            if not arrow:
                continue

            # Ignore if arrow is not a flow control arrow
            if arrow['strokeColor'] != color_code['parameter_flow']:
                continue
            
            target = arrow['endBinding']['elementId']

            # If arrow's tail isn't pointing to itself 
            # This is done because the arrow is a bound element for both the element it starts at and ends at. 
            if target != self.data['id']:
                return target
            
        return None
    
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

    # ---------- Validation ----------- #
    def validate_node(self, element_id):
        # For an element to be a node, it needs to satisfy the following conditions :
        # 1. It should be a rectangle.
        # 2. It should have a color corresponding to function or literal
        # 3. It should have text
        element = get_element_by_id(element_id)

        if element['type'] != 'rectangle':
            raise ValueError("Nodes can only be elements of 'type': 'rectangle'.")
        
        if element['strokeColor'] not in [color_code['expression']]:
            raise ValueError("Node is not the right color for function or literal")
        
        if not self._has_text():
             raise ValueError("Node has no bound text!")
        
        return True

    def __get_value(self):
        
        if not self.source():
            return self.text
        
        source = Element(self.source())

        if source.is_type('expression'):
            source = Expression(source.id)
            return f"{source.value}{self.text}"
        
        if source.is_type('variable'):
            source = Variable(source.id)
            return f"{source.value}{self.text}"
        
        if source.is_type('function'):
            source = Node(source.outer().id)
            return f"{source.run_function()}{self.text}"
        
        return None
    

global_variables = get_globals()

for variable_element in global_variables:
    variable_element = Variable(variable_element['id'])
    exec(f"{variable_element.text} = {variable_element.value}")