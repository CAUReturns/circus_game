from models.model import *
from controllers.scene import *
import random
from enum import Enum


class ObstacleType(Enum):
    DOOLI = 0
    DOUNER = 1


STAGE_NUM = 1
GAME_TIME = 20
OBSTACLE_INTERVAL = 3
OBSTACLE_NUM = ObstacleType.__len__()
LIFE_CNT = 3


class GameManager:
    def __init__(self):
        self.stage_idx = 0
        self.stages = []
        self.menu_scene = MenuScene(self)
        self.defeat_scene = DefeatScene(self)
        for i in range(STAGE_NUM):
            self.stages.append(CircusScene(self))

    def start_game(self):
        stage = self.initialize_stage()
        stage.enter()

    def end_game(self):
        stage = self.get_stage()
        stage.end()
        self.defeat_scene.enter()

    def initialize_stage(self):
        stage = self.get_stage()
        user = User(stage)
        obstacles = self.get_random_obstacles()
        landscapes = [Landscape(stage)]
        stage.initialize(user, obstacles, landscapes, LIFE_CNT)
        return stage

    def get_random_obstacles(self):
        obstacles = []
        stage = self.get_stage()
        for time_slice in range(0, GAME_TIME, OBSTACLE_INTERVAL):
            variation = random.randrange(3) - 1
            timing = time_slice - variation

            obstacle = random.randrange(OBSTACLE_NUM)
            height = random.randrange(1, 3) * 100

            if obstacle == ObstacleType.DOOLI.value:
                obstacles.append(Dooli(stage, y=height, start_time=timing))
            elif obstacle == ObstacleType.DOUNER.value:
                obstacles.append(Douner(stage, y=height, start_time=timing))
        return obstacles

    def get_stage(self):
        return self.stages[self.stage_idx]

    def get_menu(self):
        return self.menu_scene
