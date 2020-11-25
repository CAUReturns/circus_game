from bangtal import *
from controllers.libs import *
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

    def add_user(self, user):
        self.user = user

    def add_obstacle(self, obstacle):
        self.obstacles.append(obstacle)

    def add_landscape(self, landscape):
        self.landscapes.append(landscape)

    def check_hit(self):
        hit = False
        for ob in self.obstacles:
            hit = hit or ob.hit(self.user)
        if hit:
            print('Hit!')

    def move(self, idx):
        if self.direction == idx:
            return
        self.direction = -self.direction
        for landscape in self.landscapes:
            landscape.change_direction()

    def onKeyboard(self, key, pressed):
        if not pressed:
            return
        if key == Key.RIGHT.value:
            self.move(1)
        elif key == Key.LEFT.value:
            self.move(-1)
        elif key == Key.UP.value:
            self.user.jump()
