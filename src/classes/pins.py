from classes.base import Pin, Arrow
from core import color_code

class Parameter(Pin):
    def __init__(self, element_id):
        Pin.__init__(self, element_id)

        if self.color != color_code['pin']['parameter']:
            raise ValueError(f"[Parameter Pin ID : {self.id}] Invalid Color! Must be {color_code['pin']['parameter']}")
        
    def trace_value(self):
        for arrow in self.arrows['value_flow']:
            arrow = Arrow(arrow)

            if arrow.target == self.id:
                return arrow.source

        return None
    


class Return(Pin):
    def __init__(self, element_id):
        Pin.__init__(self, element_id)

        if self.color != color_code['pin']['return']:
            raise ValueError(f"[Return Pin ID : {self.id}] Invalid Color! Must be {color_code['pin']['return']}")


class Exec(Pin):
    def __init__(self, element_id):
        Pin.__init__(self, element_id)

        if self.color != color_code['pin']['exec']:
            raise ValueError(f"[Exec Pin ID : {self.id}] Invalid Color! Must be {color_code['pin']['exec']}")
        
        if not self.text:
            raise ValueError(f"[Exec Pin ID : {self.id}] No text detected! Exec pins must have a single bound or grouped text element.")
  
    def next(self):
        
        for arrow in self.arrows['control_flow']:
            arrow = Arrow(arrow)

            if arrow.source == self.id:
                return arrow.target

        return None
