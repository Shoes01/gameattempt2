class Arsenal:
    """
    This class serves as a "weapons inventory".
    """
    def __init__(self):
        self.weapons = []
    
    def add_weapon(self, weapon):
        weapon.owner = self.owner
        self.weapons.append(weapon)
    
    def remove_weapon(self, weapon):
        self.weapons.remove(weapon)

    def activate_weapon(self, weapon):
        """
        Activate a weapon for targeting.
        """
        results = []
        
        for w in self.weapons:
            if w == weapon:
                results.extend(w.activate())
                
        return results

    def get_active_weapon(self):
        """
        Get the weapon that is active from the list of weapons.
        """
        for w in self.weapons:
            if w.active:
                return w
        else:
            return None

    def fire_active_weapon(self):
        """
        Fire weapon at target.
        """
        results = []
        
        for w in self.weapons:
            if w.active:
                results.extend(w.fire())
        else:
            self.owner.action_points = 0
        
        return results
    
    def reset(self):
        for w in self.weapons:
            w.reset()