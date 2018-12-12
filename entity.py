import tcod as libtcod
import math

from components.location import Location
from components.manager import create_component, create_components, AIComponent, ChassisComponent, PropulsionComponent, WeaponComponent
from death_functions import kill_enemy, kill_player
from enum import auto, Enum
from event_queue import EventQueue
from render_functions import RenderOrder

class EntityType(Enum):
    PLAYER = auto()
    NPC = auto()

def entity_manager(entity_type, location, event_queue):
    """
    Build an entity with the specified components.
    """
    entity = None

    if entity_type == EntityType.PLAYER:
        chassis_component = create_component(ChassisComponent.BASIC_CHASSIS)
        mech_component = create_component(PropulsionComponent.BASIC_PROPULSION)
        weapon_component = create_components({WeaponComponent.LASER: 1})
        x, y = location
        location_component = Location(x, y)

        entity = Entity('@', libtcod.white, 'player', chassis=chassis_component, mech=mech_component, weapon=weapon_component, location=location_component)

    elif entity_type == EntityType.NPC:
        ai_component = create_component(AIComponent.DEBUG)
        chassis_component = create_component(ChassisComponent.WEAK_CHASSIS)
        mech_component = create_component(PropulsionComponent.WEAK_PROPULSION)
        x, y = location
        location_component = Location(x, y)

        entity = Entity('@', libtcod.yellow, 'npc', chassis=chassis_component, mech=mech_component, location=location_component, ai=ai_component)

    if entity is not None:
        event_queue.register(entity)

    return entity

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, char, color, name, chassis=None, mech=None, cursor=None, weapon=None, ai=None, location=None):
        self.char = char
        self.color = color
        self.name = name        
        self.chassis = chassis
        self.mech = mech
        self.cursor = cursor
        self.weapon = weapon                # A list of weapons.
        self.ai = ai
        self.location = location
        self.action_points = 0
        self.render_order = RenderOrder.ACTOR

        if self.chassis:    self.chassis.owner = self
        if self.mech:       self.mech.owner = self
        if self.cursor:     self.cursor.owner = self
        if self.ai:         self.ai.owner = self
        if self.location:   self.location.owner = self
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

    def fire_active_weapon(self, entities):
        """
        Fire weapon at target.
        """
        result = []
        
        for w in self.weapon:
            if w.active:
                result.extend(w.fire(entities))
        
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