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

def add_pos(point, point_at):
    "складываем две координаты"
    pointx, pointy = point
    point_atx, point_aty = point_at
    return (pointx + point_atx, pointy + point_aty)

def sub_pos(point, point_at):
    "Вычитаем две координаты"
    pointx, pointy = point
    point_atx, point_aty = point_at
    return (pointx - point_atx, pointy - point_aty)


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
        cur = self.x, self.y
        if action.atype == "MOVE&BUILD":
            cur = add_pos(cur, action.dir_1)
        return cur

    def future_build(self, action):
        "Вычисляем координату строительства"
        cur = self.x, self.y

        cur = add_pos(cur, action.dir_1)

        return add_pos(cur, action.dir_2)

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

        self.__cells__ = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]

    def moves(self, player):
        "Определяем список доступных ходов"
        cur_height = self.height(player.position())

        excluded = []
        for border in self.players + self.enemies:
            excluded.append(border.position())

        av_moves = []
        for next_cell in self.__cells__:
            next_pos = player.future(next_cell)
            #print next_pos
            next_height = self.height(next_pos)

            if  next_height - cur_height < 1 and next_height < 4 and next_pos not in excluded:
                av_moves.append(next_cell)

        return av_moves

    def calc_potential(self, pos, build_at=(-1, 1)):
        "расчитываем сумму возможных вершин, в которые можно попасть из центра"
        sum_height = 0
        #считаем, что если уровень ниже допустимого, тогда мощность падает
        cur_height = self.height(pos)

        for cell in self.__cells__:
            next_pos = add_pos(pos, cell)

            if self.position_available(next_pos):
                height = self.height(next_pos)
                # если планируем строить в этой точке
                # увеличиваем
                if next_pos == build_at:
                    height += 1

                sum_height += (height if height < 4 else 0)

        return sum_height


    def builds(self, pos):
        "Определяем список доступных ходов"
        excluded = []

        for border in self.players + self.enemies:
            excluded.append(border.position())

        av_builds = []
        for cell in self.__cells__:
            next_pos = add_pos(pos, cell)
            #print next_pos
            next_height = self.height(next_pos)

            if next_height < 4 and next_pos not in excluded:
                av_builds.append(cell)

        return av_builds

    def pushes(self, player):
        "Определяем список доступных ходов"
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

    def position_available(self, pos):
        posx, posy = pos
        return not (posx < 0 or posy < 0 or posx >= self.size or posy >= self.size)

    def height(self, forcell):
        x, y = forcell
        value = self.grid[y][x]
        if value == '.' and self.position_available(forcell):
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

        h_cur = self.world.height(self.player.position())
        near = self.player.legals[0]
        pos = self.player.future_move(near)

        h_near = self.world.height(pos)

        # данные для оптимизации
        opt_data = []

        for action in self.player.legals:
            stay_at = self.player.future_move(action)

            # определеяем доступность перемещения
            if not self.world.position_available(stay_at):
                continue

            build_at = self.player.future_build(action)

            mh = self.world.height(stay_at)
            bh = self.world.height(build_at)
            available = int(bh < 4)
            potential = self.world.calc_potential(stay_at, build_at)
            bonus = mh - h_cur

            if action.atype == "PUSH&BUILD" and bh == 0:
                
                opt_data.append(
                    {
                        'action': action,
                        'value': 100, #mh*3 - bh,
                        'potential': potential,
                        'stay_at': stay_at,
                        'build_at': build_at,
                        'bh':bh,
                        'mh':mh,
                        'available':available
                    }
                )

            else:
                opt_data.append(
                    {
                        'action': action,
                        'value': potential + available + bonus, #mh*3 - bh,
                        'potential': potential,
                        'stay_at': stay_at,
                        'build_at': build_at,
                        'bh':bh,
                        'mh':mh,
                        'available':available
                    }
                )

        solution = sorted(opt_data, key=lambda el: el['value'], reverse=True)

        #print "\n".join(str(x) for x in solution)

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
