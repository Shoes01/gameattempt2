class Cursor:
    def __init__(self):
        self.minimum = 0        # The minimum amount of tiles the cursor must highlight.
        self.maximum = 0        # The maximum amount of tiles the cursor must highlight.
        self.so_far = 0         # The amount of tiles highlited so far.
        self.target_list = []   # Keep track of which coordinates have been targeted.
    
    def turn_on(self, player, targets):
        self.owner.char = 'X'

        if len(targets) == 0:
            self.owner.x = player.x
            self.owner.y = player.y
        else:
            self.owner.x, self.owner.y = targets[-1]

    def turn_off(self):
        self.owner.char = ' '
        self.owner.x = -1
        self.owner.y = -1
    
    def move(self, move, weapon, player):
        result = []
        dx, dy = move

        # Ensure the first target is in firing range.
        if len(weapon.targets) == 0:
            if player.distance(self.owner.x + dx, self.owner.y + dy) <= weapon.range:
                self.owner.move(dx, dy)
            else:
                result = {'message': 'Target out of range.'}
        # Ensure that the next targets are adjacent to the previous target
        elif len(weapon.targets) > 0:
            tar_x, tar_y = weapon.targets[-1] # Get the most recent target added.
            if abs(tar_x - (self.owner.x + dx)) + abs(tar_y - (self.owner.y + dy)) <= 1:
                self.owner.move(dx, dy)
            else:
                result = {'message': 'Invalid target.'}
        
        return result
    
    def target(self, game_map, weapon):
        result = []

        if len(weapon.targets) < weapon.max_targets:
            if game_map.set_targeted(self.owner.x, self.owner.y):
                weapon.targets.append((self.owner.x, self.owner.y))

                result = {'target': True}
        else:
            result = {'message': 'Targeting failed.'}
        
        return result