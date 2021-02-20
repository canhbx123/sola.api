import random
import string

uncode = 'áàãảạăắằẳặẵâấầẩậẫđéèẻẽẹêếềễểệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ'
CONS = string.ascii_letters + string.digits + string.punctuation + ' ' + uncode + uncode.upper()


def create_random():
    return ''.join(random.choices(CONS, k=random.randint(1, 1000)))


def right_shift(data, bits):
    return (data & 0xffffffff) >> bits


def left_shirt(a, b):
    x = 0xFFFFFFFF & (a << b)
    if x > 0x7FFFFFFF:
        return - (~(x - 1) & 0xFFFFFFFF)
    return x


def zh(a, b):
    for c in range(0, len(b) - 2, 3):
        d = b[c + 2]
        d = ord(d[0]) - 87 if "a" <= d else int(d)
        d = right_shift(a, d) if "+" == b[c + 1] else left_shirt(a, d)
        a = (a + d) & 4294967295 if "+" == b[c] else a ^ d
    return a


def decode_ord(a):
    result = []
    for s in a:
        g = ord(s)
        if g < 128:
            result.append(g)
            continue
        if g < 2048:
            result.append(right_shift(g, 6) | 192)
        else:
            result.extend((right_shift(g, 12) | 224, right_shift(g, 6) & 63 | 128))
        result.append(g & 63 | 128)
    return result


def gen_key(a):
    d = decode_ord(a)
    a = 0
    for e in range(len(d)):
        a += d[e]
        a = zh(a, '+-a^+6')
    a = zh(a, "+-3^+b+-f")
    a %= 1000000
    return a
