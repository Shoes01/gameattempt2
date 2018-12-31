from map_objects.tile import Tile

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(False) for y in range(self.height)] for x in range(self.width)]

        tiles[30][22].blocked = True
        tiles[30][22].block_sight = True
        tiles[31][22].blocked = True
        tiles[31][22].block_sight = True
        tiles[32][22].blocked = True
        tiles[32][22].block_sight = True

        return tiles

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False

    def set_highlighted(self, coordinates, color=(255, 255, 255)):
        self.reset_flags()

        for coordinate in coordinates:
            x, y = coordinate
            if self.tiles[x][y].blocked == False:
                self.tiles[x][y].highlighted = color


    def set_targeted(self, x, y):
        self.tiles[x][y].targeted = True
        return True

    def reset_flags(self):
        # TODO: This will cause problems when the map is really big. It can be optimized to only reset tiles around the player.
        for y in range(self.height):
            for x in range(self.width):
                self.tiles[x][y].highlighted = None
                self.tiles[x][y].targeted  = False