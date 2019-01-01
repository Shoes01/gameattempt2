import tcod as libtcod
import math

from death_functions import kill_enemy, kill_player
from game_states import GameStates
from global_variables import TICKS_PER_TURN
from render_functions import RenderOrder

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, name, uuid, required_game_state=GameStates.ENEMY_TURN, chassis=None, mech=None, cursor=None, arsenal=None, ai=None, location=None, projectile=None, render=None, propulsion=None):
        self.name = name
        self.uuid = uuid
        self.required_game_state = required_game_state
        self.chassis = chassis
        self.mech = mech
        self.cursor = cursor
        self.arsenal = arsenal                # A list of weapons.
        self.ai = ai
        self.location = location
        self.projectile = projectile
        self.render = render
        self.propulsion = propulsion
        self.action_points = TICKS_PER_TURN
        self.render_order = RenderOrder.ACTOR

        if self.chassis:    self.chassis.owner = self
        if self.mech:       self.mech.owner = self
        if self.cursor:     self.cursor.owner = self
        if self.arsenal:    
            self.arsenal.owner = self
            for w in self.arsenal.weapons:
                w.owner = self
        if self.ai:         self.ai.owner = self
        if self.location:   self.location.owner = self
        if self.projectile: self.projectile.owner = self
        if self.render:     self.render.owner = self
        if self.propulsion: self.propulsion.owner = self

    def reset(self, only_action_points=False):
        """
        Reset the entity for the next turn.
        """
        self.action_points = TICKS_PER_TURN
        
        if only_action_points:
            return
        
        if self.mech:       self.mech.reset()
        if self.propulsion: self.propulsion.reset()
        if self.arsenal:    self.arsenal.reset()
    
    def distance(self, x, y):
        """
        Calculate the Manhanttan distance from self to coordinate (x, y).
        """
        return abs(self.location.x - x) + abs(self.location.y - y)