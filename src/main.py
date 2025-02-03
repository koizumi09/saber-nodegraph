from core import get_start

from classes.node import Node

def main():
    
    start = Node(get_start())
    
    current = start

    while current != None:
        
        current_return = current.run_function()

        current = current.next_node


if __name__ == '__main__':
    main()