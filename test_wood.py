# -*- coding: utf-8 -*-
import unittest
import sys
import StringIO
import itertools
import random


import woodapp as app

class TestWorld(unittest.TestCase):

    def test_world_init(self):
        "Расчет направления"

        sys.stdin = StringIO.StringIO("""5
        2
        MOLECULES 0 0 1 0 0 0 3 0 0 0 0 0
        4 3 4 4 2
        6
        0 0 1 E 1 0 0 1 3 1
        2 0 1 D 1 0 2 1 0 0
        4 0 1 E 1 1 2 1 1 0
        1 1 1 E 1 2 0 2 0 0
        3 1 1 B 1 0 0 0 0 3
        5 1 1 B 1 1 0 0 0 2""")   


        player = (5,3)
        direction = (-1,-1)
        pos = app.future_position(player, direction)
        self.assertEqual(pos, (4,2))

    def test_from_dir(self):
        "Расчет направления"
        self.assertEqual(app.from_dir("NW"), (-1, -1))
        self.assertEqual(app.from_dir("N"), (0, -1))
        self.assertEqual(app.from_dir("SW"), (-1, 1))
        self.assertEqual(app.from_dir("S"), (0, 1))
        self.assertEqual(app.from_dir("E"), (1, 0))



if __name__ == '__main__':
    unittest.main()