# Contains basic classes derived from the element class. 
# Three Basic elements of a Saber graph : Arrows, Nodes and Pins

from core import color_code, get_element_by_id
from classes.element import Element

class Arrow(Element):
    """Base class for all arrows. 

    Attributes: 
        source : Element ID of the source of the arrow (where it starts from, usually the end without the pointer)
        target : Element ID of the target of the arrow (where it points to, usually the end with the pointer)
    """
    def __init__(self, element_id):
        Element.__init__(self, element_id)

        self.source = self.__set_source()
        self.target = self.__set_target()

    def __set_source(self):
        """Find, validate and return the element ID of the element where this arrow originates from.

        Returns:
            str: Element ID of the origin element
        """
        if not self.data['startBinding']:
            raise ValueError(f"[Arrow ID : {self.id}] Arrow has no start element!")
        
        return self.data['startBinding']['elementId']

    def __set_target(self):
        """Find, validate and return the element ID of the element where this arrow points to.

        Returns:
            str: Element ID of the target element
        """
        if not self.data['endBinding']:
            raise ValueError(f"[Arrow ID : {self.id}] Arrow has no end element!")
        
        return self.data['endBinding']['elementId']

class Pin(Element):
    """Base class for all pins.

    Attributes:
        container: Element ID of the geometric container of this pin.
        arrows: A dict of all the arrows bound to this pin
    """
    def __init__(self, element_id):
        Element.__init__(self, element_id)

        if self.inner():
            raise SyntaxError(f"[Pin ID : {self.id}] Inner elements not allowed in Pins!")

        self.container = self.__set_container()
        self.arrows = self.__set_arrows()


    def __set_container(self):
        if not self.outer():
            raise SyntaxError(f"[Pin ID : {self.id}] Pins must be in a node!")

        return self.outer().id
    
    def __set_arrows(self):
        if not len(self.bound_elements):
            return []
        
        arrows = {}
        for arrow_type in color_code['arrow'].keys():
            arrows[arrow_type] = []

        for e in self.bound_elements:
            if not get_element_by_id(e):
                continue
            
            e = Element(e)
            
            if e.type in color_code['arrow'].keys():
                arrows[e.type].append(e.id)
                
        return arrows
    
    def has_text(self):
        return hasattr(self, 'text')

class Node(Element):
    """Base class for all the functions, variables and expressions.

    Attributes:
        pins : dict of all the pins in this node
        arrows : dict of all the arrows bound to this node
    """
    def __init__(self, element_id):
        Element.__init__(self, element_id)

        if not hasattr(self, 'text'):
            raise ValueError(f"[Node Id : {self.id}] Nodes must have some text!")

        self.pins = self.__set_pins()
        self.arrows = self.__set_arrows()

        if not self.arrows and not self.pins:
            raise SyntaxError(f"[Node Id : {self.id}] Nodes must have at least one arrow or a pin with an arrow!")

    def __set_pins(self):

        pins = {}
        for pin_type in color_code['pin'].keys():
            pins[pin_type] = []

        for e in self.inner():
            e = Element(e)
            if e.type in color_code['pin'].keys():
                pins[e.type].append(e.id)
                
        return pins
    
    def __set_arrows(self):
        if not len(self.bound_elements):
            return []
        
        arrows = {}
        for arrow_type in color_code['arrow'].keys():
            arrows[arrow_type] = []

        for e in self.bound_elements:
            e = Element(e)
            if e.type in color_code['arrow'].keys():

                arrows[e.type].append(e.id)
        return arrows
    
    def next(self):
        # Returns the Element ID of the next node based on control flow arrows.
    
        if len(self.pins['exec']) >= 2:
            raise SyntaxError(f"""[Node Id : {self.id}] Node.next() only works with Nodes that have a single exec pin. \n
                              Please use Node.execute() instead.""")
        
        for arrow in self.arrows['control_flow']:
            arrow = Arrow(arrow)

            if arrow.source == self.id:
                return arrow.target

        return None
    
    def source(self):
        # Find the value source of the arrow. I.e Find the butt end of whatever arrow is pointing at this node.
        # In the context of values, source = where the value comes from and sink = where the value is supposed to go.
        
        if not self.arrows:
            return None

        for arrow in self.arrows['value_flow']:
            arrow = Arrow(arrow)

            if arrow.target == self.id:
                return arrow.source

        return None

    
    def execute(self):
        # Implemented in child classes of this class
        pass