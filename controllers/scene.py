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
    def __init__(self, manager):
        self.map_idx = 0
        self.user = None
        self.sound = None
        self.manager = manager
        self.direction = 1
        self.obstacles = []
        self.landscapes = []
        super().__init__('', Formatter.image('background'))
        self.life = []

    def initialize(self, user, obstacles, landscapes, life_cnt):
        self.user = user
        self.sound = Sound(Formatter.sound('main', ''))
        self.obstacles = []
        self.landscapes = []
        for obs in obstacles:
            self.add_obstacle(obs)
        for ls in landscapes:
            self.add_landscape(ls)
        for i in range(life_cnt):
            self.increase_life()

    def increase_life(self):
        self.life.append(Life(self, self.life.__len__()))

    def decrease_life(self):
        life = self.life.pop()
        life.hide()
        if self.life.__len__() == 0:
            self.manager.end_game()

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

    def end(self):
        self.sound.stop()
        self.user.stop()
        for obs in self.obstacles:
            obs.stop()
        for ls in self.landscapes:
            ls.stop()

    def enter(self):
        # self.sound.play(loop=True)
        super().enter()


class DefeatScene(Scene):
    def __init__(self, manager):
        self.manager = manager
        self.sound = Sound(Formatter.sound('defeat', ''))
        super().__init__('', Formatter.image('defeat_scene'))

    def enter(self):
        self.sound.play(loop=False)
        super().enter()

    def start_game(self):
        self.sound.stop()
        self.manager.start_game()
