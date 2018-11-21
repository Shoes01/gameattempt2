from game_states import GameStates, TurnStates

def handle_keys(user_input, game_state, turn_state):
    if user_input:
        if game_state == GameStates.ENEMY_TURN:                 return handle_enemy_turn_keys(user_input)
        elif game_state == GameStates.PLAYER_TURN:              return handle_player_turn_keys(user_input)
        
    return {}

def handle_enemy_turn_keys(user_input):
    if user_input.key == 'ENTER' and user_input.alt:    return {'fullscreen': True}
    elif user_input.key == 'ESCAPE':                    return {'exit': True}
    
    return {}

def handle_player_turn_keys(user_input):
    if user_input.key == 'ENTER':                       return {'next_turn_phase': True}
    
    # Change impulse
    if user_input.key == 'PAGEUP':                      return {'increase impulse': True}
    elif user_input.key == 'PAGEDOWN':                  return {'decrease impulse': True}
    elif user_input.key == 'HOME':                      return {'maintain impulse': True}

    # Movement keys
    if user_input.key == 'UP':                          return {'move': (0, -1)}
    elif user_input.key == 'DOWN':                      return {'move': (0, 1)}
    elif user_input.key == 'LEFT':                      return {'move': (-1, 0)}
    elif user_input.key == 'RIGHT':                     return {'move': (1, 0)}

    if user_input.key == 'ENTER' and user_input.alt:    return {'fullscreen': True}
    elif user_input.key == 'ESCAPE':                    return {'exit': True}
    
    return {}