from tdl.map import Map

class GameMap(Map):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.explored = [[False for y in range(height)] for x in range(width)]
        self.highlight = [[False for y in range(height)] for x in range(width)]

def set_highlight(game_map, x, y):
    if (game_map.walkable[x, y] == True):
        game_map.highlight[x][y] = True


def reset_highlight(game_map):
    # TODO: This will cause problems when the map is really big. It can be optimized to only reset tiles around the player.
    for x, y in game_map:
        game_map.highlight[x][y] = False

def make_map(game_map):
    for x, y in game_map:
        game_map.walkable[x, y] = True
        game_map.transparent[x, y] = True

    game_map.walkable[30, 22] = False
    game_map.transparent[30, 22] = False
    game_map.walkable[31, 22] = False
    game_map.transparent[31, 22] = False
    game_map.walkable[32, 22] = False
    game_map.transparent[32, 22] = False