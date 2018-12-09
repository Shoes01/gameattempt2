from entity import get_entity_at_location

class Weapon:
    """
    The Weapon class stores the damage, target, and range properties of a weapon.
    """
    def __init__(self, name, damage, min_targets, max_targets, color, range):
        self.name = name
        self.damage = damage
        self.min_targets = min_targets
        self.max_targets = max_targets
        self.color = color
        self.range = range
        self.targets = []
        self.active = False
        
    def reset(self):
        self.targets = []
        self.active = False
    
    def activate(self):
        """
        Active the weapon, rendering it usable for targeting.
        """
        if self.active == True:
            return {'message': '{0} is already online.'.format(self.name.capitalize())}
        else:
            self.active = True
            return {'message': '{0} online.'.format(self.name.capitalize())}

    def fire(self, entities):
        """
        Fire the weapon at all targets.
        """
        results = []
        
        for target in self.targets:
            entity = get_entity_at_location(target, entities)
            if entity is None: 
                continue
            
            results.append(entity.chassis.take_damage(self.damage))
        
        return results