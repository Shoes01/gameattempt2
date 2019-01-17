class Projectile:
    """
    The Projectile class stores the information necessary to damage other entities.
    """
    def __init__(self, damage, damage_type):
        self.damage = damage
        self.damage_type = damage_type      # Direct and indirect.
        self.path = []                      # List of targets. TODO: What do I mean by targets...? Did I mean tiles?