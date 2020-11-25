from bangtal import *
from models.model import *


class Movement(Timer):
    def __init__(self, creature, delay, start_time, max_time):
        self.delay = delay
        self.count = 0
        self.max_time = max_time
        self.creature = creature
        self.creature.moving = True
        super().__init__(start_time)

    def action(self, **kwargs):
        pass

    def after_action(self):
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
            self.after_action()


class Jump(Movement):
    def __init__(self, creature, start_time=0):
        self.frame = 2
        delay = 0.01/self.frame
        max_time = 100*self.frame
        super().__init__(creature, delay, start_time, max_time)

    def action(self):
        dist = 1 if self.count <= self.max_time/2 else -1
        dist *= 5/self.frame
        self.creature.move(0, int(dist))


class Come(Movement):
    def __init__(self, creature, start_time=0, max_time=0):
        self.dir = -1
        delay = 0.001
        super().__init__(creature, delay, start_time, max_time)

    def change_direction(self):
        self.dir = -self.dir

    def action(self):
        self.creature.move(2*self.dir, 0)

    def after_action(self):
        self.creature.finish()
