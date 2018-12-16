import tcod as libtcod
import math

from death_functions import kill_enemy, kill_player
from global_variables import TICKS_PER_TURN
from render_functions import RenderOrder

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, char, color, name, moves_with_player=False, chassis=None, mech=None, cursor=None, weapon=None, ai=None, location=None, projectile=None):
        self.char = char
        self.color = color
        self.name = name        
        self.moves_with_player = moves_with_player
        self.chassis = chassis
        self.mech = mech
        self.cursor = cursor
        self.weapon = weapon                # A list of weapons.
        self.ai = ai
        self.location = location
        self.projectile = projectile
        self.action_points = TICKS_PER_TURN
        self.render_order = RenderOrder.ACTOR

        if self.chassis:    self.chassis.owner = self
        if self.mech:       self.mech.owner = self
        if self.cursor:     self.cursor.owner = self
        if self.ai:         self.ai.owner = self
        if self.location:   self.location.owner = self
        if self.projectile: self.projectile.owner = self
        if self.weapon:
            for w in self.weapon:
                w.owner = self

    def reset(self):
        """
        Reset the entity for the next turn.
        """
        self.mech.reset()
        for w in self.weapon:
            w.reset()        
    
    def distance(self, x, y):
        """
        Calculate the Manhanttan distance from self to coordinate (x, y).
        """
        return abs(self.location.x - x) + abs(self.location.y - y)
    
    def activate_weapon(self, chosen_weapon):
        """
        Activate a weapon for targeting.
        """
        result = []

        for w in self.weapon:
            if w == chosen_weapon:
                result.append(w.activate())

        return result

    def fire_active_weapon(self, entities, event_queue):
        """
        Fire weapon at target.
        """
        result = []
        
        for w in self.weapon:
            if w.active:
                result.extend(w.fire(entities, event_queue))
        
        return result
    
    def get_active_weapon(self):
        """
        Get the weapon that is active from the list of weapons.
        """
        for w in self.weapon:
            if w.active:
                return w
        else:
            return None