from bangtal import *
from controllers.libs import *
from models.model import *
from enum import Enum


class Key(Enum):
    LEFT = 1
    RIGHT = 4
    UP = 23
    DOWN = 19


class CircusScene(Scene):
    def __init__(self):
        self.map_idx = 0
        self.user = None
        self.direction = 1
        self.obstacles = []
        self.landscapes = []
        super().__init__('', Formatter.image('background'))
        self.life = []
        for i in range(3):
            self.increase_life()

    def stop_all(self):
        self.user.stop()
        for obs in self.obstacles:
            obs.stop()
        for ls in self.landscapes:
            ls.stop()

    def increase_life(self):
        self.life.append(Life(self, self.life.__len__()))

    def decrease_life(self):
        life = self.life.pop()
        life.hide()
        if self.life.__len__() == 0:
            self.stop_all()

    def add_user(self, user):
        self.user = user

    def add_obstacle(self, obstacle):
        self.obstacles.append(obstacle)

    def remove_obstacle(self, obs):
        if self.obstacles.count(obs) > 0:
            self.obstacles.remove(obs)
            obs.hide()

    def add_landscape(self, landscape):
        self.landscapes.append(landscape)

    def check_hit(self):
        hit = False
        for ob in self.obstacles:
            hit = hit or ob.hit(self.user)
        if hit:
            self.user.damage()
            self.decrease_life()

    def move(self, idx):
        if self.direction == idx:
            return
        self.direction = -self.direction
        for landscape in self.landscapes:
            landscape.change_direction()
        if idx == -1:
            for obs in self.obstacles:
                obs.slow()
        elif idx == 1:
            for obs in self.obstacles:
                obs.fast()

    def onKeyboard(self, key, pressed):
        if not pressed:
            return
        if key == Key.RIGHT.value:
            self.move(1)
        elif key == Key.LEFT.value:
            self.move(-1)
        elif key == Key.UP.value:
            self.user.jump()
        elif key == Key.DOWN.value:
            self.user.sit()
