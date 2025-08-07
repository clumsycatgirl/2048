from ..board import Board
import pygame as pg


class PyBoard(Board):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self._background_colour = (0x00, 0x40, 0x40)
        self.screen = pg.display.set_mode((800, 800))
        pg.display.set_caption("2048")
        self.screen.fill(self._background_colour)
        pg.display.flip()
        self.running = True

    def draw(self) -> None:
        pass

    def done(self) -> bool:
        return not self.running or super().done()
