from bangtal import *
from controllers.libs import *
from models.model import *
from models.interface import *
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
        self.destination = None
        super().__init__('', Formatter.image('background'))
        self.life = []

    def initialize(self, user, obstacles, landscapes, life_cnt, destination, sound):
        if self.user:
            self.user.stop()
            self.user.hide()
            del self.user
        self.user = user
        user.show()
        self.sound = sound
        for obs in self.obstacles:
            obs.stop()
            obs.hide()
            del obs
        self.obstacles = []
        for landscape in self.landscapes:
            landscape.stop()
            landscape.hide()
            del landscape
        self.landscapes = []
        for obs in obstacles:
            self.add_obstacle(obs)
        for ls in landscapes:
            self.add_landscape(ls)
        while len(self.life) < life_cnt:
            self.increase_life()
        if self.destination:
            self.destination.hide()
        self.destination = destination

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

        if self.destination.hit(self.user):
            self.sound.stop()
            if not self.manager.check_victory():
                self.manager.stage_clear()

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
        self.user.hide()
        for obs in self.obstacles:
            obs.stop()
            obs.hide()
        for ls in self.landscapes:
            ls.stop()
            ls.hide()

    def enter(self):
        self.sound.play(loop=True)
        super().enter()


class DefeatScene(Scene):
    def __init__(self, manager):
        super().__init__('', Formatter.image('defeat_scene'))
        self.manager = manager
        self.sound = Sound(Formatter.sound('defeat', ''))
        self.btn = RetryButton(self)

    def enter(self):
        self.sound.play(loop=False)
        super().enter()

    def start_game(self):
        self.sound.stop()
        self.manager.enter_stage_scene.init_scene(self.manager.stage_idx)
        self.manager.enter_stage_scene.enter()


class VictoryScene(Scene):
    def __init__(self, manager):
        super().__init__('', Formatter.image('victory_scene'))
        self.manager = manager
        self.sound = Sound(Formatter.sound('victory', ''))
        self.btn = EndButton(self)

    def enter(self):
        self.sound.play(loop=False)
        super().enter()


class MenuScene(Scene):
    def __init__(self, manager):
        super().__init__('', Formatter.image('main'))
        self.manager = manager
        self.sound = Sound(Formatter.sound('main', ''))
        self.btn = StartButton(self)
        self.rule_btn = RuleButton(self)
        self.sound.play(loop=True)

    def start_game(self):
        self.sound.stop()
        self.manager.init_enter_scene()
        self.manager.enter_stage_scene.enter()


class EnterStageScene(Scene):

    def __init__(self, manager):
        super().__init__('', Formatter.image('enter_stage_scene'))
        self.manager = manager
        self.stage_num_img = []
        self.base_x = 650
        self.base_y = 310
        self.len = 40

    def init_scene(self, number):
        for img in self.stage_num_img:
            img.hide()
        self.stage_num_img = []
        for idx, num in enumerate(str(number)):
            num_img = Number(num, self, self.base_x + idx * self.len, self.base_y)
            self.stage_num_img.append(num_img)

        timer = Timer(2)
        timer.onTimeout = self.manager.start_game
        timer.start()
