# -*- coding: utf-8 -*-
import sys
import math
from operator import attrgetter

DEBUG_MODE = False

def get_raw():
    "Обертка для системной функции, для отображения вводимых параметров"
    raw = raw_input()
    if DEBUG_MODE:
        print >> sys.stderr, raw
    return raw


class GamePlayer(object):
    "Описание возможных действий игрока"

    def __init__(self, index, param):
        "Инициируем информацию об игроке"
        self.index = index
        self.x, self.y = [int(j) for j in param.split()]
        self.legals = []

    def append_action(self, action):
        "Добавляем в коллекцию список доступных действий"
        self.legals.append(action)
        return True

    def position(self):
        "Определяем текущую позицию игрока"
        return self.x, self.y

    def future(self, pos):
        "Вычисляем будующую позицию"
        x, y = self.x, self.y
        dx, dy = pos
        return x + dx, y + dy


    def future_move(self, action):
        "Вычисляем будующую позицию"
        x, y = self.x, self.y
        if action.atype == "MOVE&BUILD":
            x, y  = x + action.dir_1[0], y + action.dir_1[1]

        return x, y

    def future_build(self, action):
        "Вычисляем координату строительства"
        x, y = self.x, self.y
        if action.atype == "MOVE&BUILD":
            x, y  = x + action.dir_1[0], y+action.dir_1[1]

        x, y  = x + action.dir_2[0], y + action.dir_2[1]

        return x, y

    def future_push(self, from_player):
        "Определяем следуюущую позицию после толчка"
        dx, dy = self.x - from_player.x, self.y - from_player.y

        return self.x + dx, self.y + dy

    def __repr__(self):
        return "%d: %d %d" % (self.index, self.x, self.y)

class GameAction(object):
    "описание игровых действий"
    def __init__(self, param):
        "инициализация действия из командной строки"
        self.command = param
        self.atype, index, dir_1, dir_2 = param.split()

        self.index = int(index)

        self.dir_1 = self.from_dir(dir_1)
        self.dir_2 = self.from_dir(dir_2)

    def from_dir(self, direction):
        "Преобразуем координаты"
        n, s, w, e = -1, 1, -1, 1
        x, y = 0, 0
        if "N" in direction:
            y = n
        if "S" in direction:
            y = s
        if "W" in direction:
            x = w
        if "E" in direction:
            x = e

        return x, y

    def to_dir(self, coords):
        "Преобразование обратно"
        n, s, w, e = -1, 1, -1, 1
        
        ret = ""
        x, y = coords
        if y == n:
            ret = "N"
        elif y == s:
            ret = "S"
        if x == w:
            ret = ret + "W"
        elif x == e:
            ret = ret + "E"
        return ret

    def __repr__(self):
        return "%s %d %s %s" % (self.atype, self.index, self.to_dir(self.dir_1), self.to_dir(self.dir_2))

class World(object):
    "Описание игровой площадки"
    def __init__(self):
        "Начальные параметры игрового мира"

        # управление параметрами вывода
        self.show_input = True

        self.size = int(get_raw())
        self.units_per_player = int(get_raw())

        # описание игровой площадки
        self.grid = []
        self.players = []
        self.enemies = []


    def moves(self, player):
        "Определяем список доступных ходов"
        cells = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        cur_height = self.height(player.position())

        excluded = []
        for border in self.players + self.enemies:
            excluded.append(border.position())

        av_moves = []
        for next_cell in cells:
            next_pos = player.future(next_cell)
            #print next_pos
            next_height = self.height(next_pos)

            if  next_height - cur_height < 1 and next_height < 4 and next_pos not in excluded:
                av_moves.append(next_cell)

        return av_moves


    def builds(self, pos):
        "Определяем список доступных ходов"
        cells = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        excluded = []
        for border in self.players + self.enemies:
            excluded.append(border.position())

        x, y = pos

        av_builds = []
        for dx, dy in cells:
            next_pos = x + dx, y + dy
            #print next_pos
            next_height = self.height(next_pos)

            if next_height < 4 and next_pos not in excluded:
                av_builds.append((dx, dy))

        return av_builds

    def pushes(self, player):
        "Определяем список доступных ходов"
        cells = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        x, y = player.position()
        av_pushes = []
        for enemy in self.enemies:
            ex, ey = enemy.position()
            dx, dy = x - ex, y - ey
            if abs(dx) <= 1 and abs(dy) <= 1:
                av_pushes.append(enemy)

        return av_pushes

    def update(self):
        "Считавыем параметры из консоли"

        self.grid = []
        self.players = []
        self.enemies = []


        for _ in xrange(self.size):
            self.grid.append(get_raw())

        for i in xrange(self.units_per_player):
            player = GamePlayer(i, get_raw())
            self.players.append(player)

        for i in xrange(self.units_per_player):
            enemy = GamePlayer(i, get_raw())
            self.enemies.append(enemy)

        legal_actions = int(get_raw())

        for i in xrange(legal_actions):
            raw = get_raw()
            atype, index, dir_1, dir_2 = raw.split()

            index = int(index)
            # распределяем список возможных действий
            self.players[index].append_action(GameAction(raw))

    def maps(self):
        "отображаем карту в виде строки"
        ret = None
        for row in self.grid:
            if ret is not None:
                ret = ret + "\n"
            else:
                ret = ""

            ret = ret + row.lstrip()
        return ret

    def available_move(self, next_pos):
        "Проверяем, что клетка не занята противниками"
        for player in self.players + self.enemies:
            if player.position() == next_pos:
                return False
        return True


    def height(self, forcell):
        x, y = forcell
        value = self.grid[y][x]
        if value == '.' or x < 0 or y < 0 or x >= self.size or y >= self.size:
            # переворачиваем координатную сетку
            return 4
        else:
            return int(value)

        
class StrategyWood(object):
    """Стратегия для участия в деревянной лиге:
    - ходит по доступным квадратам
    """
    def __init__(self, index, world):
        "Инициализируем стратегию"
        self.player = world.players[index]
        self.world = world
        self.solution = []


    def find_near_max(self):
        "Ищем ближайшую точку"
        if len(self.player.legals) == 0:
            return None

        near = self.player.legals[0]
        pos = self.player.future_move(near)

        h_near = self.world.height(pos)

        # данные для оптимизации
        opt_data = []

        for action in self.player.legals:
            pos = self.player.future_move(action)

            # определеяем доступность перемещения
            if not self.world.available_move(pos):
                continue


            mh = self.world.height(self.player.future_move(action))
            bh = self.world.height(self.player.future_build(action))

            opt_data.append(
                {
                    'action': action,
                    'value': mh*3 - bh,
                    'bh':bh,
                    'mh':mh,
                    'available':int(bh < 3)
                }
            )

        solution = sorted(opt_data, key=lambda el: el['value'], reverse=True)
        #print solution

        if len(solution) > 0:
            return solution[0]['action']
        else:
            return None

    def get_action(self):
        return self.find_near_max()


if __name__ == '__main__':
    
    DEBUG_MODE = True

    # size = int(raw_input())
    # units_per_player = int(raw_input())
    w = World()

    # game loop
    while True:

        w.update()

        s1 = StrategyWood(0, w)

        action = s1.get_action()

        if action == None and w.units_per_player > 0:
            s2 = StrategyWood(1, w)
            action = s2.get_action()

        print action
