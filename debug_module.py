# -*- coding: utf-8 -*-
import unittest
import sys
import StringIO
import itertools
import random

from woodapp import GameAction, GamePlayer, World, StrategyWood
        
sys.stdin = StringIO.StringIO("""7
2
...2...
..033..
.00344.
0000244
.00010.
..000..
...0...
4 1
5 4
3 2
1 2
21
MOVE&BUILD 0 NW S
MOVE&BUILD 0 NW SE
MOVE&BUILD 0 NW SW
MOVE&BUILD 0 W E
MOVE&BUILD 0 W N
MOVE&BUILD 0 W SW
MOVE&BUILD 0 W W
MOVE&BUILD 1 SW N
MOVE&BUILD 1 SW NE
MOVE&BUILD 1 SW NW
MOVE&BUILD 1 SW SW
MOVE&BUILD 1 SW W
MOVE&BUILD 1 W E
MOVE&BUILD 1 W N
MOVE&BUILD 1 W NW
MOVE&BUILD 1 W S
MOVE&BUILD 1 W SW
MOVE&BUILD 1 W W
PUSH&BUILD 0 SW S
PUSH&BUILD 0 SW SW
PUSH&BUILD 0 SW W
""")
w = World()

w.update()

#print w.maps()

s1 = StrategyWood(0, w)

#print s1.get_action()

print w.calc_potential((3,0), (3,1))
print w.calc_potential((3,0), (2,1))
