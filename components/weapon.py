class Weapon:
    def __init__(self, name, damage, min_targets, max_targets, color):
        self.name = name
        self.damage = damage
        self.min_targets = min_targets
        self.max_targets = max_targets
        self.color = color
        self.targets = []
        
    def reset(self):
        self.targets = []