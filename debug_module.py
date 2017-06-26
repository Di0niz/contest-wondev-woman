# -*- coding: utf-8 -*-
import unittest
import sys
import StringIO
import itertools
import random

from woodapp import GameAction, GamePlayer, World, StrategyWood
        
sys.stdin = StringIO.StringIO("""7
2
...4...
..444..
.24444.
0004444
.00442.
..040..
...4...
4 5
1 3
5 4
2 3
8
MOVE&BUILD 1 S N
MOVE&BUILD 1 S S
MOVE&BUILD 1 S SE
MOVE&BUILD 1 S W
MOVE&BUILD 1 SW E
MOVE&BUILD 1 SW NE
MOVE&BUILD 1 SW SE
PUSH&BUILD 1 SE S""")
w = World()

w.update()

#print w.maps()

s1 = StrategyWood(1, w)

print w.moves(w.players[1])
print w.pushes(w.players[1])
print w.builds(w.players[1].position())

print s1.get_action()
