class Chassis:
    """
    The Chassis class holds the structural information of the Entity.
    """
    def __init__(self, max_hp):
        self.max_hp = max_hp    # Maximum HP.
        self.hp = max_hp        # Current HP.
    
    def take_damage(self, damage):
        """
        The entity has been hit by weapon fire. Take damage.
        """
        result = []

        self.hp -= damage

        if self.hp > 0:
            result = {'message': '{0} was dealt {1} damage.'.format(self.owner.name.capitalize(), damage)}
        else:
            result = {'dead': self.owner}

        return result