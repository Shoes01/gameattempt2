import tcod as libtcod
import math

from global_variables import distance_to, fill_in_line

class Propulsion:
    """
    This class will house the movement logic, as well as location logic.
    """
    def __init__(self, max_speed, max_impulse):
        self.max_speed = max_speed
        self.max_impulse = max_impulse
        self.speed_x = 0
        self.speed_y = 0
        self.path = []
        self.chosen_tile = None
        self.legal_tiles = {}   # A dict holding 'green', 'yellow' and 'red'. TODO: Should this instead be a tuple (x, y, color)?
    
    @property
    def speed(self):
        return abs(self.speed_x) + abs(self.speed_y)
    
    def reset(self):
        #self.chosen_tile = None
        self.path = []
        self.legal_tiles.clear()

    def calculate_movement_range(self):
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

                    if new_speed > self.max_speed:
                        continue
                    
                    if new_speed > self.speed:
                        green_list.append((x + self.speed_x + xi, y + self.speed_y + yi))
                    if new_speed == self.speed:
                        yellow_list.append((x + self.speed_x + xi, y + self.speed_y + yi))
                    if new_speed < self.speed:
                        red_list.append((x + self.speed_x + xi, y + self.speed_y + yi))

        self.legal_tiles['red'] = red_list
        self.legal_tiles['yellow'] = yellow_list
        self.legal_tiles['green'] = green_list

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

        path = list(libtcod.line_iter(xo, yo, xd, yd))

        if path:
            fixed_path = fill_in_line(path)
            
        else:
            return []

        self.path = fixed_path

        return self.path
    
    def move(self):
        """
        Move the entity towards its legal tiles.
        """
        results = []

        if not self.path:
            self.owner.action_points = 0
        elif self.owner.action_points == 0:
            print('How did the user manage to move the entity so far that they spent all their APs?')
        else:
            x, y = self.path.pop(0)
            dx, dy = x - self.owner.location.x, y - self.owner.location.y

            self.owner.location.move(dx, dy)

        return results

    def choose_tile(self, destination):
        """
        Choose a tile. Remember the path and the destination.
        """
        self.chosen_tile = destination

        legal_tiles = []
        legal_tiles.extend(self.legal_tiles.get('green'))
        legal_tiles.extend(self.legal_tiles.get('yellow'))
        legal_tiles.extend(self.legal_tiles.get('red'))
        
        if destination in legal_tiles:
            self.fetch_path_to_tile(destination=destination)
        else:
            closest_tile = legal_tiles.pop()

            for tile in legal_tiles:
                if distance_to(tile, destination, manhattan=False) < distance_to(closest_tile, destination, manhattan=False):
                    closest_tile = tile
            
            self.fetch_path_to_tile(destination=closest_tile)


    def update_speed(self):
        self.speed_x = 0
        self.speed_y = 0

        if self.path:
            xo, yo = self.owner.location.x, self.owner.location.y
            xd, yd = self.path[-1]
            self.speed_x = xd - xo
            self.speed_y = yd - yo