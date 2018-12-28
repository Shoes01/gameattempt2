import tcod as libtcod
import uuid

from components.ai import DoNothing, MoveAlongPath, Overseer
from components.chassis import Chassis
from components.location import Location
from components.mech import Mech
from components.projectile import Projectile
from components.render import Render
from components.weapon import Weapon
from entity import Entity
from enum import auto, Enum

class AIComponent(Enum):
    DEBUG = auto()
    PROJECTILE = auto()
    OVERSEER_AI = auto()

class ChassisComponent(Enum):
    BASIC_CHASSIS = auto()
    WEAK_CHASSIS = auto()

class PropulsionComponent(Enum):
    BASIC_PROPULSION = auto()
    WEAK_PROPULSION = auto()

class WeaponComponent(Enum):
    LASER = auto()
    GUN = auto()

class EntityType(Enum):
    PLAYER = auto()
    NPC = auto()
    OVERSEER = auto()

class ProjectileType(Enum):
    BASIC_PROJECTILE = auto()
    LASER_PROJECTILE = auto()

def entity_factory(entity_type, location, entities, weapon=None):
    """
    Build an entity with the specified components.
    """
    entity = None

    # Unit entities.
    if entity_type == EntityType.PLAYER:
        chassis_component = create_component(ChassisComponent.BASIC_CHASSIS)
        mech_component = create_component(PropulsionComponent.BASIC_PROPULSION)
        weapon_component = create_components({WeaponComponent.LASER: 1, WeaponComponent.GUN: 1})
        x, y = location
        location_component = Location(x, y)
        render_component = Render('@', libtcod.white)

        entity = Entity('player', uuid.uuid4(), moves_with_player=True, chassis=chassis_component, mech=mech_component, weapon=weapon_component, location=location_component, render=render_component)

    elif entity_type == EntityType.NPC:
        ai_component = create_component(AIComponent.DEBUG)
        chassis_component = create_component(ChassisComponent.WEAK_CHASSIS)
        mech_component = create_component(PropulsionComponent.WEAK_PROPULSION)
        weapon_component = create_components({WeaponComponent.GUN: 1})
        x, y = location
        location_component = Location(x, y)
        render_component = Render('@', libtcod.yellow)

        entity = Entity('npc', uuid.uuid4(), chassis=chassis_component, mech=mech_component, weapon=weapon_component, location=location_component, ai=ai_component, render=render_component)

    elif entity_type == EntityType.OVERSEER:
        ai_component = create_component(AIComponent.OVERSEER_AI)
        mech_component = Mech(peak_momentum=100, max_impulse=100)
        mech_component.impulse = weapon.rate_of_fire
        x, y = location
        location_component = Location(x, y)
        weapon_component = []
        new_weapon = Weapon(weapon.name, weapon.damage, weapon.min_targets, weapon.max_targets, weapon.color, weapon.range, weapon.cost, weapon.rate_of_fire, projectile=weapon.projectile)
        new_weapon.targets = weapon.targets
        weapon_component.append(new_weapon)

        entity = Entity('overseer', uuid.uuid4(), ai=ai_component, mech=mech_component, location=location_component, weapon=weapon_component)

    # Projectile entities.
    elif entity_type == ProjectileType.BASIC_PROJECTILE:
        ai_component = create_component(AIComponent.PROJECTILE)
        mech_component = Mech(peak_momentum=100, max_impulse=100)
        mech_component.impulse = 4 # This essentially sets the speed of the projectile.
        x, y = location
        location_component = Location(x, y)
        projectile_component = Projectile(damage=10, damage_type='direct')
        render_component = Render('o', libtcod.orange)

        entity = Entity('ballistic projectile', uuid.uuid4(), ai=ai_component, mech=mech_component, location=location_component, projectile=projectile_component, render=render_component)

    elif entity_type == ProjectileType.LASER_PROJECTILE:
        ai_component = create_component(AIComponent.PROJECTILE)
        mech_component = Mech(peak_momentum=100, max_impulse=100)
        mech_component.impulse = 3600 # This essentially sets the speed of the projectile.
        x, y = location
        location_component = Location(x, y)
        projectile_component = Projectile(damage=10, damage_type='direct')
        render_component = Render('-', libtcod.dark_green)

        entity = Entity('laser pulse', uuid.uuid4(), ai=ai_component, mech=mech_component, location=location_component, projectile=projectile_component, render=render_component)

    if entity is not None:
        entities.append(entity)

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
        return Weapon(name='pulse laser', damage=5, min_targets=1, max_targets=5, color=libtcod.green, range=10, cost=1, rate_of_fire=3600, projectile=ProjectileType.LASER_PROJECTILE)
    
    elif component == WeaponComponent.GUN:
        return Weapon(name='gattling gun', damage=5, min_targets=1, max_targets=3, color=libtcod.red, range=10, cost=1, rate_of_fire=4, projectile=ProjectileType.BASIC_PROJECTILE)
    
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
    elif component == AIComponent.PROJECTILE:
        return MoveAlongPath()
    elif component == AIComponent.OVERSEER_AI:
        return Overseer()
    
    return None