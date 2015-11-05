#!/usr/bin/python

import libtcodpy as TCOD

import math
import shelve
import textwrap


SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

MAP_WIDTH = 80
MAP_HEIGHT = 45

LIMIT_FPS = 20

dark_wall = TCOD.Color(0, 0, 100)
dark_ground = TCOD.Color(50, 50, 150)


class Object:
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y 
        self.char = char
        self.color = color

    def move(self, dx, dy):
        if not map[self.x + dx][self.y + dy].blocked:
            self.x += dx
            self.y += dy

    def draw(self):
        # sets the color and draws the char
        TCOD.console_set_default_foreground(con, self.color)
        TCOD.console_put_char(con,
                              self.x, self.y, self.char,
                              TCOD.BKGND_NONE)

    def clear(self):
        TCOD.console_put_char(con, self.x, self.y, ' ', TCOD.BKGND_NONE)

class Tile:
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked

        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

def make_map():
    global map
    map = [[ Tile(False)
        for y in range(MAP_HEIGHT) ]
            for x in range(MAP_WIDTH) ]
            
    # places two pillars to test map
    map[30][22].blocked = True
    map[30][22].block_sight = True
    map[50][22].blocked = True
    map[50][22].block_sight = True

def render_all():
    global light_wall
    global light_ground
    
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            wall = map[x][y].block_sight
            if wall:
                TCOD.console_set_char_background(con, x, y, dark_wall, TCOD.BKGND_SET)
            else:
                TCOD.console_set_char_background(con, x, y, dark_ground, TCOD.BKGND_SET)
                
    for object in objects:
        object.draw()
        
    TCOD.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    
def handle_keys():
    #key = TCOD.console_check_for_keypress()
    key = TCOD.console_wait_for_keypress(True)

    if key.vk == TCOD.KEY_ENTER and key.lalt:
        TCOD.console_set_fullscreen(not TCOD.console_is_fullscreen())
    elif key.vk == TCOD.KEY_ESCAPE:
        return True

    if    TCOD.console_is_key_pressed(TCOD.KEY_UP   ):
        player.move(0, -1)
    elif  TCOD.console_is_key_pressed(TCOD.KEY_DOWN ):
        player.move(0, 1)
    elif  TCOD.console_is_key_pressed(TCOD.KEY_LEFT ):
        player.move(-1, 0)
    elif  TCOD.console_is_key_pressed(TCOD.KEY_RIGHT):
        player.move(1, 0)

###################
##  INIT & MAIN  ##
###################

TCOD.console_set_custom_font("arial12x12.png",
                                 TCOD.FONT_TYPE_GREYSCALE |
                                 TCOD.FONT_LAYOUT_TCOD)
TCOD.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, "QWEST", False)
TCOD.sys_set_fps(LIMIT_FPS)
con = TCOD.console_new(MAP_WIDTH, MAP_HEIGHT)

player = Object(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', TCOD.white)
npc = Object(SCREEN_WIDTH/2 - 5, SCREEN_HEIGHT/2, '@', TCOD.yellow)
objects = [npc, player]

make_map()


while not TCOD.console_is_window_closed():
    render_all()

    TCOD.console_flush()

    for object in objects:
        object.clear

    exit = handle_keys()
    if exit:
        break


#if __name__ == "__main__":
#   main()