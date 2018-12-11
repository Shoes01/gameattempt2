import tcod as libtcod

from components.chassis import Chassis
from components.mech import Mech
from components.weapon import Weapon
from enum import auto, Enum

class WeaponComponent(Enum):
    LASER = auto()

class ChassisComponent(Enum):
    BASIC_CHASSIS = auto()
    WEAK_CHASSIS = auto()

class PropulsionComponent(Enum):
    BASIC_PROPULSION = auto()
    WEAK_PROPULSION = auto()

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
    
    return None