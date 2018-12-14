class Projectile:
    """
    The Projectile class stores the information necessary to damage other entities.
    """
    def __init__(self, damage, damage_type):
        self.damage = damage
        self.damage_type = damage_type
        self.path = []                      # List of targets.
    
