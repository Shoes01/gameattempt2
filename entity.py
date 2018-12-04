import math

from render_functions import RenderOrder

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, char, color, name, has_moved=False, render_order=RenderOrder.CORPSE, mech=None, cursor=None, weapon=None, ai=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.has_moved = False
        self.render_order = render_order
        self.mech = mech
        self.cursor = cursor
        self.weapon = weapon
        self.ai = ai

        if self.mech:   self.mech.owner = self        
        if self.cursor: self.cursor.owner = self
        if self.weapon: self.weapon.owner = self
        if self.ai:     self.ai.owner = self

    def move(self, dx, dy):
        """
        Move the entity according to the rules of momentum.
        Cares about obstacles.
        """
        if self.mech.calculate_accumulated_momentum() < self.mech.calculate_maximum_momentum():
            # Allow the player to move.

            # The trivial case: the mech is at rest.
            if self.mech.maximum_horizontal_momentum == 0 and self.mech.maximum_vertical_momentum == 0 and self.mech.impulse == 1:
                # Allow the player to move in any direction.
                self.fly(dx, dy)
                self.mech.accumulated_horizontal_momentum += dx
                self.mech.accumulated_vertical_momentum += dy
                self.mech.has_spent_impulse = True
            
            # The non-trivial case: the mech is moving, so there are some directions that are not allowed.
            # Moving along the x-axis
            elif abs(self.mech.accumulated_horizontal_momentum) < abs(self.mech.maximum_horizontal_momentum) and dx != 0:
                # The mech has momentum left. Check that it wants to move in the right direction.
                if math.copysign(1, dx) == math.copysign(1, self.mech.maximum_horizontal_momentum):
                    # Allow the player to move in the x axis
                    self.fly(dx, 0)
                    self.mech.accumulated_horizontal_momentum += dx
            # Moving along the y-axis
            elif abs(self.mech.accumulated_vertical_momentum) < abs(self.mech.maximum_vertical_momentum) and dy != 0:
                # The mech has momentum left. Check that it wants to move in the right direction.
                if math.copysign(1, dy) == math.copysign(1, self.mech.maximum_vertical_momentum):
                    # Allow the player to move in the y axis
                    self.fly(0, dy)
                    self.mech.accumulated_vertical_momentum += dy
            # Moving after all momentum has been spent
            elif abs(self.mech.impulse) == 1 and not self.mech.has_spent_impulse:
                # Gain momentum in a direction.
                # Check the x-axis.
                if dx != 0 and self.mech.maximum_horizontal_momentum == 0 or math.copysign(1, dx) == math.copysign(1, self.mech.maximum_horizontal_momentum):
                    self.fly(dx, 0)
                    self.mech.accumulated_horizontal_momentum += dx
                    self.mech.has_spent_impulse = True
                # Check the y-axis.
                if dy != 0 and self.mech.maximum_vertical_momentum == 0 or math.copysign(1, dy) == math.copysign(1, self.mech.maximum_vertical_momentum):
                    self.fly(0, dy)
                    self.mech.accumulated_vertical_momentum += dy
                    self.mech.has_spent_impulse = True

    def fly(self, dx, dy):
        """
        Move the entity regardless of everything.
        """
        self.x += dx
        self.y += dy
        self.has_moved = True

    def reset(self):
        """
        Reset the entity for the next turn.
        """
        self.mech.reset()
        self.weapon.reset()
        self.has_moved = False
    
    def distance(self, x, y):
        """
        Calculate the Manhanttan distance from self to coordinate (x, y)
        """
        return abs(self.x - x) + abs(self.y - y)
    
    def fire_weapon(self, game_map, entities):
        """
        Fire the entity's weapon.
        """
        results = []

        if self.weapon is None: 
            return results
        
        for target in self.weapon.targets:
            entity = self.get_entity_at_location(target, entities)
            results.append(self.damage_entity(entity, self.weapon.damage))
        
        return results

    def damage_entity(self, entity, damage):
        results = []
        
        entity.mech.hp -= damage

        results = {'message': '{0} was dealth {1} damage.'.format(entity.name.capitalize(), damage)}

        return results

    def get_entity_at_location(self, location, entities):
        x, y = location

        for entity in entities:
            if x == entity.x and y == entity.y:
                return entity
        
        return None