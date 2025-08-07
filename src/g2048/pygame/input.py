import getpass
import pygame as pg
from .board import PyBoard


def get_pyinput(board: PyBoard) -> str:
    for event in pg.event.get():
        if event.type == pygame.QUIT:
            board.running = False

    return getpass.getpass("")
