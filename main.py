from enum import Enum
import panda2d

class ExtendMethod(Enum):
    LEFT = -1
    RIGHT = 1
    UP = 1
    DOWN = -1

class Extension:
    def __init__(self):
        self.scale = 1.0

    def extend(self, pivot, value, direction: ExtendMethod):
        return pivot + (value * direction.value * self.scale)

class Game(panda2d.PandaWindow):
    def __init__(self):
        super().__init__(800, 600, "Test Window", panda2d.Resizable.BOTH, panda2d.Anchor.CENTER)
        self.extension = Extension()
        self.extension.scale = 1.0

        self.extension_change_factor = 20.0
        self.extension_change_offset = 1.0

        self.plus_last_frame = False
        self.minus_last_frame = False

    def update(self):
        growth = self.extension_change_offset + self.extension_change_factor * self.deltatime

        if self.keydown(panda2d.Key.EQUALS) and not self.plus_last_frame:
            self.extension.scale *= growth
            self.plus_last_frame = True
        if self.keydown(panda2d.Key.MINUS) and not self.minus_last_frame:
            self.extension.scale /= growth
            self.minus_last_frame = True

        if not self.keydown(panda2d.Key.EQUALS):
            self.plus_last_frame = False
        if not self.keydown(panda2d.Key.MINUS):
            self.minus_last_frame = False

    def draw(self):
        self.clear(panda2d.Color(0, 0, 0))
        self.fill_rect(self.width / -2, self.height / -2, self.extension.extend(self.width / -2, 5, ExtendMethod.RIGHT), self.height / 2, panda2d.Color(255, 0, 0))
        self.fill_rect(self.extension.extend(self.width / 2, 5, ExtendMethod.LEFT), self.height / -2, self.width / 2, self.height / 2, panda2d.Color(0, 0, 255))
game = Game()
game.start()
