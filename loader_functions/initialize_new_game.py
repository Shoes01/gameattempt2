import tcod as libtcod

from components.ai import DoNothing
from components.chassis import Chassis
from components.cursor import Cursor
from components.location import Location
from components.manager import create_components, ChassisComponent, PropulsionComponent, WeaponComponent
from components.mech import Mech
from entity import Entity
from event_queue import EventQueue
from game_messages import MessageLog
from game_states import GameStates, TurnStates
from map_objects.game_map import GameMap
from render_functions import RenderOrder

def get_constants():
    screen_width = 80
    screen_height = 50

    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height

    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    status_width = 15
    status_height = screen_height - panel_height
    status_x = screen_width - status_width

    map_width = 80
    map_height = screen_height - panel_height

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    colors = {
        'dark_wall': (0, 0, 100),
        'dark_ground': (50, 50, 150),
        'light_wall': (130, 110, 50),
        'light_ground': (200, 180, 50),
        'highlight': (199, 234, 70)
    }

    constants = {
        'screen_width': screen_width,
        'screen_height': screen_height,
        'bar_width': bar_width,
        'panel_height': panel_height,
        'panel_y': panel_y,
        'message_x': message_x,
        'message_width': message_width,
        'message_height': message_height,
        'status_width': status_width,
        'status_height': status_height,
        'status_x': status_x,
        'map_width': map_width,
        'map_height': map_height,
        'fov_algorithm': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,
        'colors': colors
    }

    return constants

def get_game_variables(constants):
    # Create player.
    chassis_component = create_components({ChassisComponent.BASIC_CHASSIS: 1})
    mech_component = create_components({PropulsionComponent.BASIC_PROPULSION: 1})
    weapon_component = create_components({WeaponComponent.LASER: 2})
    location_component = Location(x=int(constants['screen_width'] / 2), y=int(constants['screen_height'] / 2))
    player = Entity('@', libtcod.white, "player", 
                    render_order=RenderOrder.ACTOR, chassis=chassis_component, mech=mech_component, weapon=weapon_component, location=location_component)
    
    # Create NPC.
    ai_component = DoNothing()
    chassis_component = create_components({ChassisComponent.WEAK_CHASSIS: 1})
    mech_component = create_components({PropulsionComponent.WEAK_PROPULSION: 1})
    location_component = Location(x=int(constants['screen_width'] / 2) - 5, y=int(constants['screen_height'] / 2))
    npc = Entity('@', libtcod.yellow, "NPC", 
                    render_order=RenderOrder.ACTOR, chassis=chassis_component, mech=mech_component, ai=ai_component, location=location_component)
    
    # Create cursor.
    cursor_component = Cursor()
    location_component = Location()
    cursor = Entity('X', libtcod.red, "cursor", render_order=RenderOrder.CURSOR, cursor=cursor_component, location=location_component)
    
    # Create entities list.
    entities = [player, cursor, npc]

    # Create game_map.
    game_map = GameMap(constants['map_width'], constants['map_height'])

    # Create message_log.
    message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

    # Set game_state.
    game_state = GameStates.PLAYER_TURN
    
    # Set turn_state.
    turn_state = TurnStates.UPKEEP_PHASE

    # Open the event queue, and load it up.
    event_queue = EventQueue()
    for entity in entities:
        if entity is not cursor:
            event_queue.register(entity)

    return player, cursor, entities, game_map, message_log, game_state, turn_state, event_queue