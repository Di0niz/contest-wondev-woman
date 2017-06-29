# -*- coding: utf-8 -*-
import unittest
import sys
import StringIO
import itertools
import random

import time

from silverapp import GameAction, GamePlayer, World, StrategyWood

t = time.time()

        
sys.stdin = StringIO.StringIO("""5
2
00000
03300
02330
00210
00000
2 3
0 1
2 2
-1 -1
3
PUSH&BUILD 0 N N
PUSH&BUILD 0 N NE
PUSH&BUILD 0 N NW

""")
w = World()
w.initialize()

w.update()

s1 = StrategyWood(0, w)


solution = s1.get_action()

t1 = (time.time() - t)*1000

print '---'
if solution is None:
    s2 = StrategyWood(1, w)
    solution = s2.get_action()
    print w.maps(w.players[1].position())
else:
    print w.maps(w.players[0].position())



print solution['action'], solution


#--------
print "%5.2lf" % ((time.time() -t)*1000) 