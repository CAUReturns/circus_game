from models.motion import *
from controllers.libs import *


class CustomObject(Object):
    def __init__(self, x, y, img, game_scene):
        super().__init__(img)
        self.x = x
        self.y = y
        self.ended = False
        self.motion = None
        self.scene = game_scene
        self.locate(game_scene, self.x, self.y)
        self.show()

    def move(self, xd, yd):
        self.x += xd
        self.y += yd
        self.locate(self.scene, self.x, self.y)

    def stop(self):
        if self.motion is not None:
            self.ended = True
            self.motion.stop()

    def finish(self):
        pass


class Life(CustomObject):
    def __init__(self, game_scene, idx):
        img = Formatter.image('life')
        super().__init__(1065+idx*60, 650, img, game_scene)


class Landscape(CustomObject):
    def __init__(self, game_scene, stage):
        img = Formatter.image('landscape')
        super().__init__(1300, 419, img, game_scene)
        self.motion = Come(self)
        self.motion.set_stage_speed = stage
        self.motion.start()

    def change_direction(self):
        self.motion.change_direction()

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


class User(Creature):
    def __init__(self, game_scene):
        self.idx = 0
        img = Formatter.image('user', idx=self.idx)
        self.damaging = False
        self.moving = False
        self.sitting = False
        super().__init__(100, 100, 90, 100, img, game_scene)
        self.motion = Walk(self)
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

    def damage(self):
        self.damaging = True
        self.motion.stop()
        self.set_hitbox(100, 90, 100)
        img = Formatter.image('user', idx=14)
        self.setImage(img)
        Damage(self).start()

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
    def __init__(self, game_scene, stage, y, xr, yr, start_time, img):
        super().__init__(1300, y, xr, yr, img, game_scene)
        self.already_hit = False
        self.motion = Come(self, start_time)
        self.motion.set_stage_speed(stage)
        self.motion.start()

    def hit(self, user):
        x_hit = not (self.x > user.x+user.xr or self.x+self.xr < user.x)
        y_hit = not (self.y > user.y+user.yr or self.y+self.yr < user.y)
        if x_hit and y_hit and not self.already_hit:
            self.already_hit = True
            return True
        return False

    def finish(self):
        if self.x < -150:
            self.scene.remove_obstacle(self)
            super().stop()
        self.scene.check_hit()

    def slow(self):
        self.motion.slow()

    def fast(self):
        self.motion.fast()


class Douner(Obstacle):
    def __init__(self, game_scene, stage, y=100, start_time=0):
        img = Formatter.image('obs1')
        super().__init__(game_scene, stage, y, 50, 60, start_time, img)


class Dooli(Obstacle):
    def __init__(self, game_scene, stage, y=100, start_time=0):
        img = Formatter.image('obs2')
        super().__init__(game_scene, stage, y, 50, 60, start_time, img)


class Destination(Obstacle):
    def __init__(self, game_scene, stage, y=100, start_time=0):
        img = Formatter.image('destination')
        super().__init__(game_scene, stage, y, 50, 60, start_time, img)


class Number(Object):
    def __init__(self, num, target_scene, x, y, scale=1.0):
        img = None
        if num == '0':
            img = Formatter.image('0')
        elif num == '1':
            img = Formatter.image('1')
        elif num == '2':
            img = Formatter.image('2')
        elif num == '3':
            img = Formatter.image('3')
        elif num == '4':
            img = Formatter.image('4')
        elif num == '5':
            img = Formatter.image('5')
        elif num == '6':
            img = Formatter.image('6')
        elif num == '7':
            img = Formatter.image('7')
        elif num == '8':
            img = Formatter.image('8')
        else:
            img = Formatter.image('9')
        super().__init__(img)
        self.x = x
        self.y = y
        self.scale = scale
        self.scene = target_scene
        self.locate(target_scene, self.x, self.y)
        self.setScale(self.scale)
        self.show()
