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
        self.cruising_speed = max_speed
    
    @property
    def speed(self):
        return abs(self.speed_x) + abs(self.speed_y)
    
    def reset(self):
        self.path.clear()
        self.legal_tiles.clear()
    
    def choose_tile(self, tile, game_map):
        """
        Attempt to choose a tile.
        """
        ### Choose tile.
        self.chosen_tile = tile
        xo, yo = self.owner.location.x, self.owner.location.y
        xd, yd = tile

        ### Check to see if it's in the legal tile range.
        legal_tiles = []
        legal_tiles.extend(self.legal_tiles.get('green'))
        legal_tiles.extend(self.legal_tiles.get('yellow'))
        legal_tiles.extend(self.legal_tiles.get('red'))

        if legal_tiles and tile in legal_tiles:
            path = list(libtcod.line_iter(xo, yo, xd, yd))

            if path:
                self.path = fill_in_line(path)
                        
            return {}

        ### Adjust speed.
        # Calculate true_angle
        xc, yc = xo + self.speed_x, yo + self.speed_y   # This is the center of the legal_tiles grid.

        dx = xd - xc
        dy = yd - yc
        
        true_angle = math.atan2(dy, dx)
        true_angle = int(true_angle * 180 / math.pi) + 180
        # Now loop over all possible impulses in order to find the closest angle.
        available_impulse = self.max_speed - self.speed
        if available_impulse > self.max_impulse:
            available_impulse = self.max_impulse

        closest_angle = 999
        closest_impulse = 0

        for impulse_x in range(-available_impulse, available_impulse + 1):
            for impulse_y in range(-available_impulse, available_impulse + 1):
                # Try every combo of impulse available.
                if ( abs(impulse_x) + abs(impulse_y) <= available_impulse and
                     abs(self.speed_x + impulse_x) + abs(self.speed_y + impulse_y) <= self.cruising_speed):
                    # If it's not more than what's available, see what the angle would be.
                    new_angle = math.atan2(impulse_y, impulse_x)
                    new_angle = int(new_angle * 180 / math.pi) + 180

                    if ( abs(new_angle - true_angle) < abs(closest_angle - true_angle) or 
                        (abs(new_angle - true_angle) == abs(closest_angle - true_angle) and abs(impulse_x) + abs(impulse_y) > closest_impulse)):
                        # If the angle is close, then we have a new coordinate.
                        closest_angle = new_angle
                        closest_impulse = abs(impulse_x) + abs(impulse_y)
                        dx = impulse_x
                        dy = impulse_y

        new_xd, new_yd = xo + dx + self.speed_x, yo + dy + self.speed_y

        path = list(libtcod.line_iter(xo, yo, new_xd, new_yd))

        if path:
            self.path = fill_in_line(path)            

        return {}
    
    def change_cruising_speed(self, delta):
        """
        Change the maximum speed the entity will move at.
        """
        self.cruising_speed += delta

        if self.cruising_speed > self.max_speed:
            self.cruising_speed = self.max_speed
        elif self.cruising_speed < 1:
            self.cruising_speed = 1
        
        if self.cruising_speed + self.max_impulse < self.speed:
            self.cruising_speed -= delta
            return {'message': 'Cruising speed cannot go lower than {0}.'.format(self.cruising_speed)}


        
        self.reset()

        return {'message': 'Cruising speed set to {0}.'.format(self.cruising_speed)}

    def calculate_movement_range(self, game_map):
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
                    line = list(libtcod.line_iter(xo, yo, xd, yd))
                    good_tile = True

                    if new_speed > self.max_speed:
                        # Can't exceed max speed.
                        continue
                    if game_map.tiles[xd][yd].blocked:
                        # Can't path to blocked tiles.
                        continue

                    for tile in line:
                        xt, yt = tile
                        if game_map.tiles[xt][yt].blocked:
                            # Can't path to tiles behind blocked tiles.
                            good_tile = False
                    
                    if new_speed > self.speed and new_speed <= self.cruising_speed and good_tile:
                        green_list.append((x + self.speed_x + xi, y + self.speed_y + yi))
                    if new_speed == self.speed and new_speed <= self.cruising_speed and good_tile:
                        yellow_list.append((x + self.speed_x + xi, y + self.speed_y + yi))
                    if new_speed < self.speed and new_speed <= self.cruising_speed and good_tile:
                        red_list.append((x + self.speed_x + xi, y + self.speed_y + yi))

        self.legal_tiles['red'] = red_list
        self.legal_tiles['yellow'] = yellow_list
        self.legal_tiles['green'] = green_list

    def build_path(self):
        """
        Build a path using only cardinal directions from self to chosen_tile.
        """
        path = []
        legal_tiles = []
        closest_tile = None

        legal_tiles.extend(self.legal_tiles.get('green'))
        legal_tiles.extend(self.legal_tiles.get('yellow'))
        legal_tiles.extend(self.legal_tiles.get('red'))

        if len(legal_tiles) > 0 and self.chosen_tile not in legal_tiles:
            closest_tile = legal_tiles.pop()
            for tile in legal_tiles:
                if distance_to(tile, self.chosen_tile, manhattan=False) < distance_to(closest_tile, self.chosen_tile, manhattan=False):
                    closest_tile = tile

        xo, yo = self.owner.location.x, self.owner.location.y
        xd, yd = self.chosen_tile
        if closest_tile:
            xd, yd = closest_tile

        path = list(libtcod.line_iter(xo, yo, xd, yd))

        if path:
            self.path = fill_in_line(path)            
            return self.path
        
        return []

    def update_speed(self):
        if self.path:
            xo, yo = self.owner.location.x, self.owner.location.y
            xd, yd = self.path[-1]

            if (xd, yd) in self.legal_tiles.get('yellow'):
                # Speed doesn't change.
                pass
            elif (xd, yd) in self.legal_tiles.get('green'):
                # Speed does change.
                self.speed_x = xd - xo
                self.speed_y = yd - yo
            elif (xd, yd) in self.legal_tiles.get('red'):
                # Speed does change.
                self.speed_x = xd - xo
                self.speed_y = yd - yo
            else:
                # If the path doesn't end inside the red tile range, it's because the player is unable to path safely.
                # Their speed should drop as low as possible as a precaution.
                if self.speed_x > 0:
                    self.speed_x -= self.max_impulse // 2
                elif self.speed_x < 0:
                    self.speed_x += self.max_impulse // 2
                if self.speed_y > 0:
                    self.speed_y -= self.max_impulse // 2
                elif self.speed_y < 0:
                    self.speed_y += self.max_impulse // 2
        else:
            self.speed_x = 0
            self.speed_y = 0
            print('There was no path in the update_speed function.')