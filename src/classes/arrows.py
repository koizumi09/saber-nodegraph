# The ultimate classes for Arrows. Mostly just used for validation at this point.

from core import color_code
from classes.base import Element, Arrow

class ValueFlow(Arrow):
    def __init__(self, element_id):
        Arrow.__init__(self, element_id)

        if self.color != color_code['arrow']['value_flow']:
            raise ValueError(f"[Value Arrow ID : {self.id}] Invalid Color! Must be {color_code['arrow']['value_flow']}")

        allowed_sources = ['variable', 'expression', 'return']
        allowed_targets = ['variable', 'expression', 'parameter']

        if self.source:
            if Element(self.source).type not in allowed_sources:
                raise ValueError(f"[Value Arrow ID : {self.id}] Invalid Source - {self.source}. Must be one of - {allowed_sources}")
        if self.target:
            if Element(self.target).type not in allowed_targets:
                raise ValueError(f"[Value Arrow ID : {self.id}] Invalid Target - {self.target}. Must be one of - {allowed_targets}")

class ControlFlow(Arrow):
    def __init__(self, element_id):
        Arrow.__init__(self, element_id)

        if self.color != color_code['arrow']['control_flow']:
            raise ValueError(f"[Control Arrow ID : {self.id}] Invalid Color! Must be {color_code['arrow']['control_flow']}")

        allowed_sources = ['variable', 'function', 'exec']
        allowed_targets = ['variable', 'function']
        
        if self.source:
            if Element(self.source).type not in allowed_sources:
                raise ValueError(f"[Control Arrow ID : {self.id}] Invalid Source - {self.source}. Must be one of - {allowed_sources}")
        if self.target:
            if Element(self.target).type not in allowed_targets:
                raise ValueError(f"[Control Arrow ID : {self.id}] Invalid Target - {self.target}. Must be one of - {allowed_targets}")
