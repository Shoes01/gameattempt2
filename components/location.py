class Location:
    def __init__(self, x=-1, y=-1):
        self.x = x
        self.y = y
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.owner.action_points -= int(27720 / self.owner.mech.speed)   # TODO: Move 27720 to the game init file

        if dx != 0 and dy != 0:
            self.owner.has_moved = True