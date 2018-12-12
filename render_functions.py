import math
import tcod as libtcod

from enum import auto, Enum
from game_states import GameStates
from map_objects.game_map import GameMap
from menus import weapon_menu
from ui_functions import draw_card

class RenderOrder(Enum):
    CORPSE = auto()
    ACTOR = auto()
    CURSOR = auto()

def get_names_under_mouse(mouse, entities, fov_map, cursor):
    # Check to see if the cursor is active. If yes, then giev the names that are under it.
    (x, y) = (mouse.cx, mouse.cy)

    if cursor.location is not None:
        (x, y) = (cursor.location.x, cursor.location.y)

    names = []

    for entity in entities:
        if entity != cursor and entity.location.x == x and entity.location.y == y and libtcod.map_is_in_fov(fov_map, entity.location.x, entity.location.y):
            names.append(entity.name)

    names = ', '.join(names)

    return names.capitalize()

def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color, string_color):
    # Render a bar (HP, experience, etc). first calculate the width of the bar
    bar_width = int(float(value) / maximum * total_width)

    # Render the background first
    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(panel, back_color)
    # Now render the bar on top
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    # Finally, some centered text with the values
    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                             '{0}: {1}/{2}'.format(name, value, maximum))

def render_all(
    con, panel, entities, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height, bar_width, panel_height, panel_y, mouse, colors, 
    status, status_height, status_width, status_x, game_state, turn_state, player, cursor):
    """
    Print con console.
    Displays the tiles and entities.
    """
    if fov_recompute:
        # Draw all the tiles in the game map
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight
                explored = game_map.tiles[x][y].explored
                highlighted = game_map.tiles[x][y].highlighted
                targeted = game_map.tiles[x][y].targeted

                if visible:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_wall'), libtcod.BKGND_SET)
                    else:                        
                        libtcod.console_set_char_background(con, x, y, colors.get('light_ground'), libtcod.BKGND_SET)

                    game_map.tiles[x][y].explored = True
                elif explored:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)
                
                if highlighted:
                    libtcod.console_set_char_background(con, x, y, colors.get('highlight'), libtcod.BKGND_SET)

                if targeted:
                    libtcod.console_set_char_background(con, x, y, libtcod.light_red, libtcod.BKGND_SET)

    # Draw all entities in the list
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)
    
    for entity in entities_in_render_order:
        if entity.location is not None:
            draw_entity(con, entity, fov_map, game_map)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    """
    Print panel console.
    Displays HP bar and message log.
    """
    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    # Print the game messages, one line at a time
    y = 1
    for message in message_log.messages:
        libtcod.console_set_default_foreground(panel, message.color)
        libtcod.console_print_ex(panel, message_log.x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
        y += 1

    # Print what is under the mouse.
    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT,
                             get_names_under_mouse(mouse, entities, fov_map, cursor))

    # Print the HP bar.
    render_bar(panel, 1, 1, bar_width, 'HP', player.chassis.hp, player.chassis.max_hp,
               libtcod.light_red, libtcod.darker_red, libtcod.white)

    libtcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)

    """
    Print status card.
    Displays game state and turn state, momentum state and more.
    Displays weapons stats.
    """
    libtcod.console_set_default_background(status, libtcod.black)
    libtcod.console_clear(status)

    draw_card(status, 0, 0, status_width, status_height, libtcod.white, 
        turn=game_state.name, phase=turn_state.name, impulse=player.mech.impulse,
        momentum=player.mech.calculate_maximum_momentum(), h_mom=player.mech.maximum_horizontal_momentum, v_mom=player.mech.maximum_vertical_momentum)

    if player.weapon is not None and len(player.weapon) > 0:
        iterator = 1
        for weapon in player.weapon:    
            draw_card(status, 0, iterator*10, status_width, status_height, weapon.color, 
                weapon=weapon.name, dmg=weapon.damage, range=weapon.range, cur_targets=len(weapon.targets), max_targets=weapon.max_targets)
            iterator += 1

    libtcod.console_blit(status, 0, 0, status_width, status_height, 0, status_x, 0)

    """
    Print menus.
    """
    if game_state == GameStates.SHOW_WEAPONS_MENU:
        weapon_menu(con, 'Choose your weapon to fire.', player.weapon, 50, screen_height, screen_width)

def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity, fov_map, game_map):
    if libtcod.map_is_in_fov(fov_map, entity.location.x, entity.location.y):
            libtcod.console_set_default_foreground(con, entity.color)
            libtcod.console_put_char(con, entity.location.x, entity.location.y, entity.char, libtcod.BKGND_NONE)

def clear_entity(con, entity):
    # erase the character that represents this object
    if entity.location is not None:
        libtcod.console_put_char(con, entity.location.x, entity.location.y, ' ', libtcod.BKGND_NONE)

def highlight_legal_moves(player, game_map):
    game_map.reset_flags()
    
    h_mom = player.mech.maximum_horizontal_momentum
    v_mom = player.mech.maximum_vertical_momentum
    mech_momentum = player.mech.calculate_maximum_momentum()
    mech_impulse = player.mech.impulse

    minimum = 0 - abs(mech_momentum)
    maximum = 0 + abs(mech_momentum) + 1

    for x in range(minimum, maximum):
        for y in range(minimum, maximum):
            if (abs(x) + abs(y) >= mech_momentum and             # Ensure the tile exceeds the minimum.
                abs(x) <= abs(h_mom) + abs(mech_impulse) and     # Ensure the x value is below the horizontal momentum.
                abs(y) <= abs(v_mom) + abs(mech_impulse) and     # Ensure the y value is below the vertical momentum.
                abs(x) + abs(y) <= mech_momentum):               # Ensure that the x and y values are below the mech momentum. (This is to avoid the +1 being counted each way)
                # Now check to see that the direction matches the momentum.
                if h_mom == 0:                                                                      # x can be anything.
                    if v_mom == 0:                                                                      # y can be anything (this is the trivial case).
                        game_map.set_highlighted(player.location.x + x, player.location.y + y)
                    elif v_mom != 0 and ( y == 0 or math.copysign(1, y) == math.copysign(1, v_mom) ):   # y must be 0 or have the same sign as v_mom.
                        game_map.set_highlighted(player.location.x + x, player.location.y + y)
                elif h_mom != 0 and ( x == 0 or math.copysign(1, x) == math.copysign(1, h_mom) ):   # x must be 0 or have the same sign as h_mom.
                    if v_mom == 0:                                                                      # y can be anything.
                        game_map.set_highlighted(player.location.x + x, player.location.y + y)
                    elif v_mom != 0 and ( y == 0 or math.copysign(1, y) == math.copysign(1, v_mom) ):   # y must be 0 or have the same sign as v_mom.
                        game_map.set_highlighted(player.location.x + x, player.location.y + y)

def erase_cell(con, x, y):
    """
    Some temporary cell fg and bg should stick around until the end of a phase.
    Those need to be manually erased.
    """
    libtcod.console_put_char(con, x, y, ' ', libtcod.BKGND_NONE)