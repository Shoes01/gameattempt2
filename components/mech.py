import math

class Mech:
    def __init__(self, hp, peak_momentum):
        self.hp = hp
        self.peak_momentum = peak_momentum      # The absolute highest momentum the mech can have
        self.maximum_horizontal_momentum = 0    # Positive: right
        self.maximum_vertical_momentum = 0      # Positive: down
        self.impulse = 0                        # Three options, -1 (deccelaration), 0 (no change), +1 (acceleration)
        self.remaining_impulse = 0              # Used to track the "bonus" momentum
        self.accumulated_horizontal_momentum = 0# When this number reaches maximum momentum, the player can no longer move in that direction, unless it has impulse.
        self.accumulated_vertical_momentum = 0  # When this number reaches maximum momentum, the player can no longer move in that direction, unless it has impulse.
        
    def calculate_maximum_momentum(self):
        # Calculate the maximum momentum the mech can use this turn.
        return self.impulse + abs(self.maximum_horizontal_momentum) + abs(self.maximum_vertical_momentum)
    
    def calculate_accumulated_momentum(self):
        # Calculate the momentum the mech has accumulated this turn.
        # It does not include the impulse.
        return abs(self.accumulated_horizontal_momentum) + abs(self.accumulated_vertical_momentum)
    
    def has_spent_minimum_momentum(self):
        # Check to see that the mech has moved the minimum tiles required by their momentum.
        if self.calculate_accumulated_momentum() >= self.calculate_maximum_momentum() - 2:
            return True
        return False
    
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