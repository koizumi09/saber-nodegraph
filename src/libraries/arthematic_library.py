

def add(*args):
    if len(args) < 2:
        raise ValueError
    sum = 0
    first = True
    for arg in args:
        if first:
            sum = arg
            first = False
            continue
        sum += arg

    return sum

def substract(*args):
    if len(args) < 2:
        raise ValueError
    diff = 0
    first = True
    for arg in args:
        if first:
            diff = arg
            first = False
            continue
        diff -= arg

    return diff

def multiply(*args):
    if len(args) < 2:
        raise ValueError
    prod = 1
    first = True
    for arg in args:
        if first:
            prod = arg
            first = False
            continue
        prod *= arg

    return prod

def divide(*args):
    if len(args) < 2:
        raise ValueError
    div = 1
    first = True
    for arg in args:
        if first:
            div = arg
            first = False
            continue
        div /= arg

    return div