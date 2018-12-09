import math

class Mech:
    """
    The Mech class stores the HP and the Momentum properties.
    """
    def __init__(self, peak_momentum, max_impulse=1):
        self.peak_momentum = peak_momentum      # The absolute highest momentum the mech can have
        self.maximum_horizontal_momentum = 0    # Positive: right
        self.maximum_vertical_momentum = 0      # Positive: down
        self.impulse = 0                        # Three options, -1 (deccelaration), 0 (no change), +1 (acceleration)
        self.max_impulse = abs(max_impulse)     # How high the impulse can go.
        self.has_spent_impulse = False          # When impulse is used to propel the mech further and gain momentum, this is set to True.
        self.accumulated_horizontal_momentum = 0# When this number reaches maximum momentum, the player can no longer move in that direction, unless it has impulse.
        self.accumulated_vertical_momentum = 0  # When this number reaches maximum momentum, the player can no longer move in that direction, unless it has impulse.
        
    def calculate_maximum_momentum(self):
        # Calculate the maximum momentum the mech can use this turn.
        mech_momentum = self.impulse + abs(self.maximum_horizontal_momentum) + abs(self.maximum_vertical_momentum)

        if self.peak_momentum <= mech_momentum:
            return self.peak_momentum
        return mech_momentum
    
    def calculate_accumulated_momentum(self):
        # Calculate the momentum the mech has accumulated this turn.
        # It does not include the impulse.
        return abs(self.accumulated_horizontal_momentum) + abs(self.accumulated_vertical_momentum)
    
    def has_spent_minimum_momentum(self):
        # Check to see that the mech has moved the minimum tiles required by their momentum.
        if self.calculate_accumulated_momentum() >= self.calculate_maximum_momentum() - 2:
            return True
        return False
    
    def change_impulse(self, delta):
        self.impulse += delta
        if abs(self.impulse) > abs(self.max_impulse):
            self.impulse = int(math.copysign(self.max_impulse, delta))

    def reset(self):
        # Reduce maximum horizontal momentum if the mech did not reach max. Increase if it exceeded it.
        if abs(self.accumulated_horizontal_momentum) < abs(self.maximum_horizontal_momentum):
            self.maximum_horizontal_momentum = self.accumulated_horizontal_momentum
        elif abs(self.accumulated_horizontal_momentum) > abs(self.maximum_horizontal_momentum):
            self.maximum_horizontal_momentum += int(math.copysign(1, self.accumulated_horizontal_momentum))

        # Reduce maximum vertical momentum if the mech did not reach max. Increase if it exceeded it.
        if abs(self.accumulated_vertical_momentum) < abs(self.maximum_vertical_momentum):
            self.maximum_vertical_momentum = self.accumulated_vertical_momentum
        elif abs(self.accumulated_vertical_momentum) > abs(self.maximum_vertical_momentum):
            self.maximum_vertical_momentum += int(math.copysign(1, self.accumulated_vertical_momentum))

        # Reset values.
        self.accumulated_horizontal_momentum = 0
        self.accumulated_vertical_momentum = 0
        self.has_spent_impulse = False
    
    def move(self, dx, dy):
        """
        Move the entity according to the rules of momentum.
        Cares about obstacles.
        """
        if self.calculate_accumulated_momentum() < self.calculate_maximum_momentum():
            # Allow the player to move.

            # The trivial case: the mech is at rest.
            if self.maximum_horizontal_momentum == 0 and self.maximum_vertical_momentum == 0 and self.impulse == 1:
                # Allow the player to move in any direction.
                self.owner.move(dx, dy)
                self.accumulated_horizontal_momentum += dx
                self.accumulated_vertical_momentum += dy
                self.has_spent_impulse = True
            
            # The non-trivial case: the mech is moving, so there are some directions that are not allowed.
            # Moving along the x-axis
            elif abs(self.accumulated_horizontal_momentum) < abs(self.maximum_horizontal_momentum) and dx != 0:
                # The mech has momentum left. Check that it wants to move in the right direction.
                if math.copysign(1, dx) == math.copysign(1, self.maximum_horizontal_momentum):
                    # Allow the player to move in the x axis
                    self.owner.move(dx, 0)
                    self.accumulated_horizontal_momentum += dx
            # Moving along the y-axis
            elif abs(self.accumulated_vertical_momentum) < abs(self.maximum_vertical_momentum) and dy != 0:
                # The mech has momentum left. Check that it wants to move in the right direction.
                if math.copysign(1, dy) == math.copysign(1, self.maximum_vertical_momentum):
                    # Allow the player to move in the y axis
                    self.owner.move(0, dy)
                    self.accumulated_vertical_momentum += dy
            # Moving after all momentum has been spent
            elif abs(self.impulse) == 1 and not self.has_spent_impulse:
                # Gain momentum in a direction.
                # Check the x-axis.
                if dx != 0 and self.maximum_horizontal_momentum == 0 or math.copysign(1, dx) == math.copysign(1, self.maximum_horizontal_momentum):
                    self.owner.move(dx, 0)
                    self.accumulated_horizontal_momentum += dx
                    self.has_spent_impulse = True
                # Check the y-axis.
                if dy != 0 and self.maximum_vertical_momentum == 0 or math.copysign(1, dy) == math.copysign(1, self.maximum_vertical_momentum):
                    self.owner.move(0, dy)
                    self.accumulated_vertical_momentum += dy
                    self.has_spent_impulse = True