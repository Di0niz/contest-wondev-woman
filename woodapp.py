# -*- coding: utf-8 -*-
import sys
import math

class GameAction(object):
    "описание игровых действий"
    def __init__(self, param):
        "инициализация действия из командной строки"
        pass
        
class World(object):
    "Описание игровой площадки"
    def __init__(self):
        "Начальные параметры игрового мира"
        self.size = int(raw_input())
        self.units_per_player = int(raw_input())

        # описание игровой площадки
        self.grid = []

    def update(self):
        "Считавыем параметры из консоли"

        self.grid = []

        for _ in xrange(self.size):
            row = raw_input()
            self.grid.append(row)

        for _ in xrange(self.units_per_player):
            players.append( [int(j) for j in raw_input().split()])
            legals.append([])  

    def maps(self):
        "отображаем карту в виде строки"
        ret = None
        for row in grid:
            if not (ret is None):
                ret = ret + "\n"
            else:
                ret = ""

            ret = ret + row
        return ret

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def from_dir(direction):
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
    
def future_position(player, direction):
    x, y = player
    dx, dy = direction
    return x + dx, y + dy

def find_near_max(grid, player, legals):
    
    near = legals[0]
    pos = future_position(player, from_dir(legals[0][2]))
    h_near = height(grid, pos)
    for atype, index, dir_1, dir_2 in legals:
        pos = future_position(player, from_dir(dir_1))
        h = height(grid, pos)
        if h > h_near and h < 4:
            h_near = h
            near = (atype, index, dir_1, dir_2)
    return near
    
    
def height(grid, pos):
    print >> sys.stderr, pos
    x, y = pos
    target = grid[y][x]
    return target
    
def draw_map(grid):
    ret = None
    for row in grid:
        if not (ret is None):
            ret = ret + "\n"
        else:
            ret = ""
        
        ret = ret + row
    return ret

if __name__ == '__main__':

    size = int(raw_input())
    units_per_player = int(raw_input())

    # game loop
    while True:

        grid = []
        legals = []
        players = []
        for i in xrange(size):
            row = raw_input()
            grid.append(row)
        for i in xrange(units_per_player):
            players.append( [int(j) for j in raw_input().split()])
            legals.append([])
        for i in xrange(units_per_player):
            other_x, other_y = [int(j) for j in raw_input().split()]
        legal_actions = int(raw_input())
        for i in xrange(legal_actions):
            raw = raw_input()
            print >> sys.stderr, raw

            atype, index, dir_1, dir_2 = raw.split()

            index = int(index)
            legals[index].append((atype, index, dir_1, dir_2))

        print >> sys.stderr, draw_map(grid)

        for i in xrange(units_per_player):

            player = players[i]

            near = find_near_max(grid, player, legals[i])
            print "%s %s %s %s" % near
