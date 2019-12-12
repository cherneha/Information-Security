from bitarray import bitarray

def next_elem(num, current_index):
    i = current_index + 1
    if i >= len(num):
        return -1
    while num[i] == False:
        i += 1
        if i >= len(num):
            return -1
    return i


def next_elem_power(num, current_power):
    max_pow = len(num) - 1
    current_index = max_pow - current_power
    next_el = next_elem(num, current_index)
    if next_el == -1:
        return -1
    return max_pow - next_el


def leftshift(ba, count):
    return ba[count:] + (bitarray('0') * count)

def multiply_binary(a, b):
    product = bitarray('0' * (len(a) + len(b)))
    b = bitarray('0' * (len(product) - len(b))) + b
    for i in range(len(a) - 1, -1, -1):
        # print("b = ", b)
        if a[i] == True:
            product = product ^ b
        b = leftshift(b, 1)
    i = 0
    while i < len(product) and product[i] == False:
        i += 1
    return product[i:]

def bitarray_to_str(a):
    a = a.tolist()
    str = ""
    foundTrue = False
    for el in a:
        if el == True:
            str += '1'
            foundTrue = True
        else:
            if foundTrue:
                str += '0'
    return str