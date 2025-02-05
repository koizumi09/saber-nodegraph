from core import drawing, all_shapes

from classes.element import Element
from classes import nodes
from classes import arrows
from classes import pins


def main():

    start, node_graph = initialize_node_graph()
    current_node = node_graph[start].next()

    while current_node != None:
        return_value = node_graph[current_node].execute()
        next = node_graph[current_node].next()

        current_node = next

def initialize_node_graph():
    node_graph = {}

    for e in drawing['elements']:
        if e['type'] in all_shapes:
            e = Element(e['id'])
            
            if e.type == 'variable':
                e = nodes.Variable(e.id)
            if e.type == 'function':
                e = nodes.Function(e.id)
            if e.type == 'expression':
                e = nodes.Expression(e.id)

            if e.type == 'parameter':
                e = pins.Parameter(e.id)
            if e.type == 'return':
                e = pins.Return(e.id)
            if e.type == 'exec':
                e = pins.Exec(e.id)

            if e.type == 'control_flow':
                e = arrows.ControlFlow(e.id)
            if e.type == 'value_flow':
                e = arrows.ValueFlow(e.id)

            node_graph[e.id] = e

            if e.text == 'Start':
                start = e.id

    return (start, node_graph)

if __name__ == '__main__':
    main()