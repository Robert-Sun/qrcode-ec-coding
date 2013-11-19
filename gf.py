# -*- coding: utf-8 -*-

# 重新理解了一下伽罗华域，简化了exp table和log table的生成
# GF(2**8)，本原多项式f(x) = x**8+x**4+x**3+x**2+1
# 因为加法为异或运算，于是可以得出x**8 = x**4 + x**3 + x**2 + 1
# 因此x**9 = x**8 * x = (x**4 + x**3 + x**2 + 1) * x
# 依次类推

# 伽罗华域GF(2**8, 100011101)
BASIC_EXPONENT = 8

EXP_TABLE = list(range(256))
LOG_TABLE = list(range(256))

for i in xrange(8):
    EXP_TABLE[i] = 1 << i

for i in xrange(8, 256):
    EXP_TABLE[i] = (EXP_TABLE[i - 4] ^ EXP_TABLE[i - 5] ^ EXP_TABLE[i - 6] ^
        EXP_TABLE[i - 8])

for i in xrange(255):
    LOG_TABLE[EXP_TABLE[i]] = i

for i in xrange(256):
    print i, EXP_TABLE[i]

print '################'

for i in xrange(256):
    print i, LOG_TABLE[i]
