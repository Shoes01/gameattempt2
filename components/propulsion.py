import tcod as libtcod
import math

class Propulsion:
    """
    This class will house the movement logic, as well as location logic.
    """
    def __init__(self, peak_momentum, max_impulse):
        self.peak_momentum = peak_momentum
        self.max_impulse = max_impulse
        self.speed_x = 0
        self.speed_y = 0
        self.path = []
    
    @property
    def speed(self):
        return self.speed_x + self.speed_y
    
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

    def fetch_legal_tiles_impulse(self):
        """
        Get a list of tiles the entity may move to given its current impulse.
        """
        results = []
        for x in range(0, self.impulse + int(math.copysign(1, self.impulse))):
            for y in range(0, self.impulse + int(math.copysign(1, self.impulse))):
                if abs(x) + abs(y) == abs(self.impulse):
                    results.append((self.owner.location.x + x, self.owner.location.y + y))
        
        return results
    
    def move(self):
        """
        Move the entity towards its legal tiles.
        """
        results = []

        if not self.path:
            self.owner.action_points = 0
            results.append({'message': 'Player reached the end of path.'})
        elif self.owner.action_points == 0:
            results.append({'message': 'Player spent APs.'})
        else:
            x, y = self.path.pop(0)
            dx, dy = x - self.owner.location.x, y - self.owner.location.y

            self.owner.location.move(dx, dy)
            
            results.append({'message': 'Player moved.'})

        return results

    def fetch_path_to_tile(self, destination):
        """
        Build a path using only cardinal directions from self to destination.
        """
        
        path = []
        fixed_path = []

        xo, yo = self.owner.location.x, self.owner.location.y
        xd, yd = destination

        if destination in self.fetch_legal_tiles():
            path = list(libtcod.line_iter(xo, yo, xd, yd))
            if path:
                fixed_path.append(path.pop(0))

        while (len(path)):
            x1, y1 = fixed_path[-1]
            x2, y2 = path[0]

            if (x1 - x2)*(y1 - y2) == 0:
                # These points are good.
                fixed_path.append(path.pop(0))
            else:
                # These points are diagonal. Insert a new point, with a new x value but the same y value.
                dx = x2 - x1
                new_point = (x1 + dx, y1)
                fixed_path.append(new_point)

        # Remove the tile the entity is currently standing on.
        if fixed_path:
            fixed_path.pop(0)

        self.path = fixed_path

        return self.path
    
    def fetch_path_to_tile_mouse(self, mouse):
        destination = (mouse.cx, mouse.cy)
        return self.fetch_path_to_tile(destination)
    
    def get_movement_range(self):
        """
        Find three lists of tiles the player may move to. 
        First list is in case of speed increase.
        Second list is in case of speed equilibrium.
        Third list is in case of speed decrease.
        """
        
        green_list = []
        yellow_list = []
        red_list = []

        x = self.owner.location.x
        y = self.owner.location.y

        # Green
        for i in range(self.max_impulse + 1):
        #   Ensure that max_impulse is used in the same direction as the speed.
            if self.speed_x != 0:
                green_list.append((x + self.speed_x + int(math.copysign(i, self.speed_x)), y + self.speed_y))
            else:
                green_list.append((x + i, y + self.speed_y))
                green_list.append((x - i, y + self.speed_y))
            if self.speed_y != 0:
                green_list.append((x + self.speed_x, y + self.speed_y + int(math.copysign(i, self.speed_y))))
            else:
                green_list.append((x + self.speed_x, y + i))
                green_list.append((x + self.speed_x, y - i))

        # Yellow
        yellow_list.append((x + self.speed_x, y + self.speed_y))

        # Red
        for i in range(i + 1):
        #   Ensure that max_impulse is used in the same direction as the speed.
            if self.speed_x != 0:
                red_list.append((x + self.speed_x + int(math.copysign(i, self.speed_x)), y + self.speed_y))
            if self.speed_y != 0:
                red_list.append((x + self.speed_x, y + self.speed_y + int(math.copysign(i, self.speed_y))))
        
        return green_list, yellow_list, red_list