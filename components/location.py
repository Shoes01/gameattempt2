from global_variables import TICKS_PER_TURN

class Location:
    def __init__(self, x=-1, y=-1):
        self.x = x
        self.y = y
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        if self.owner.cursor is None:
            self.owner.action_points -= TICKS_PER_TURN // self.owner.propulsion.speed