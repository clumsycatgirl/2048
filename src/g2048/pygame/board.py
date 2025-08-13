from ..board import Board
import pygame as pg

screens = {}
clocks = {}

pg.font.init()
FONT = pg.font.SysFont("Helvetica", 72)

class PyBoard(Board):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self._background_colour = (0x00, 0x00, 0x00)
        self._display_width = self._display_height = 800
        
        _hash = hash(self)
        if _hash not in screens:
            screens[_hash] = pg.display.set_mode((800, 800))
        self._hash = _hash
        if _hash not in clocks:
            clocks[_hash] = pg.time.Clock()

        pg.display.set_caption("2048")
        self.running = True
        
        self._FPS = 24

    def render(self) -> None:
        self._screen().fill(self._background_colour)
        pg.draw.rect(self._screen(), (0xFD, 0xF8, 0xD4), (10, 10, self._display_width - 10 * 2, self._display_height - 10 * 2))
        
        # 800 - 20 = 780 / 4 = 190
        # | | | | |
        # 2.5 190 5 190 5 190 5 190 2.5
        base_offset = 20
        cell_width, cell_height = 190, 190

        for x in range(self.height):
            for y in range(self.width):
                if self[x, y] == 0: continue

                rect = pg.Rect(base_offset + x * cell_width, base_offset + y * cell_height, cell_width, cell_height)
                pg.draw.rect(self._screen(), (0x80, 0x00, 0x00), pg.Rect(rect.left + 2, rect.top + 2, rect.width - 4, rect.height - 4), 4)

                text_surface = FONT.render(str(self[x, y]), False, (0x00, 0x00, 0x00))
                new_rect = text_surface.get_rect(center=rect.center)

                self._screen().blit(text_surface, new_rect)

        pg.display.flip()

    def done(self) -> bool:
        return not self.running or super().done()

    def tick(self) -> None:
        self._clock().tick(self._FPS)

    def _clock(self) -> pg.time.Clock:
        return clocks[self._hash]

    def _screen(self) -> pg.Surface:
        return screens[self._hash]

    
