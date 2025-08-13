import getpass
import pygame as pg
from .board import PyBoard


def get_input(board: PyBoard) -> str:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            board.running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a:
                return 'a'
            if event.key == pg.K_w:
                return 'w'
            if event.key == pg.K_s:
                return 's'
            if event.key == pg.K_d:
                return 'd'

    return None
