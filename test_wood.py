# -*- coding: utf-8 -*-
import unittest
import sys
import StringIO
import itertools
import random

from woodapp import GameAction, GamePlayer, World, StrategyWood

import woodapp as app

class TestWorld(unittest.TestCase):

    def test_init_player(self):
        "Тестирование объекта Player"

        player = GamePlayer(0, "3 3")
        action = GameAction("MOVE&BUILD 0 E E")

        self.assertEqual(player.future_move(action), (4, 3))
        self.assertEqual(player.future_build(action), (5, 3))

    def test_init_game_action(self):
        "Тестирование преобразования в объект и обратно"
        self.assertEqual(str(GameAction("MOVE&BUILD 0 N E")), "MOVE&BUILD 0 N E")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 N N")), "MOVE&BUILD 0 N N")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 N NW")), "MOVE&BUILD 0 N NW")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 N S")), "MOVE&BUILD 0 N S")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 N SW")), "MOVE&BUILD 0 N SW")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 N W")), "MOVE&BUILD 0 N W")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 NE NW")), "MOVE&BUILD 0 NE NW")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 NE SE")), "MOVE&BUILD 0 NE SE")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 NE SW")), "MOVE&BUILD 0 NE SW")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 NE W")), "MOVE&BUILD 0 NE W")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 NW E")), "MOVE&BUILD 0 NW E")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 NW N")), "MOVE&BUILD 0 NW N")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 NW NE")), "MOVE&BUILD 0 NW NE")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 NW NW")), "MOVE&BUILD 0 NW NW")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 NW S")), "MOVE&BUILD 0 NW S")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 NW SE")), "MOVE&BUILD 0 NW SE")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 S E")), "MOVE&BUILD 0 S E")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 S N")), "MOVE&BUILD 0 S N")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 S NW")), "MOVE&BUILD 0 S NW")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 S S")), "MOVE&BUILD 0 S S")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 S SW")), "MOVE&BUILD 0 S SW")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 S W")), "MOVE&BUILD 0 S W")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 SE NE")), "MOVE&BUILD 0 SE NE")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 SE NW")), "MOVE&BUILD 0 SE NW")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 SE SW")), "MOVE&BUILD 0 SE SW")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 SE W")), "MOVE&BUILD 0 SE W")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 SW E")), "MOVE&BUILD 0 SW E")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 SW N")), "MOVE&BUILD 0 SW N")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 SW NE")), "MOVE&BUILD 0 SW NE")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 SW S")), "MOVE&BUILD 0 SW S")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 SW SE")), "MOVE&BUILD 0 SW SE")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 SW SW")), "MOVE&BUILD 0 SW SW")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 SW W")), "MOVE&BUILD 0 SW W")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 W E")), "MOVE&BUILD 0 W E")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 W N")), "MOVE&BUILD 0 W N")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 W NE")), "MOVE&BUILD 0 W NE")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 W S")), "MOVE&BUILD 0 W S")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 W SE")), "MOVE&BUILD 0 W SE")
        self.assertEqual(str(GameAction("MOVE&BUILD 0 W SW")), "MOVE&BUILD 0 W SW")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 E N")), "MOVE&BUILD 1 E N")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 E NE")), "MOVE&BUILD 1 E NE")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 E S")), "MOVE&BUILD 1 E S")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 E SE")), "MOVE&BUILD 1 E SE")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 E SW")), "MOVE&BUILD 1 E SW")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 E W")), "MOVE&BUILD 1 E W")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 NE E")), "MOVE&BUILD 1 NE E")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 NE N")), "MOVE&BUILD 1 NE N")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 NE NE")), "MOVE&BUILD 1 NE NE")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 NE NW")), "MOVE&BUILD 1 NE NW")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 NE S")), "MOVE&BUILD 1 NE S")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 NE SW")), "MOVE&BUILD 1 NE SW")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 NW NE")), "MOVE&BUILD 1 NW NE")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 NW S")), "MOVE&BUILD 1 NW S")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 NW SE")), "MOVE&BUILD 1 NW SE")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 NW SW")), "MOVE&BUILD 1 NW SW")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 S E")), "MOVE&BUILD 1 S E")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 S N")), "MOVE&BUILD 1 S N")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 S NE")), "MOVE&BUILD 1 S NE")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 S NW")), "MOVE&BUILD 1 S NW")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 S S")), "MOVE&BUILD 1 S S")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 S SE")), "MOVE&BUILD 1 S SE")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 S W")), "MOVE&BUILD 1 S W")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 SE E")), "MOVE&BUILD 1 SE E")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 SE N")), "MOVE&BUILD 1 SE N")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 SE NW")), "MOVE&BUILD 1 SE NW")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 SE S")), "MOVE&BUILD 1 SE S")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 SE SE")), "MOVE&BUILD 1 SE SE")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 SE SW")), "MOVE&BUILD 1 SE SW")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 SE W")), "MOVE&BUILD 1 SE W")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 SW E")), "MOVE&BUILD 1 SW E")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 SW N")), "MOVE&BUILD 1 SW N")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 SW NE")), "MOVE&BUILD 1 SW NE")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 SW NW")), "MOVE&BUILD 1 SW NW")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 SW SE")), "MOVE&BUILD 1 SW SE")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 W E")), "MOVE&BUILD 1 W E")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 W N")), "MOVE&BUILD 1 W N")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 W S")), "MOVE&BUILD 1 W S")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 W SE")), "MOVE&BUILD 1 W SE")
        self.assertEqual(str(GameAction("MOVE&BUILD 1 W W")), "MOVE&BUILD 1 W W")
        self.assertEqual(str(GameAction("PUSH&BUILD 0 E E")), "PUSH&BUILD 0 E E")
        self.assertEqual(str(GameAction("PUSH&BUILD 1 N N")), "PUSH&BUILD 1 N N")
        self.assertEqual(str(GameAction("PUSH&BUILD 1 N NE")), "PUSH&BUILD 1 N NE")

    def test_world_init(self):
        "Расчет направления"

        sys.stdin = StringIO.StringIO("""7
2
...0...
..000..
.00000.
0000000
.00000.
..000..
...0...
3 3
1 3
4 4
2 1
78
MOVE&BUILD 0 E E
MOVE&BUILD 0 E N
MOVE&BUILD 0 E NE
MOVE&BUILD 0 E NW
MOVE&BUILD 0 E SE
MOVE&BUILD 0 E SW
MOVE&BUILD 0 E W
MOVE&BUILD 0 N E
MOVE&BUILD 0 N N
MOVE&BUILD 0 N NE
MOVE&BUILD 0 N S
MOVE&BUILD 0 N SE
MOVE&BUILD 0 N SW
MOVE&BUILD 0 N W
MOVE&BUILD 0 NE E
MOVE&BUILD 0 NE N
MOVE&BUILD 0 NE NW
MOVE&BUILD 0 NE S
MOVE&BUILD 0 NE SE
MOVE&BUILD 0 NE SW
MOVE&BUILD 0 NE W
MOVE&BUILD 0 NW E
MOVE&BUILD 0 NW NE
MOVE&BUILD 0 NW S
MOVE&BUILD 0 NW SE
MOVE&BUILD 0 NW W
MOVE&BUILD 0 S N
MOVE&BUILD 0 S NE
MOVE&BUILD 0 S NW
MOVE&BUILD 0 S S
MOVE&BUILD 0 S SE
MOVE&BUILD 0 S SW
MOVE&BUILD 0 S W
MOVE&BUILD 0 SW E
MOVE&BUILD 0 SW N
MOVE&BUILD 0 SW NE
MOVE&BUILD 0 SW S
MOVE&BUILD 0 SW SE
MOVE&BUILD 0 SW W
MOVE&BUILD 0 W E
MOVE&BUILD 0 W N
MOVE&BUILD 0 W NE
MOVE&BUILD 0 W NW
MOVE&BUILD 0 W S
MOVE&BUILD 0 W SE
MOVE&BUILD 0 W SW
MOVE&BUILD 1 E N
MOVE&BUILD 1 E NE
MOVE&BUILD 1 E NW
MOVE&BUILD 1 E S
MOVE&BUILD 1 E SE
MOVE&BUILD 1 E SW
MOVE&BUILD 1 E W
MOVE&BUILD 1 N E
MOVE&BUILD 1 N S
MOVE&BUILD 1 N SE
MOVE&BUILD 1 N SW
MOVE&BUILD 1 NE E
MOVE&BUILD 1 NE NE
MOVE&BUILD 1 NE S
MOVE&BUILD 1 NE SW
MOVE&BUILD 1 NE W
MOVE&BUILD 1 S E
MOVE&BUILD 1 S N
MOVE&BUILD 1 S NE
MOVE&BUILD 1 S NW
MOVE&BUILD 1 S SE
MOVE&BUILD 1 SE E
MOVE&BUILD 1 SE N
MOVE&BUILD 1 SE NW
MOVE&BUILD 1 SE S
MOVE&BUILD 1 SE SE
MOVE&BUILD 1 SE W
MOVE&BUILD 1 W E
MOVE&BUILD 1 W NE
MOVE&BUILD 1 W SE
PUSH&BUILD 0 SE E
PUSH&BUILD 0 SE S""")
        w = World()

        w.update()

        print w.maps()


    def test_from_dir(self):
        "Расчет направления"
        # self.assertEqual(app.from_dir("NW"), (-1, -1))
        # self.assertEqual(app.from_dir("N"), (0, -1))
        # self.assertEqual(app.from_dir("SW"), (-1, 1))
        # self.assertEqual(app.from_dir("S"), (0, 1))
        # self.assertEqual(app.from_dir("E"), (1, 0))
        pass


if __name__ == '__main__':
    unittest.main()