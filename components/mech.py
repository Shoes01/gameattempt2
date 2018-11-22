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
        self.bonus_h_mom = 0
        self.bonus_v_mom = 0
        
    def calculate_maximum_momentum(self):
        # Calculate the maximum momentum the mech can use this turn.
        return self.impulse + abs(self.maximum_horizontal_momentum) + abs(self.maximum_vertical_momentum)
    
    def calculate_accumulated_momentum(self):
        # Calculate the momentum the mech has accumulated this turn.
        # It does not include the impulse.
        return abs(self.accumulated_horizontal_momentum) + abs(self.accumulated_vertical_momentum)
    
    def reset(self):
        self.accumulated_horizontal_momentum = 0
        self.accumulated_vertical_momentum = 0
        self.maximum_horizontal_momentum += self.bonus_h_mom
        self.bonus_h_mom = 0
        self.maximum_vertical_momentum += self.bonus_v_mom
        self.bonus_v_mom = 0