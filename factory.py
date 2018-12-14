import tcod as libtcod

from components.ai import DoNothing
from components.chassis import Chassis
from components.location import Location
from components.mech import Mech
from components.weapon import Weapon
from entity import Entity
from enum import auto, Enum

class AIComponent(Enum):
    DEBUG = auto()

class ChassisComponent(Enum):
    BASIC_CHASSIS = auto()
    WEAK_CHASSIS = auto()

class PropulsionComponent(Enum):
    BASIC_PROPULSION = auto()
    WEAK_PROPULSION = auto()

class WeaponComponent(Enum):
    LASER = auto()

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

def create_components(component_dict):
    """
    Return a list of components.
    """
    results = []

    for component, quantity in component_dict.items():
        iter = 1
        while (iter <= quantity):
            results.append(create_component(component))
            iter += 1

    if type(component) is not WeaponComponent:
        return results.pop()    # Only multi-weapon entities are supported at the moment.
    else:
        return results

def create_component(component):
    """
    Return the desired component.
    """
    # Weapon components.
    if component == WeaponComponent.LASER:
        return Weapon(name='Laser', damage=5, min_targets=0, max_targets=5, color=libtcod.green, range=10, cost=1)
    
    # Chassis components.
    elif component == ChassisComponent.BASIC_CHASSIS:
        return Chassis(max_hp=30)
    elif component == ChassisComponent.WEAK_CHASSIS:
        return Chassis(max_hp=20)
    
    # Propulsion components.
    elif component == PropulsionComponent.BASIC_PROPULSION:
        return Mech(peak_momentum=6, max_impulse=1)
    elif component == PropulsionComponent.WEAK_PROPULSION:
        return Mech(peak_momentum=4, max_impulse=1)
    
    # AI components.
    elif component == AIComponent.DEBUG:
        return DoNothing()
    
    return None