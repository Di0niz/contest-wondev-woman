# -*- coding: utf-8 -*-
import sys
import math
import time

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

def dist_pos(point, point_at):
    "определяем расстояние между точками"
    pointx, pointy = point
    point_atx, point_aty = point_at
    return max(abs(pointx - point_atx), abs(pointy - point_aty))


class GamePlayer(object):
    "Описание возможных действий игрока"

    def __init__(self, index, param):
        "Инициируем информацию об игроке"
        self.index = index
        self.x, self.y = [int(j) for j in param.split()]
        self.legals = []
        self.did_action = None
        self.pushed = False

    def copy(self):
        return GamePlayer(self.index, "%d %d" % (self.x, self.y))

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

        self.size = 0 #int(get_raw())
        self.units_per_player = 0 #int(get_raw())

        # описание игровой площадки
        self.grid = {}
        self.players = [] # (x, y)
        self.enemies = [] # (x, y)

        # ноль исключаем из обхода, так как высоту клетки мереем отдельно
        self.__cells__ = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]

    def initialize(self):
        "читаем данные из потока"
        self.size = int(get_raw())
        self.units_per_player = int(get_raw())

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

    def calc_potential(self, position, check_block = True):
        "расчитываем сумму возможных вершин, в которые можно попасть из центра"
        sum_height = 0
        #считаем, что если уровень ниже допустимого, тогда мощность падает
        #pos = player.position()

        if position == (-1, -1):
            return sum_height

        # определяем дельту между центром и крайними точками
        min_dh = 4
        min_height = 4
        cur_height = self.height(position)

        for cell in self.__cells__:
            next_pos = add_pos(position, cell)

            #if self.position_available(next_pos):
            height = self.height(next_pos)
            # если планируем строить в этой точке
            # увеличиваем
            sum_height += (height*2 if height < 4 else 0)

            # если себя запер, то считаем это плохим случаем
            min_height = min(min_height, height)

            if not (0, 0) == cell and cur_height < height:
                min_dh = min(min_dh, height - cur_height)

        # если в заподне, тогда выходим
        if min_dh > 1 and cur_height < 2 and check_block:
            sum_height = 0

        # если себя замуровал, тогда выходим из клетки
        if min_height == 4 and check_block:
            sum_height = 0

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

    def future(self, action):
        "Создаем копию мира, определя"
        f_world = World()

        f_world.size = self.size
        f_world.units_per_player = self.units_per_player

        # описание игровой площадки
        f_world.grid = self.grid.copy()

        # объявляем вспомогательные переменные для определения направления
        push_from, push_to = None, None
        build_at = None

        # копируем игроков
        for player in self.players:
            new_player = player.copy()

            if player.index == action.index:

                if action.atype == "MOVE&BUILD":
                    new_player.x, new_player.y = add_pos((new_player.x, new_player.y), action.dir_1)

                    build_at = add_pos((new_player.x, new_player.y), action.dir_2)

                    #print build_at, action.dir_2
                elif action.atype == "PUSH&BUILD":
                    build_at = add_pos((new_player.x, new_player.y), action.dir_1)
                    push_from = build_at
                    push_to = add_pos(push_from, action.dir_2)

                #print f_world.grid, f_world.grid[5]
                #print build_at, f_world.height(build_at)
                f_world.set_height(build_at, f_world.height(build_at)+1)
            f_world.players.append(new_player)



        for player in self.enemies:
            new_player = player.copy()

            if new_player.position() == push_from:
                new_player.x, new_player.y = push_to
                new_player.pushed = True

            f_world.enemies.append(new_player)

        if build_at in [x.position() for x in f_world.enemies]:
            return None

        # обрабатываем условие, что нельзя стоить на месте противника
        return f_world

    def update(self):
        "Считавыем параметры из консоли"

        self.grid = {}
        self.players = []
        self.enemies = []


        for i in xrange(self.size):
            raw = get_raw()
            for j in xrange(len(raw)):
                self.grid[(j, i)] = int(raw[j]) if not raw[j] == '.' else 4

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

    def maps(self, current_position=None, enemies_position=[]):
        "отображаем карту в виде строки"
        ret = ""
        for i in xrange(self.size):
            if i > 0:
                ret = ret + "\n"

            for j in xrange(self.size):
                position = (j, i)
                if position == current_position:
                    ret = ret + "x"
                elif position in enemies_position:
                    ret = ret + "e"
                else:
                    ret = ret + str(self.grid[position])
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
        h = 4
        if forcell in self.grid:
            h = self.grid[forcell]

        return h

    def set_height(self, forcell, new_height):
        x, y = forcell
        if forcell in self.grid:
            self.grid[forcell] = new_height

        return new_height


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

        # данные для оптимизации
        opt_data = []

        for action in self.player.legals:

            f_world = self.world.future(action)

            if f_world is None:
                continue

            f_player = f_world.players[self.player.index]

            f_build_at = add_pos(f_player.position(), action.dir_2)

            fp = 0.0
            fp = f_world.calc_potential(f_player.position())

            fb = 0.0
            fb = f_world.calc_potential(f_build_at, False)

            fe = 0.0
            for player in f_world.enemies:
                enemy_position = player.position()
                fe += f_world.calc_potential(enemy_position)

            f_dist = dist_pos(self.player.position(), f_build_at)

            f_height = f_world.height(f_player.position())
            f_makegold = int(f_height == 3 and action.atype == "MOVE&BUILD")
            f_build_near = int(self.player.position() == f_build_at)

            Eval = 2.0*f_makegold + 3.0*f_height + 1.5*fp + 0.3*fb - 1.3*fe - 0.5*f_dist
            #Eval = 2.0*f_makegold + 4.0*f_height + 0.4*fp - 1.0*fe

            feature_set = {
                'action': action,
                'value': Eval, #mh*3 - bh,
                'f_makegold': f_makegold,
                'f_height': f_height,
                'f_player': fp,
                'f_build': fb,
                'f_dist': f_dist,
                'f_enemy': fe
            }

            # print feature_set
            # print f_world.maps(self.player.position(), [f_build_at])

            opt_data.append(feature_set)

        solutions = sorted(opt_data, key=lambda el: el['value'], reverse=True)

        # print "\n".join(str(x) for x in solutions)
        if len(solutions) > 0:
            return solutions[0]
        else:
            return None

    def get_action(self):
        return self.find_near_max()


if __name__ == '__main__':

    DEBUG_MODE = True

    # size = int(raw_input())
    # units_per_player = int(raw_input())
    w = World()

    w.initialize()

    # game loop
    while True:

        t = time.time()


        w.update()

        s1 = StrategyWood(0, w)

        solution1 = s1.get_action()
        t1 = (time.time() - t)*1000

        if t1 < 50 and (w.units_per_player > 0):

            s2 = StrategyWood(1, w)
            solution2 = s2.get_action()

            if solution1 is None:
                solution = solution2
            elif solution2 is None:
                solution = solution1
            elif solution1['value'] > solution2['value']:
                solution = solution1
            else:
                solution = solution1
        else:
            solution = solution1

        if solution is None:
            print "LOSE"
        else:
            print solution['action']
