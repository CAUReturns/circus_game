from models.model import *
from controllers.scene import *
import random
from enum import Enum

STAGE_NUM = 1
GAME_TIME = 20
OBST_INTERVAL = 3

OBST_NUM = 2

class Obstacle(Enum):
    DOOLI = 0
    DOUNER = 1

class GameManager:

    def __init__(self):
        self.curr_stage = 0
        self.stage_list = []
        self.hit_scene = None

        for i in range(STAGE_NUM):
            stage = CircusScene()
            self.stage_list.append(stage)

    def init_stage(self, curr_stage):
        stage = self.stage_list[curr_stage]
        self.hit_scene = HitScene(stage)

        stage.add_user(User(stage, self.hit_scene))
        stage.add_landscape(Landscape(stage))
        
        if curr_stage == 0:
            self.obstacle_random_generator_1(curr_stage)
        else:
            pass

    def obstacle_random_generator_1(self, curr_stage):
        stage = self.stage_list[curr_stage]

        for time_slice in range(0, GAME_TIME, OBST_INTERVAL):
            variation = random.randrange(3) - 1
            timing = time_slice - variation

            obstacle = random.randrange(OBST_NUM)
            height = random.randrange(1, 3) * 100

            if obstacle == Obstacle.DOOLI.value:
                print("dooli")
                stage.add_obstacle(Dooli(stage, self.hit_scene, y=height, start_time=timing))
            elif obstacle == Obstacle.DOUNER.value:
                print("douner")
                stage.add_obstacle(Douner(stage, self.hit_scene, y=height, start_time=timing))
            else:
                pass

    def set_curr_stage(self, curr_stage):
        self.curr_stage = curr_stage

    def start_game(self):
        startGame(self.stage_list[0])
