import tcod as libtcod

import factory

from game_states import GameStates
from global_variables import TICKS_PER_TURN

class Weapon:
    """
    The Weapon class stores the damage, target, and range properties of a weapon.
    """
    def __init__(self, name, damage, min_targets, max_targets, color, range, cost, rate_of_fire, projectile=None):
        self.name = name
        self.damage = damage
        self.min_targets = min_targets
        self.max_targets = max_targets
        self.color = color
        self.range = range
        self.cost = cost
        self.rate_of_fire = rate_of_fire
        self.projectile = projectile        # factory.py, ProjectileType
        self.targets = []
        self.active = False
        self.cooldown = 0
        
    def reset(self):
        self.targets = []
        self.active = False
        if self.cooldown > 0: 
            self.cooldown -= 4
        if self.cooldown < 0:
            self.cooldown = 0
    
    def activate(self):
        """
        Active the weapon, rendering it usable for targeting.
        """
        if self.active == True:
            return {'message': '{0} attemps to activate their {1}, but it is already online.'.format(self.owner.name.capitalize(), self.name.capitalize())}
        elif self.cooldown > 0:
            return {'message': '{0} attemps to activate their {1}, but it has not cooled down.'.format(self.owner.name.capitalize(), self.name.capitalize())}
        else:
            self.active = True
            return {'message': '{0} actviates their {1}.'.format(self.owner.name.capitalize(), self.name.capitalize())}

    def fire(self):
        """
        Fire the weapon at all targets.
        """
        results = []
        location = (self.owner.location.x, self.owner.location.y)
        self.cooldown += self.cost

        if self.owner.required_game_state == GameStates.PLAYER_TURN:
            required_game_state = GameStates.ENEMY_TURN
        else:
            required_game_state = GameStates.PLAYER_TURN

        for target in self.targets:
            if self.owner.action_points <= 0:
                break

            results.append({'new_projectile': (self.projectile, location, target, self.owner.action_points, required_game_state)})

            self.owner.action_points -= TICKS_PER_TURN // self.rate_of_fire            
        
        return results