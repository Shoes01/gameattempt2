import tcod as libtcod
import math

class Propulsion:
    """
    This class will house the movement logic, as well as location logic.
    """
    def __init__(self, peak_momentum, max_impulse):
        self.peak_momentum = peak_momentum
        self.max_impulse = max_impulse
        self.impulse = 0
    
    def change_impulse(self, delta):
        """
        Increase or decrease impulse, never exceeding the maximum.
        """
        self.impulse += delta

        if abs(self.impulse) > self.max_impulse:
            self.impulse = int(math.copysign(self.max_impulse, delta))
    
    def fetch_legal_tiles(self):
        """
        Get a list of tiles the entity may move to.
        """
        results = []

        for x in range(-self.max_impulse, self.max_impulse + 1):
            for y in range(-self.max_impulse, self.max_impulse + 1):
                if abs(x) + abs(y) <= self.max_impulse:
                    results.append((self.owner.location.x + x, self.owner.location.y + y))
        
        return results
    
    def fetch_path_to_tile(self, destination):
        entity = self.owner

        xo, yo = entity.location.x, entity.location.yo
        xd, yd = destination

        path = list(libtcod.line_iter(xo, yo, xd, yd))

        return path
