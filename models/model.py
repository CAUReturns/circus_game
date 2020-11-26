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

    def finish(self):
        pass


class Landscape(CustomObject):
    def __init__(self, game_scene):
        img = Formatter.image('landscape')
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
    def __init__(self, x, y, xr, yr, img, game_scene, hit_scene):
        super().__init__(x, y, img, game_scene)
        self.xr = xr
        self.yr = yr
        self.hit_scene = hit_scene

    def move(self, xd, yd):
        super().move(xd, yd)
        if self.scene.check_hit():
            self.hit_scene.enter()


class User(Creature):
    def __init__(self, game_scene, hit_scene):
        self.idx = 0
        img = Formatter.image('user', idx=self.idx)
        self.moving = False
        self.sitting = False
        self.motion = Walk(self)
        super().__init__(100, 100, 90, 100, img, game_scene, hit_scene)
        self.motion.start()

    def jump(self):
        if not self.moving:
            self.stand()
            Jump(self).start()

    def set_hitbox(self, y, xr, yr):
        self.y = y
        self.locate(self.scene, self.x, self.y)
        self.xr = xr
        self.yr = yr

    def sit(self):
        if self.sitting:
            self.stand()
        elif not self.moving:
            self.sitting = True
            img = Formatter.image('user', idx=13)
            self.setImage(img)
            self.set_hitbox(90, 90, 60)
            self.motion.stop()

    def stand(self):
        self.sitting = False
        img = Formatter.image('user', idx=0)
        self.setImage(img)
        self.set_hitbox(100, 90, 100)
        self.motion.start()

    def walk(self):
        self.idx = (self.idx+1) % 13
        img = Formatter.image('user', idx=self.idx)
        self.setImage(img)


class Obstacle(Creature):
    def __init__(self, game_scene, hit_scene, y, xr, yr, start_time, img):
        super().__init__(1300, y, xr, yr, img, game_scene, hit_scene)
        self.motion = Come(self, start_time)
        self.motion.start()

    def hit(self, user):
        x_hit = not (self.x > user.x+user.xr or self.x+self.xr < user.x)
        y_hit = not (self.y > user.y+user.yr or self.y+self.yr < user.y)
        return x_hit and y_hit

    def finish(self):
        if self.x < -150:
            self.scene.remove_obstacle(self)
            self.motion.stop()

    def slow(self):
        self.motion.slow()

    def fast(self):
        self.motion.fast()


class Douner(Obstacle):
    def __init__(self, game_scene, hit_scene, y=100, start_time=0):
        img = Formatter.image('obs1')
        super().__init__(game_scene, hit_scene, y, 103, 60, start_time, img)


class Dooli(Obstacle):
    def __init__(self, game_scene, hit_scene, y=100, start_time=0):
        img = Formatter.image('obs2')
        super().__init__(game_scene, hit_scene, y, 50, 60, start_time, img)
