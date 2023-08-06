from oye_vix.vicky import calci
from oye_vix.my_cmd import command as c

from oye_vix.vicky import hello as h
import math, oye_vix.vicky

calci.add(4,5)

q, r = calci.div(8)
print('Quotient = {}'.format(q))
print('Remainder = {}'.format(r))

v = vicky.pie()
m = math.pi

if m == v:
    print()
    print(m, v)
else: print('unequal')

print('Hi, ' + h.hi())
h.bye('Ankit')

c.cmd()
