from components.location import Location
from systems.movement import cursor_movement

class Cursor:
    def turn_on(self, player, targets=[]):
        self.owner.location = Location()
        self.owner.location.owner = self.owner

        if len(targets) == 0:
            self.owner.location.x = player.location.x
            self.owner.location.y = player.location.y
        else:
            self.owner.location.x, self.owner.location.y = targets[-1]

    def turn_off(self):
        self.owner.location = None
    
    def move(self, move, weapon, player):
        result = []
        dx, dy = move

        # Ensure the first target is in firing range.
        if len(weapon.targets) == 0:
            if player.distance(self.owner.location.x + dx, self.owner.location.y + dy) <= weapon.range:
                cursor_movement(self.owner, dx, dy)
            else:
                result = {'message': 'Target out of range.'}
        # Ensure that the next targets are adjacent to the previous target
        elif len(weapon.targets) > 0:
            tar_x, tar_y = weapon.targets[-1] # Get the most recent target added.
            if abs(tar_x - (self.owner.location.x + dx)) + abs(tar_y - (self.owner.location.y + dy)) <= 1:
                cursor_movement(self.owner, dx, dy)
            else:
                result = {'message': 'Invalid target.'}
        
        return result
    
    def target(self, game_map, weapon):
        result = []

        if len(weapon.targets) < weapon.max_targets:
            if game_map.set_targeted(self.owner.location.x, self.owner.location.y):
                weapon.targets.append((self.owner.location.x, self.owner.location.y))

                result = {'target': True}
        else:
            result = {'message': 'Targeting failed.'}
        
        return result