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
34434
44442
11201
00000
00000
0 0
2 3
-1 -1
3 2
36
MOVE&BUILD 1 E E
MOVE&BUILD 1 E NE
MOVE&BUILD 1 E NW
MOVE&BUILD 1 E S
MOVE&BUILD 1 E SE
MOVE&BUILD 1 E SW
MOVE&BUILD 1 E W
MOVE&BUILD 1 NW E
MOVE&BUILD 1 NW S
MOVE&BUILD 1 NW SE
MOVE&BUILD 1 NW SW
MOVE&BUILD 1 NW W
MOVE&BUILD 1 S E
MOVE&BUILD 1 S N
MOVE&BUILD 1 S NE
MOVE&BUILD 1 S NW
MOVE&BUILD 1 S W
MOVE&BUILD 1 SE E
MOVE&BUILD 1 SE N
MOVE&BUILD 1 SE NE
MOVE&BUILD 1 SE NW
MOVE&BUILD 1 SE W
MOVE&BUILD 1 SW E
MOVE&BUILD 1 SW N
MOVE&BUILD 1 SW NE
MOVE&BUILD 1 SW NW
MOVE&BUILD 1 SW W
MOVE&BUILD 1 W E
MOVE&BUILD 1 W N
MOVE&BUILD 1 W NE
MOVE&BUILD 1 W NW
MOVE&BUILD 1 W S
MOVE&BUILD 1 W SE
MOVE&BUILD 1 W SW
MOVE&BUILD 1 W W
PUSH&BUILD 1 NE E


""")
w = World()
w.initialize()

w.update()

#print w.maps()

s1 = StrategyWood(0, w)


solution = s1.get_action()

t1 = (time.time() - t)*1000

if t1 < 50 and (w.units_per_player > 0 or solution is None):
    solution1 = solution

    s2 = StrategyWood(1, w)

    solution2 = s2.get_action()
    
    if solution1 is None:
        solution = solution2
    elif solution1['value'] < solution2['value']:
        solution = solution2


print solution['action']


#--------
print "%5.2lf" % ((time.time() -t)*1000) < 50