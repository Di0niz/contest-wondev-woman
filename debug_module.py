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
00033
00033
00044
00002
00033
4 3
0 0
-1 -1
-1 -1
3
MOVE&BUILD 0 S N
MOVE&BUILD 0 S W
MOVE&BUILD 0 SW N



""")
w = World()
w.initialize()

w.update()

#print w.maps()
print '---'

s1 = StrategyWood(0, w)


solution = s1.get_action()

t1 = (time.time() - t)*1000

print '---'
# 
# if t1 < 50 and (w.units_per_player > 0 or solution is None):
#     solution1 = solution
# 
#     s2 = StrategyWood(1, w)
# 
#     solution2 = s2.get_action()
#     
#     if solution1 is None:
#         solution = solution2
#     elif solution1['value'] < solution2['value']:
#         solution = solution2
# 

print solution['action']


#--------
print "%5.2lf" % ((time.time() -t)*1000) 