import tcod as libtcod

from game_states import GameStates

def handle_keys(key, game_state):
    if key:
        if game_state == GameStates.ENEMY_TURN:         return handle_enemy_turn_keys(key)
        elif game_state == GameStates.PLAYER_TURN:      return handle_player_turn_keys(key)
        elif game_state == GameStates.TARGETING:        return handle_targeting_keys(key)
        elif game_state == GameStates.SHOW_WEAPONS_MENU:return handle_menu_keys(key)
        elif game_state == GameStates.LOOK:             return handle_look_keys(key)
    return {}

def handle_enemy_turn_keys(key):
    if key.vk == libtcod.KEY_ENTER and key.lalt:        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:                  return {'exit': True}
    
    return {}

def handle_player_turn_keys(key):
    key_char = chr(key.c)
    result = {}

    # Movement keys
    result = generic_move_keys(key)

    if key.vk == libtcod.KEY_ENTER:                     result = {'next_turn_phase': True}
    
    # Change impulse
    if key.vk == libtcod.KEY_PAGEUP:                    result = {'delta_speed':  1}
    elif key.vk == libtcod.KEY_PAGEDOWN:                result = {'delta_speed': -1}
    elif key.vk == libtcod.KEY_HOME:                    result = {'delta_speed':  999}

    # Other keys
    if key_char == 'f':                                 result = {'show_weapons_menu': True}
    if key_char == 'r':                                 result = {'reset_targets': True}
    if key_char == 'x':                                 result = {'look': True}

    if key.vk == libtcod.KEY_ENTER and key.lalt:        result = {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:                  result = {'exit': True}
    
    return result

def handle_targeting_keys(key):
    key_char = chr(key.c)
    result = {}

    # Movement keys
    result = generic_move_keys(key)

    # Other keys
    if key_char == 'f':                                 result = {'exit': True}

    if key.vk == libtcod.KEY_ENTER:                     result = {'select': True}
    elif key.vk == libtcod.KEY_ESCAPE:                  result = {'exit': True}
    
    return result

def handle_menu_keys(key):
    result = {}

    index = key.c - ord('a')

    if index >= 0:                                      result = {'weapons_menu_index': index}

    if key.vk == libtcod.KEY_ENTER and key.lalt:        result = {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:                  result = {'exit': True}

    return result

def handle_look_keys(key):
    result = {}

    # Movement keys
    result = generic_move_keys(key)

    if key.vk == libtcod.KEY_ENTER and key.lalt:        result = {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:                  result = {'exit': True}

    return result

def generic_move_keys(key):
    key_char = chr(key.c)

    if key.vk == libtcod.KEY_UP or key_char == 'w':         return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or key_char == 's':     return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or key_char == 'a':     return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or key_char == 'd':    return {'move': (1, 0)}
    
    return {}

def handle_mouse(mouse):
    (x, y) = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:                           return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:                         return {'right_click': (x, y)}

    return {}