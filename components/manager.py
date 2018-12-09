import tcod as libtcod

from components.weapon import Weapon
from enum import auto, Enum

class WeaponComponent(Enum):
    LASER = auto()

class ChassisComponent(Enum):
    BASIC_MECH = auto()

class PropulsionComponent(Enum):
    BASIC_ENGINE = auto()

def create_components(component_dict):
    """
    Return a list of components.
    """
    results = []

    for quantity, component in component_dict.items():
        iter = 1
        while (iter <= quantity):
            results.append(create_component(component))
            iter += 1

    return results

def create_component(component):
    if component == WeaponComponent.LASER:
        return Weapon('Laser', 5, 5, 5, libtcod.green, 10)
    
    return None