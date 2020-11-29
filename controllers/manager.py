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
MAX_STAGE = 2


class GameManager:
    def __init__(self):
        self.stage_idx = 1
        self.menu_scene = MenuScene(self)
        self.defeat_scene = DefeatScene(self)
        self.victory_scene = VictoryScene(self)
        self.enter_stage_scene = EnterStageScene(self)
        self.stage = CircusScene(self)
        self.user = None
        self.sound_list = []
        for i in range(1,4):
            filename = 'gameplay' + str(i)
            self.sound_list.append(Sound(Formatter.sound(filename, '')))

    def start_game(self):
        self.initialize_stage()
        self.stage.enter()

    def end_game(self):
        self.stage.end()
        self.stage.destination.hide()
        self.defeat_scene.enter()

    def check_victory(self):
        if self.stage_idx == MAX_STAGE:
            self.victory()
            return True
        return False

    def victory(self):
        self.stage.end()
        self.stage.destination.hide()
        self.victory_scene.enter()

    def stage_clear(self):
        self.stage_idx += 1
        self.enter_stage_scene.init_scene(self.stage_idx)
        self.enter_stage_scene.enter()

    def init_enter_scene(self):
        self.enter_stage_scene.init_scene(self.stage_idx)

    def initialize_stage(self):
        self.user = User(self.stage)
        obstacles = self.get_random_obstacles()
        destination = Destination(self.stage, self.stage_idx, start_time=GAME_TIME + 3)
        landscapes = [Landscape(self.stage, self.stage_idx)]
        curr_sound = self.sound_list[self.stage_idx % 3 - 1]
        self.stage.initialize(self.user, obstacles, landscapes, LIFE_CNT, destination, curr_sound)

        return self.stage

    def get_random_obstacles(self):
        obstacles = []
        stage = self.stage
        timing = 0
        while timing < GAME_TIME:
            variation = random.randrange(3)
            timing = timing + variation - 0.4 * self.stage_idx

            obstacle = random.randrange(OBSTACLE_NUM)
            height = random.randrange(1, 3) * 100

            if obstacle == ObstacleType.DOOLI.value:
                obstacles.append(Dooli(stage, self.stage_idx*2, y=height, start_time=timing))
            elif obstacle == ObstacleType.DOUNER.value:
                obstacles.append(Douner(stage, self.stage_idx*2, y=height, start_time=timing))
            timing += 2

        return obstacles

    def get_menu(self):
        return self.menu_scene
