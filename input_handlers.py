from game_states import GameStates

def handle_keys(user_input, game_state):
    if user_input:
        if game_state == GameStates.ENEMY_TURN:         return handle_enemy_turn_keys(user_input)
        elif game_state == GameStates.PLAYER_TURN:      return handle_player_turn_keys(user_input)
        elif game_state == GameStates.TARGETING:        return handle_targeting_keys(user_input)
        
    return {}

def handle_enemy_turn_keys(user_input):
    if user_input.key == 'ENTER' and user_input.alt:    return {'fullscreen': True}
    elif user_input.key == 'ESCAPE':                    return {'exit': True}
    
    return {}

def handle_player_turn_keys(user_input):
    key_char = user_input.char
    result = {}

    # Movement keys
    result = generic_move_keys(user_input)

    if user_input.key == 'ENTER':                       result = {'next turn phase': True}
    
    # Change impulse
    if user_input.key == 'PAGEUP':                      result = {'impulse':  1}
    elif user_input.key == 'PAGEDOWN':                  result = {'impulse': -1}
    elif user_input.key == 'HOME':                      result = {'impulse':  0}

    # Other keys
    if key_char == 'f':                                 result = {'change game state': GameStates.TARGETING}

    if user_input.key == 'ENTER' and user_input.alt:    result = {'fullscreen': True}
    elif user_input.key == 'ESCAPE':                    result = {'exit': True}
    
    return result

def handle_targeting_keys(user_input):
    result = {}

    # Movement keys
    result = generic_move_keys(user_input)

    if user_input.key == 'ENTER':                       result = {'select': True}
    elif user_input.key == 'ESCAPE':                    result = {'exit': True}
    
    return result

def generic_move_keys(user_input):
    if user_input.key == 'UP':                          return {'move': (0, -1)}
    elif user_input.key == 'DOWN':                      return {'move': (0, 1)}
    elif user_input.key == 'LEFT':                      return {'move': (-1, 0)}
    elif user_input.key == 'RIGHT':                     return {'move': (1, 0)}
    
    return {}
