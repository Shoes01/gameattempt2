class Mech:
    def __init__(self, hp, max_momentum):
        self.hp = hp
        self.max_momentum = max_momentum
        self.horizontal_momentum = 0        # Positive: right
        self.vertical_momentum = 0          # Positive: down