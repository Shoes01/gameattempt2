import tcod as libtcod

import factory

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
            self.cooldown -= 1
    
    def activate(self):
        """
        Active the weapon, rendering it usable for targeting.
        """
        if self.active == True:
            return {'message': '{0} is already online.'.format(self.name.capitalize())}
        elif self.cooldown > 0:
            return {'message': '{0} has not cooled down yet.'.format(self.name.capitalize())}
        else:
            self.active = True
            return {'message': '{0} online.'.format(self.name.capitalize())}

    def fire(self, entities, event_queue):
        """
        Fire the weapon at all targets.
        """
        # TODO: This needs to be refactored
        results = []
        self.cooldown += self.cost
        
        # Projectile code
        (x, y) = (self.owner.location.x, self.owner.location.y)
        factory.entity_factory(factory.EntityType.OVERSEER, (x, y), entities, self)
        
        return results

# TODO: Find a better place for this.
def get_entity_at_location(location, entities):
    x, y = location

    for entity in entities:
        if entity.location is not None and x == entity.location.x and y == entity.location.y:
            return entity
    
    return None