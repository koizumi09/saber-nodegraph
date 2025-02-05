# Ultimate class for Nodes. This is where most of the stuff hapepens.
# All global variables and imports are done here.

from classes.base import Node, Element
from classes.pins import Pin, Parameter, Return, Exec
from classes.arrows import ValueFlow
from core import get_globals, get_imports, color_code, container_shapes

from importlib import import_module

# Import the initial import statements
import_elements = get_imports()

for import_element in import_elements:
    import_element = Element(import_element['id'])
    exec(import_element.text)

# Get the initial globals list and set variable_map and scope for later
global_variables = get_globals()
scope = "main"      # Stores the current scope of the variable to be stored. To be properly implemented
variable_map = {}   # Stores all the variables, their values and their scope

class Function(Node):
    def __init__(self, element_id):
        Node.__init__(self, element_id)

    def get_params(self):
        """Get the parameters required to execute this node's function. 
        Will recursively evaluate function returns, variables and expressions to get param values

        Returns:
            params: list of all the params required to run the given function
        """

        # This part currently is the core of this entire project, along with get_value()
        params = []
        for pin in self.pins['parameter']:
            pin = Parameter(pin)
            node = Element(pin.trace_value())

            if node.type == 'return':
                node = Return(node.id)
                node = Function(node.container)
                params.append(eval(node.execute()))
            
            if node.type == 'variable':
                node = Variable(node.id)
                params.append(eval(node.get_value()))
        
            if node.type == 'expression':
                node = Expression(node.id)
                params.append(eval(node.get_value()))
        
        return params
    
    def next(self):
        """Handles the case of multiple exec pins. Calls the generic next() method of
        its super class if multiple exec pins are not present.

        Returns:
            str: Element ID of the next node
        """
        next = None

        # If there are multiple exec pins, find the one that has 
        # text that matches exactly the return of the executed function.
        if len(self.pins['exec']) >= 2:
            for exec_pin in self.pins['exec']:
                exec_pin = Exec(exec_pin)
                if eval(exec_pin.text) == self.return_value:
                    next = exec_pin.next()

        else:
            next = super().next()

        return next

    def execute(self):
        """Runs the function and imports any methods required. God help me
        when its time to make the class method implementation of this...

        Returns:
            any: Return value of the function executed.
        """
      
        params = self.get_params()

        if "." in self.text:
            module, function = self.text.rsplit(".", 1) 
            module = import_module(module)
            function = getattr(module, function)
        else:
            function = eval(self.text)

        self.return_value = function(*params)

        return self.return_value

class Variable(Node):
    """Handles variables. I dunno what else to say, pretty straight.
    """
    def __init__(self, element_id):
        Node.__init__(self, element_id)

    def __has_sink(self):
        if not self.arrows:
            return False
        
        for arrow in self.arrows['value_flow']:
            arrow = ValueFlow(arrow)

            if arrow.source == self.id:
                return True
        
        return False
    
    def get_value(self):
        """Gets the value of the variable.
        Updates the variable_map
        creates a variable in the global namespace for expression evaluation
        Makes sure that the values are getting evaluated at the right place.

        Returns:
            any: current value of the variable
        """
        self.value = self.__get_value()

        if not self.__has_sink():
            if self.value and type(self.value) == str:
                self.value = eval(self.value)
            self.update_variable()
        
        if self.text not in variable_map[scope]: 
            if self.value and type(self.value) == str:
                self.value = eval(self.value)
            self.update_variable()
        
        return self.value
        
    def __get_value(self):
        """The biggest headache of this project, this helper for get_value is
        used for handling recursion and all the other special cases.
        I've tried documenting it to the best of my ability, but honestly it just works.
        """

        # CASE : When global variable == name of this node doesn't exist
        if self.text not in variable_map[scope]:
            # When no source is detected, initialize global with None
            if not self.source():
                return None
            # When source is detected, initialize global with source.value
            else:
                node = Node(self.source())
                if node.type == 'expression':
                    node = Expression(node.id)
                    return f"{node.get_value()}"
                else :
                    raise ValueError(f"""[Variable ID : {self.id}] Variables can only be initialized with an expression! 
                        Use Color : {color_code['node']['expression']} and Shape : {container_shapes} node for expression."""
                    )
                
        # CASE : When global variable == name of this node already exist
        if self.text in variable_map[scope]:
            # When no source is detected, value is what is stored in the global variable
            if not self.source():
                return f"{variable_map[scope][self.text]}"
            
            # When source is detected, value is calculated recursively by traversing the branch to the end
            else:
                if variable_map[scope][self.text] == None:
                    variable_map[scope][self.text] = ""

                # if self doesn't have a sink (i.e. it is the last element in a chain), then the value is overwritten
                if not self.__has_sink():
                    node = Node(self.source())
                        
                    if node.type == 'return':
                        node = Return(node.id)
                        node = Function(node.container)
                        return f"{node.execute()}"
                
                    if node.type == 'variable':
                        node = Variable(node.id)
                        return f"{node.get_value()}"
                    
                    if node.type == 'expression':
                        node = Expression(node.id)
                        return f"{node.get_value()}"
                    
                # if self has a sink (i.e. it is not the last element in a chain), then the value is 
                else :
                    node = Node(self.source())
                    if node.type == 'return':
                        node = Return(node.id)
                        node = Function(node.container)
                        return f"{node.execute()} {variable_map[scope][self.text]}"
                    
                    if node.type == 'variable':
                        node = Variable(node.id)
                        return f"{node.get_value()} {variable_map[scope][self.text]}"
                    
                    if node.type == 'expression':
                        node = Expression(node.id)
                        return f"{node.get_value()} {variable_map[scope][self.text]}"
                        
            return None
    
    def update_variable(self):
        """Update the global variable values and the variable_map dict
        """
        variable_map[scope][self.text] = self.value
        exec(f"global {self.text}; {self.text} = {self.value}")
    
    def execute(self):
        return self.get_value()

class Expression(Node):
    def __init__(self, element_id):
        Node.__init__(self, element_id)

    def get_value(self):
        if not self.source():
            return self.text

        node = Node(self.source())
        
        if node.type == 'function':
            node = Function(node.id)
            return f"{node.execute()} {self.text}"
        
        if node.type == 'variable':
            node = Variable(node.id)
            return f"{node.get_value()} {self.text}"
        
        if node.type == 'expression':
            node = Expression(node.id)
            return f"{node.get_value()} {self.text}"
            
        return None
    
# Read and create the global variables
variable_map[scope] = {}
for v in global_variables:
    v = Variable(v['id'])

    if v.get_value() == None:
        variable_map[scope][v.text] = None
        exec(f"{v.text} = {variable_map[scope][v.text]}")
        continue
    
    variable_map[scope][v.text] = v.get_value()
    exec(f"{v.text} = {variable_map[scope][v.text]}")

   