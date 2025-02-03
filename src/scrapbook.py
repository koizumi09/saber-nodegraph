
from core import get_element_by_id
from classes.node import Node
from classes.element import Element
from classes.parameter import Parameter, ReturnValue


print_id = "IZS5oz5ja_VSkLGrc1yme"
print_param_id = "prR28PZyLDw_tgS1Fn99k"
random_rectangle_id = "68A0kcgQO5hc2d89fl64z"

sus_arrow = "kTvQ2MDEa9Ocj3bjMqsHa"
#box = get_element_by_id(sus_arrow)['endBinding']['elementId']

sus_box = "5aZxnpF8YR5IxGnlTr892"
substract_box = "3DLx6segeafBI3gD2KLdw"







# #target_id = "LbtkQrcoFvlIETPxs8mgG"
# first_container_id = "1DpNuQLp0Ar3k4DciV8xd"
# second_container_id = "Q8YVFO6JuNFO3MWWnp-WT"

# print_element = Node(print_id)
# param_element = Parameter(param_with_text_id)
# param_element_no_text = Element(random_rectangle_id)

# target = Element(target_id)
# first_container = Element(first_container_id)
# second_container = Element(second_container_id)

element = Node(print_id)

print(element.run_function())

    # for e in element.inner():
    #     print(e.data)
    # #print(element.inner())