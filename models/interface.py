from bangtal import *
from controllers.libs import *


class CustomInterface(Object):
    def __init__(self, x, y, img, game_scene):
        super().__init__(img)
        self.x = x
        self.y = y
        self.scene = game_scene
        self.locate(game_scene, self.x, self.y)
        self.show()


class RetryButton(CustomInterface):
    def __init__(self, game_scene):
        super().__init__(505, 180, Formatter.image('retry_btn', ''), game_scene)

    def onMouseAction(self, x, y, action):
        self.scene.start_game()


class EndButton(CustomInterface):
    def __init__(self, game_scene):
        super().__init__(467, 180, Formatter.image('end_btn', ''), game_scene)

    def onMouseAction(self, x, y, action):
        endGame()


class StartButton(CustomInterface):
    def __init__(self, game_scene):
        super().__init__(505, 70, Formatter.image('start_btn', ''), game_scene)

    def onMouseAction(self, x, y, action):
        self.scene.start_game()


class RuleButton(CustomInterface):
    def __init__(self, game_scene):
        super().__init__(1100, 535, Formatter.image('rule_btn', ''), game_scene)
        self.clicked = False

    def onMouseAction(self, x, y, action):
        if self.clicked is False:
            scene = Rule(self.scene, self)
            self.hide()

    def show(self):
        super().show()


class Rule(CustomInterface):
    def __init__(self, game_scene, btn):
        super().__init__(100, 20, Formatter.image('rule', ''), game_scene)
        self.setScale(0.9)
        self.btn = btn

    def onMouseAction(self, x, y, action):
        self.hide()
        self.btn.show()
