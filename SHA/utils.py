
def to_hex(bin):
    hex = ""
    for i in range(0, int(len(bin)/4)):
        block = bin[i * 4: (i + 1) * 4]
        num = block[0] * 8 + block[1] * 4 + block[2] * 2 + block[3] * 1
        hex += str(format(num, 'x'))
    return hex