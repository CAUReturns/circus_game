from bangtal import *
from models.model import *


class Movement(Timer):
    def __init__(self, creature, delay, max_time):
        self.delay = delay
        self.count = 0
        self.max_time = max_time
        self.creature = creature
        self.creature.moving = True
        super().__init__(self.delay)

    def action(self, **kwargs):
        pass

    def onTimeout(self):
        self.count += 1
        self.action()
        if self.count < self.max_time or self.max_time == 0:
            self.set(self.delay)
            self.start()
        else:
            self.creature.moving = False
            self.count = 0
            self.stop()


class Jump(Movement):
    def __init__(self, creature):
        self.frame = 2
        delay = 0.01/self.frame
        max_time = 40*self.frame
        super().__init__(creature, delay, max_time)

    def action(self):
        dist = 1 if self.count <= self.max_time/2 else -1
        dist *= 7/self.frame
        self.creature.move(0, int(dist))


class Come(Movement):
    def __init__(self, creature, max_time=0):
        self.dir = -1
        delay = 0.01
        super().__init__(creature, delay, max_time)

    def change_direction(self):
        self.dir = -self.dir

    def action(self):
        self.creature.move(2*self.dir, 0)
