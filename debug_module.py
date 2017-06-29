# -*- coding: utf-8 -*-
import unittest
import sys
import StringIO
import itertools
import random

import time

from silverapp import GameAction, GamePlayer, World, StrategyWood

t = time.time()

        
sys.stdin = StringIO.StringIO("""6
2
000000
000003
000033
000000
.3300.
030000
1 4
0 5
-1 -1
-1 -1
35
MOVE&BUILD 0 E E
MOVE&BUILD 0 E N
MOVE&BUILD 0 E NE
MOVE&BUILD 0 E NW
MOVE&BUILD 0 E S
MOVE&BUILD 0 E SE
MOVE&BUILD 0 E SW
MOVE&BUILD 0 E W
MOVE&BUILD 0 N E
MOVE&BUILD 0 N N
MOVE&BUILD 0 N NE
MOVE&BUILD 0 N NW
MOVE&BUILD 0 N S
MOVE&BUILD 0 N SE
MOVE&BUILD 0 N W
MOVE&BUILD 0 NE E
MOVE&BUILD 0 NE N
MOVE&BUILD 0 NE NE
MOVE&BUILD 0 NE NW
MOVE&BUILD 0 NE S
MOVE&BUILD 0 NE SE
MOVE&BUILD 0 NE SW
MOVE&BUILD 0 NE W
MOVE&BUILD 0 NW E
MOVE&BUILD 0 NW N
MOVE&BUILD 0 NW NE
MOVE&BUILD 0 NW SE
MOVE&BUILD 0 S E
MOVE&BUILD 0 S N
MOVE&BUILD 0 S NE
MOVE&BUILD 0 SE E
MOVE&BUILD 0 SE N
MOVE&BUILD 0 SE NE
MOVE&BUILD 0 SE NW
MOVE&BUILD 0 SE W
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