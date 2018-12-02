import tcod as libtcod

from game_states import GameStates

def handle_keys(key, game_state):
    if key:
        if game_state == GameStates.ENEMY_TURN:         return handle_enemy_turn_keys(key)
        elif game_state == GameStates.PLAYER_TURN:      return handle_player_turn_keys(key)
        elif game_state == GameStates.TARGETING:        return handle_targeting_keys(key)
        
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

    if key.vk == libtcod.KEY_ENTER:                     result = {'next turn phase': True}
    
    # Change impulse
    if key.vk == libtcod.KEY_PAGEUP:                    result = {'impulse':  1}
    elif key.vk == libtcod.KEY_PAGEDOWN:                result = {'impulse': -1}
    elif key.vk == libtcod.KEY_HOME:                    result = {'impulse':  0}

    # Other keys
    if key_char == 'f':                                 result = {'change game state': GameStates.TARGETING}
    if key_char == 'r':                                 result = {'reset_targets': True}

    if key.vk == libtcod.KEY_ENTER and key.lalt:        result = {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:                  result = {'exit': True}
    
    return result

def handle_targeting_keys(key):
    result = {}

    # Movement keys
    result = generic_move_keys(key)

    if key.vk == libtcod.KEY_ENTER:                     result = {'select': True}
    elif key.vk == libtcod.KEY_ESCAPE:                  result = {'exit': True}
    
    return result

def generic_move_keys(key):
    if key.vk == libtcod.KEY_UP:                        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN:                    return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT:                    return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT:                   return {'move': (1, 0)}
    
    return {}
