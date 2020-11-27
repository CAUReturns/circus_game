from bangtal import *
from models.model import *


class Movement(Timer):
    def __init__(self, creature, delay, start_time, max_time):
        self.delay = delay
        self.count = 0
        self.max_time = max_time
        self.creature = creature
        self.stopped = False
        self.creature.moving = True
        super().__init__(start_time)

    def action(self, **kwargs):
        pass

    def after_action(self):
        pass

    def stop(self):
        self.stopped = True
        super().stop()

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
    def __init__(self, creature, start_time=0):
        self.frame = 0.5
        delay = 0.01/self.frame
        max_time = 100*self.frame
        super().__init__(creature, delay, start_time, max_time)

    def action(self):
        if self.creature.damaging:
            self.stop()
        dist = 1 if self.count <= self.max_time/2 else -1
        dist *= 5/self.frame
        if not self.stopped:
            self.creature.move(0, int(dist))


class Come(Movement):
    def __init__(self, creature, start_time=0, max_time=0):
        self.dir = -1
        self.speed = 2
        self.stage_speed = 0
        delay = 0.001
        super().__init__(creature, delay, start_time, max_time)

    def change_direction(self):
        self.dir = -self.dir

    def action(self):
        if self.stopped:
            return
        self.creature.move(int(self.speed*self.dir - self.stage_speed), 0)
        self.creature.finish()

    def slow(self):
        self.speed = 1.5

    def fast(self):
        self.speed = 2

    def set_stage_speed(self, num):
        self.stage_speed = num


class Walk(Movement):
    def __init__(self, creature, start_time=0, max_time=0):
        self.dir = -1
        delay = 0.001
        super().__init__(creature, delay, start_time, max_time)
        self.creature.moving = False

    def action(self):
        self.creature.walk()


class Damage(Timer):
    def __init__(self, creature):
        super().__init__(0.5)
        self.creature = creature
        self.creature.set_hitbox(100, 90, 100)

    def onTimeout(self):
        if not self.creature.ended:
            self.creature.stand()
            self.creature.damaging = False
