# A clone of the arcade game Stacker
# Copyright (C) 2007  Clint Herron
# Copyright (C) 2017-2020  Nguyễn Gia Phong
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""A clone of the arcade game Stacker"""

__version__ = '2.1.0'
__all__ = ['Slacker']

from contextlib import ExitStack, redirect_stdout
from importlib.resources import path
from io import StringIO
from math import cos, pi
from random import randrange
from typing import List, Optional

with redirect_stdout(StringIO()): import pygame
from pygame import (K_0, K_1, K_9, K_ESCAPE, K_SPACE, KEYDOWN,
                    QUIT, K_q, Rect, draw, event, image)
from pygame.display import flip, set_caption, set_icon, set_mode
from pygame.font import Font
from pygame.surface import Surface
from pygame.time import get_ticks

TANGO = {'Butter': ((252, 233, 79), (237, 212, 0), (196, 160, 0)),
         'Orange': ((252, 175, 62), (245, 121, 0), (206, 92, 0)),
         'Chocolate': ((233, 185, 110), (193, 125, 17), (143, 89, 2)),
         'Chameleon': ((138, 226, 52), (115, 210, 22), (78, 154, 6)),
         'Sky Blue': ((114, 159, 207), (52, 101, 164), (32, 74, 135)),
         'Plum': ((173, 127, 168), (117, 80, 123), (92, 53, 102)),
         'Scarlet Red': ((239, 41, 41), (204, 0, 0), (164, 0, 0)),
         'Aluminium': ((238, 238, 236), (211, 215, 207), (186, 189, 182),
                       (136, 138, 133), (85, 87, 83), (46, 52, 54))}

BG_COLOR = TANGO['Aluminium'][5]
COLOR_MAJOR = TANGO['Scarlet Red']
COLOR_MINOR = TANGO['Sky Blue']
MAJOR = 5

INTRO, PLAYING, LOSE, WIN = range(4)
MAX_WIDTH = (1,)*7 + (2,)*5 + (3,)*3
WIN_LEVEL = 15

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 280, 600
BOARD_SIZE = BOARD_WIDTH, BOARD_HEIGHT = 7, 15
TILE_SIZE = 40

MAX_SPEED, WIN_SPEED, SPEED_DIFF = 70, 100, 5
INIT_SPEED = MAX_SPEED + (BOARD_HEIGHT + 1)*SPEED_DIFF


class SlackerTile:
    """SlackerTile(x, y) -> SlackerTile

    Slacker object for storing tiles.
    """

    def __init__(self, screen: Surface,
                 x: float, y: float, state: int = PLAYING,
                 missed_time: Optional[int] = None) -> None:
        self.screen, self.x, self.y = screen, x, y
        if state == LOSE:
            self.dim = 1
        elif missed_time is None:
            self.dim = 0
        else:
            self.dim = 2
        self.missed_time = missed_time
        self.wiggle = state in (INTRO, WIN)

    def get_xoffset(self, maxoffset: float, duration: int = 820) -> float:
        """Return the offset on x-axis to make the tile complete an cycle of
        wiggling oscillation in given duration (in milliseconds).
        """
        if not self.wiggle: return 0
        return maxoffset * cos((get_ticks()/duration+self.y/BOARD_HEIGHT)*pi)

    def get_yoffset(self) -> float:
        """Return the offset on y-axis when the tile is falling."""
        if self.missed_time is None: return 0
        return (get_ticks()-self.missed_time)**2 / 25000

    def isfallen(self) -> bool:
        """Return if the tile has fallen off the screen."""
        return self.y + self.get_yoffset() > BOARD_HEIGHT

    def draw(self, max_x_offset: float = 2.0) -> None:
        """Draw the tile."""
        if self.y < MAJOR:
            color = COLOR_MAJOR
        else:
            color = COLOR_MINOR
        rect = Rect((self.x+self.get_xoffset(max_x_offset))*TILE_SIZE,
                    (self.y+self.get_yoffset())*TILE_SIZE,
                    TILE_SIZE, TILE_SIZE)
        draw.rect(self.screen, color[self.dim], rect)
        draw.rect(self.screen, BG_COLOR, rect, TILE_SIZE//11)


class Slacker:
    """This class provides functions to run the game Slacker, a clone of
    the popular arcade game Stacker.
    """

    def __init__(self, restart: bool = False) -> None:
        self.exit_stack = ExitStack()
        self.font = self.data('VT323-Regular.ttf')
        self.board = [[False]*BOARD_WIDTH for h in range(BOARD_HEIGHT)]
        self.game_state = PLAYING if restart else INTRO
        self.falling_tiles: List[SlackerTile] = []
        self.speed = INIT_SPEED + randrange(5)
        self.speed_ratio = 1.0
        self.width = MAX_WIDTH[-1]
        self.y = BOARD_HEIGHT - 1

    def __enter__(self) -> Slacker:
        pygame.init()
        set_caption('Slacker')
        set_icon(image.load(self.data('icon.png')))
        self.screen = set_mode(SCREEN_SIZE)
        return self

    def __exit__(self, *exc) -> None:
        pygame.quit()
        self.exit_stack.close()

    def data(self, resource: str) -> str:
        """Return a true filesystem path for specified resource."""
        return str(self.exit_stack.enter_context(
            path('slacker_game', resource)))

    def draw_text(self, string: str, height: float):
        """Width-fit the string in the screen on the given height."""
        font = Font(self.font, int(SCREEN_WIDTH*2.5/(len(string)+1)))
        text = font.render(string, False, COLOR_MINOR[0])
        self.screen.blit(text, ((SCREEN_WIDTH - text.get_width()) // 2,
                                int(SCREEN_HEIGHT * height)))

    def intro(self) -> None:
        """Draw the intro screen."""
        for i in [(2, 2), (3, 2), (4, 2), (1.5, 3), (4.5, 3),
                  (1.5, 4), (2, 5), (3, 5), (4, 5), (4.5, 6),
                  (1.5, 7), (4.5, 7), (2, 8), (3, 8), (4, 8)]:
            SlackerTile(self.screen, *i, state=INTRO).draw(1.5)
        if get_ticks() // 820 % 2:
            self.draw_text('Press Spacebar', 0.75)

    def draw_board(self) -> None:
        """Draw the board and the tiles inside."""
        for y, row in enumerate(self.board):
            for x, block in enumerate(row):
                if block:
                    SlackerTile(self.screen, x, y, self.game_state).draw()

        # Draw the falling tiles
        for ft in self.falling_tiles:
            if ft.isfallen():
                self.falling_tiles.remove(ft)
            else:
                ft.draw()

    def update_screen(self) -> None:
        """Draw the whole screen and everything inside."""
        self.screen.fill(BG_COLOR)
        if self.game_state == INTRO:
            self.intro()
        elif self.game_state in (PLAYING, LOSE, WIN):
            self.draw_board()
        flip()

    def update_movement(self) -> None:
        """Update the direction the blocks are moving in."""
        speed = self.speed * self.speed_ratio
        positions = BOARD_WIDTH + self.width - 2
        p = int(round(get_ticks()/speed)) % (positions*2)
        self.x = (-p % positions if p > positions else p) - self.width + 1
        self.board[self.y] = [0 <= x - self.x < self.width
                              for x in range(BOARD_WIDTH)]

    def key_hit(self) -> None:
        """Process the current position of the blocks relatively to the
        ones underneath when user hit the switch, then decide if the
        user will win, lose or go to the next level of the tower.
        """
        if self.y < BOARD_HEIGHT - 1:
            for x in range(max(0, self.x),
                           min(self.x + self.width, BOARD_WIDTH)):
                # If there isn't any block underneath
                if not self.board[self.y + 1][x]:
                    # Get rid of the block not standing on solid ground
                    self.board[self.y][x] = False
                    # Then, add that falling block to falling_tiles
                    self.falling_tiles.append(SlackerTile(
                        self.screen, x, self.y, missed_time=get_ticks()))
        self.width = sum(self.board[self.y])
        if not self.width:
            self.game_state = LOSE
        elif not self.y:
            self.game_state = WIN
        else:
            self.y -= 1
            self.width = min(self.width, MAX_WIDTH[self.y])
            self.speed = MAX_SPEED + self.y*SPEED_DIFF + randrange(5)

    def handle_intro(self) -> bool:
        """Handle events in intro."""
        for e in event.get():
            if e.type == QUIT: return False
            if e.type != KEYDOWN: continue
            if e.key in (K_ESCAPE, K_q): return False
            if e.key == K_SPACE: self.game_state = PLAYING
        return True

    def handle_playing(self) -> bool:
        """Handle events in game."""
        for e in event.get():
            if e.type == QUIT: return False
            if e.type != KEYDOWN: continue
            if e.key == K_SPACE:
                self.key_hit()
            elif e.key in (K_ESCAPE, K_q):
                Slacker.__init__(self)
            # Yes, these are cheats.
            elif e.key == K_0:
                self.width += self.width < BOARD_WIDTH
            elif K_1 <= e.key <= K_9 + 1:
                self.speed_ratio = (K_9-e.key+1) / 5.0
        self.update_movement()
        return True

    def handle_ending(self) -> bool:
        """Handle events in ending screens."""
        for e in event.get():
            if e.type == QUIT: return False
            if e.type == KEYDOWN: Slacker.__init__(self, restart=True)
        return True

    def handle_events(self) -> bool:
        """Handle queued events."""
        if self.game_state == INTRO: return self.handle_intro()
        if self.game_state == PLAYING: return self.handle_playing()
        if self.game_state in (LOSE, WIN): return self.handle_ending()
        return False
