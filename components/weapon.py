import tcod as libtcod

import factory

class Weapon:
    """
    The Weapon class stores the damage, target, and range properties of a weapon.
    """
    def __init__(self, name, damage, min_targets, max_targets, color, range, cost, projectile=None):
        self.name = name
        self.damage = damage
        self.min_targets = min_targets
        self.max_targets = max_targets
        self.color = color
        self.range = range
        self.cost = cost
        self.projectile = projectile    # Type
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
        results = []
        self.cooldown += self.cost
        
        # Projectile code
        for target in self.targets:
            if self.projectile is factory.ProjectileType.BASIC_PROJECTILE:
                (x, y) = (self.owner.location.x, self.owner.location.y)
                projectile = factory.entity_factory(self.projectile, (x, y), event_queue)
                if projectile.moves_with_player:
                    self.owner.moves_with_player = False
                else:
                    self.owner.moves_with_player = True

                xo, yo = projectile.location.x, projectile.location.y
                xd, yd = target
                
                projectile.projectile.path = list(libtcod.line_iter(xd, yd, xo, yo))

                entities.append(projectile)

        # Simple laser code
        for target in self.targets:
            entity = get_entity_at_location(target, entities)
            if entity is None: 
                continue
            
            results.append(entity.chassis.take_damage(self.damage))
        
        return results

# TODO: Find a better place for this.
def get_entity_at_location(location, entities):
    x, y = location

    for entity in entities:
        if entity.location is not None and x == entity.location.x and y == entity.location.y:
            return entity
    
    return None