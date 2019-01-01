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
        self.chosen_tile = None
    
    @property
    def speed(self):
        return abs(self.speed_x) + abs(self.speed_y)
    
    def reset(self):
        self.chosen_tile = None
        self.path = []

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

        # TODO: In order for this to work for an arbitrary impulse, the "impulse" needs to be able to go in two directions.
        # So I think I will need to work with something like for x in range(max + 1): for y in range(max + 1), if x + y <= max: then work from here.
        
        # Green
        min = -self.max_impulse
        max = self.max_impulse + 1
        for xi in range(min, max):
            for yi in range(min, max):
                if (abs(xi) + abs(yi)) <= self.max_impulse:
                    xo = self.owner.location.x
                    xd = x + self.speed_x + xi
                    yo = self.owner.location.y
                    yd = y + self.speed_y + yi

                    new_speed = abs(xd - xo) + abs(yd - yo)
                    
                    if new_speed > self.speed:
                        green_list.append((x + self.speed_x + xi, y + self.speed_y + yi))
                    if new_speed == self.speed:
                        yellow_list.append((x + self.speed_x + xi, y + self.speed_y + yi))
                    if new_speed < self.speed:
                        red_list.append((x + self.speed_x + xi, y + self.speed_y + yi))

        return green_list, yellow_list, red_list

    def fetch_path_to_tile(self, destination=None, mouse=None):
        """
        Build a path using only cardinal directions from self to destination.
        """
        
        path = []
        fixed_path = []

        xo, yo = self.owner.location.x, self.owner.location.y

        if mouse:
            xd, yd = mouse.cx, mouse.cy
            destination = (xd, yd)
        if destination:
            xd, yd = destination

        l1, l2, l3 = self.get_movement_range()
        range = l1 + l2 + l3

        if destination in range:
            path = list(libtcod.line_iter(xo, yo, xd, yd))
            if path:
                fixed_path.append(path.pop(0))
        else:
            return []

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

    def choose_tile(self, destination):
        """
        Choose a tile. Remember the path and the destination.
        """
        l1, l2, l3 = self.get_movement_range()
        range = l1 + l2 + l3

        if destination in range:
            self.chosen_tile = destination
            self.fetch_path_to_tile(destination=destination)

    def update_speed(self):
        self.speed_x = 0
        self.speed_y = 0

        if self.path:
            xo, yo = self.owner.location.x, self.owner.location.y
            xd, yd = self.path[-1]
            self.speed_x = xd - xo
            self.speed_y = yd - yo