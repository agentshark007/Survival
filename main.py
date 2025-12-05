import panda2d


class Game(panda2d.PandaWindow):
    def __init__(self):
        super().__init__(800, 600, "Test Window", panda2d.Resizable.BOTH, panda2d.Anchor.CENTER)

    def initialize(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass


game = Game()
game.start()
