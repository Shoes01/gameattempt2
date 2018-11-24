import math

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, char, color, name, mech=None, cursor=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.mech = mech
        self.cursor = cursor

        if self.mech:   self.mech.owner = self        
        if self.cursor: self.cursor.owner = self

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
                self.x += dx
                self.y += dy
                self.mech.accumulated_horizontal_momentum += dx
                self.mech.accumulated_vertical_momentum += dy
                self.mech.has_spent_impulse = True
            
            # The non-trivial case: the mech is moving, so there are some directions that are not allowed.
            # Moving along the x-axis
            elif abs(self.mech.accumulated_horizontal_momentum) < abs(self.mech.maximum_horizontal_momentum) and dx != 0:
                # The mech has momentum left. Check that it wants to move in the right direction.
                if math.copysign(1, dx) == math.copysign(1, self.mech.maximum_horizontal_momentum):
                    # Allow the player to move in the x axis
                    self.x += dx
                    self.mech.accumulated_horizontal_momentum += dx
            # Moving along the y-axis
            elif abs(self.mech.accumulated_vertical_momentum) < abs(self.mech.maximum_vertical_momentum) and dy != 0:
                # The mech has momentum left. Check that it wants to move in the right direction.
                if math.copysign(1, dy) == math.copysign(1, self.mech.maximum_vertical_momentum):
                    # Allow the player to move in the y axis
                    self.y += dy
                    self.mech.accumulated_vertical_momentum += dy
            # Moving after all momentum has been spent
            elif self.mech.impulse == 1 and not self.mech.has_spent_impulse:
                # Gain momentum in a direction.
                # Check the x-axis.
                if dx != 0 and self.mech.maximum_horizontal_momentum == 0 or math.copysign(1, dx) == math.copysign(1, self.mech.maximum_horizontal_momentum):
                    self.x += dx
                    self.mech.accumulated_horizontal_momentum += dx
                    self.mech.has_spent_impulse = True
                # Check the y-axis.
                if dy != 0 and self.mech.maximum_vertical_momentum == 0 or math.copysign(1, dy) == math.copysign(1, self.mech.maximum_vertical_momentum):
                    self.y += dy
                    self.mech.accumulated_vertical_momentum += dy
                    self.mech.has_spent_impulse = True

    def fly(self, dx, dy):
        """
        Move the entity regardless of everything.
        """
        self.x += dx
        self.y += dy
