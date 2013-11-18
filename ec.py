# -*- coding: utf-8 -*-

DEBUG = True

# 伽罗华域GF(256, 285)
BASIC_EXPONENT = 8
BASIC_MODULO = 0b100011101

# 存储 指数-值 键值对
exponent_values_table = dict()
# 存储 值-指数 键值对
value_exponents_table = dict()

def set_exponent_for_value(key, val):
    try:
        value_exponents_table[key]
    except KeyError:
        value_exponents_table[key] = val

for i in range(0, BASIC_EXPONENT):
    val = 2 ** i
    exponent_values_table[i] = val
    set_exponent_for_value(val, i)

# 对于2的n次方，如果小于256，则直接使用幂指数运算，如果大于256，则将其分解为2的n-1次方与2的乘积，而2的n-1次方已经计算过，所以使用已经算出的值乘以2，如果西小于256，则保留结果，如果大于256，则与285做异或运算
max_limit = 2 ** BASIC_EXPONENT;
for i in range(BASIC_EXPONENT, max_limit):
    prev = exponent_values_table[i - 1]
    current = prev * 2
    if current >= max_limit:
        current ^= BASIC_MODULO
    exponent_values_table[i] = current
    set_exponent_for_value(current, i)

if DEBUG:
    for key, value in exponent_values_table.items():
        print "%d = %d" % (key, value)

    for key, value in value_exponents_table.items():
        print "%d = %d" % (key, value)

def multiply_polymal(first, second):
    """两个多项式乘积，构造generator_polymal的规则，详细原理见http://www.thonky.com/qr-code-tutorial/error-correction-coding/
    """
    m = len(first) - 1
    n = len(second) - 1
    max_exp = m + n
    result = list()
    for i in xrange(0, max_exp + 1):
        coefficient = 0
        for j in xrange(0, i + 1):
            if j > m or i - j > n:
                continue
            val1 = first[m - j]
            val2 = second[n - (i - j)]
            total = val1 + val2
            if total >= max_limit:
                total %= (max_limit - 1)
            total = exponent_values_table[total]
            coefficient ^= total
        result.insert(0, value_exponents_table[coefficient])
    return result

# 计算纠错码需要message_polymal和generator_polymal一起运算，本方法生成steps个纠错码应该使用的generator_polymal
def generator_polymal(steps):
    polymal = [0, 0]
    for i in xrange(1, steps):
        polymal = multiply_polymal(polymal, [0, i])
    return polymal

if DEBUG:
    polymal = generator_polymal(7)
    print polymal
    assert tuple(polymal) == (0, 87, 229, 146, 149, 238, 102, 21)

def generate_error_correction_codes(datawords, error_code_counts):
    """生成数据串datawords的个数为error_code_counts的纠错码串，详细原理见http://www.thonky.com/qr-code-tutorial/error-correction-coding/
    """
    gen_polymal = generator_polymal(error_code_counts)
    message_polymal = list()
    data_len = len(datawords)

    for i in xrange(0, data_len):
        message_polymal.append(datawords[i])

    result = list()
    for i in xrange(0, data_len):
        mul_base = message_polymal[0]

        for j in xrange(0, len(gen_polymal)):
            mul_data = gen_polymal[j] + value_exponents_table[mul_base]
            if mul_data >= max_limit:
                mul_data %= (max_limit - 1)

            if j >= len(message_polymal):
                message_polymal.append(exponent_values_table[mul_data])
            else:
                message_polymal[j] = exponent_values_table[mul_data] ^ message_polymal[j]

        message_polymal.pop(0)

    return message_polymal


if DEBUG:
    result = generate_error_correction_codes((32, 91, 11, 120, 209, 114, 220, 77, 67, 64, 236, 17, 236, 17, 236, 17), 10)
    print result
    assert tuple(result) == (196, 35, 39, 119, 235, 215, 231, 226, 93, 23)
