from map_objects.tile import Tile

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(False) for y in range(self.height)] for x in range(self.width)]

        tiles[40][9].blocked = True
        tiles[40][9].block_sight = True
        tiles[41][9].blocked = True
        tiles[41][9].block_sight = True
        tiles[42][9].blocked = True
        tiles[42][9].block_sight = True
        tiles[43][9].blocked = True
        tiles[43][9].block_sight = True
        tiles[44][9].blocked = True
        tiles[44][9].block_sight = True
        tiles[45][9].blocked = True
        tiles[45][9].block_sight = True
        tiles[46][9].blocked = True
        tiles[46][9].block_sight = True


        return tiles

    def set_highlighted(self, coordinates, color=(255, 255, 255)):
        for coordinate in coordinates:
            x, y = coordinate
            if self.tiles[x][y].blocked == False:
                self.tiles[x][y].highlighted = color
    
    def reset_highlighted(self):
        # TODO: This will cause problems when the map is really big. It can be optimized to only reset tiles around the player.
        for y in range(self.height):
            for x in range(self.width):
                self.tiles[x][y].highlighted = None
    
    def reset_pathable(self):
        for y in range(self.height):
            for x in range(self.width):
                self.tiles[x][y].pathable = None

    def set_pathable(self, coordinates, color=(255, 255, 255)):
        for coordinate in coordinates:
            x, y = coordinate
            if len(self.tiles) >= x and len(self.tiles[x]) >= y:
                if self.tiles[x][y].blocked == False:
                    self.tiles[x][y].pathable = color

    def set_targeted(self, x, y):
        self.tiles[x][y].targeted = True
        return True

    def reset_flags(self):
        # TODO: This will cause problems when the map is really big. It can be optimized to only reset tiles around the player.
        for y in range(self.height):
            for x in range(self.width):
                self.tiles[x][y].highlighted = None
                self.tiles[x][y].targeted  = False
                self.tiles[x][y].pathable = None