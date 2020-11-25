from models.motion import *
from controllers.libs import *


class CustomObject(Object):
    def __init__(self, x, y, img, game_scene):
        super().__init__(img)
        self.x = x
        self.y = y
        self.scene = game_scene
        self.locate(game_scene, self.x, self.y)
        self.show()

    def move(self, xd, yd):
        self.x += xd
        self.y += yd
        self.locate(self.scene, self.x, self.y)


class Landscape(CustomObject):
    def __init__(self, game_scene, idx):
        img = Formatter.image('landscape', idx)
        super().__init__(1300, 419, img, game_scene)
        self.movement = Come(self)
        self.movement.start()

    def change_direction(self):
        self.movement.change_direction()

    def move(self, xd, yd):
        if self.x < -130:
            self.x = 1300+xd
        elif self.x > 1300:
            self.x = -130+xd
        super().move(xd, yd)


class Creature(CustomObject):
    def __init__(self, x, y, xr, yr, img, game_scene):
        super().__init__(x, y, img, game_scene)
        self.xr = xr
        self.yr = yr

    def move(self, xd, yd):
        super().move(xd, yd)
        self.scene.check_hit()


class User(Creature):
    def __init__(self, game_scene):
        img = Formatter.image('user')
        self.moving = False
        super().__init__(100, 100, 200, 100, img, game_scene)

    def jump(self):
        if not self.moving:
            Jump(self).start()


class Obstacle(Creature):
    def __init__(self, game_scene, idx):
        img = Formatter.image('obs', idx)
        super().__init__(1300, 100, 100, 100, img, game_scene)
        Come(self, 800).start()

    def hit(self, user):
        x_hit = abs(self.x-user.x) <= max(self.xr, user.xr)
        y_hit = abs(self.y-user.y) <= max(self.yr, user.yr)
        return x_hit and y_hit
