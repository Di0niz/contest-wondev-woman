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
30304
33223
30023
00000
00000
4 1
3 0
-1 -1
-1 -1
19
MOVE&BUILD 0 S N
MOVE&BUILD 0 S NW
MOVE&BUILD 0 S S
MOVE&BUILD 0 S SW
MOVE&BUILD 0 S W
MOVE&BUILD 0 SW E
MOVE&BUILD 0 SW N
MOVE&BUILD 0 SW NE
MOVE&BUILD 0 SW NW
MOVE&BUILD 0 SW S
MOVE&BUILD 0 SW SE
MOVE&BUILD 0 SW SW
MOVE&BUILD 0 SW W
MOVE&BUILD 0 W E
MOVE&BUILD 0 W NW
MOVE&BUILD 0 W S
MOVE&BUILD 0 W SE
MOVE&BUILD 0 W SW
MOVE&BUILD 0 W W

""")
w = World()
w.initialize()

w.update()

#print w.maps()

s1 = StrategyWood(0, w)

print s1.get_action()

#print s1.world.calc_potential((3,0), (4,0))


print w.maps()

#--------
print "%5.2lf" % ((time.time() -t)*20)