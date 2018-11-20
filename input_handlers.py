from game_states import GameStates, TurnStates

def handle_keys(user_input, game_state, turn_state):
    if user_input:
        if game_state == GameStates.ENEMY_TURN:                 return handle_enemy_turn_keys(user_input)
        elif game_state == GameStates.PLAYER_TURN:
            if turn_state == TurnStates.PRE_MOVEMENT_PHASE:     return handle_player_pre_movement_keys(user_input)
            elif turn_state == TurnStates.MOVEMENT_PHASE:       return handle_player_movement_keys(user_input)
            elif turn_state == TurnStates.POST_MOVEMENT_PHASE:  return handle_player_post_movement_keys(user_input)
            elif turn_state == TurnStates.PRE_ATTACK_PHASE:     return handle_player_pre_attack_keys(user_input)
            elif turn_state == TurnStates.ATTACK_PHASE:         return handle_player_attack_keys(user_input)
            elif turn_state == TurnStates.POST_MOVEMENT_PHASE:  return handle_player_post_attack_keys(user_input)

    return {}

def handle_enemy_turn_keys(user_input):
    if user_input.key == 'ENTER' and user_input.alt:    return {'fullscreen': True}
    elif user_input.key == 'ESCAPE':                    return {'exit': True}
    
    return {}

def handle_player_pre_movement_keys(user_input):
    if user_input.key == 'ENTER' and user_input.alt:    return {'fullscreen': True}
    elif user_input.key == 'ESCAPE':                    return {'exit': True}
    
    return {}

def handle_player_movement_keys(user_input):
    if user_input.key == 'ENTER':                       return {'next_turn_phase': True}
    
    # Movement keys
    if user_input.key == 'UP':                          return {'move': (0, -1)}
    elif user_input.key == 'DOWN':                      return {'move': (0, 1)}
    elif user_input.key == 'LEFT':                      return {'move': (-1, 0)}
    elif user_input.key == 'RIGHT':                     return {'move': (1, 0)}

    if user_input.key == 'ENTER' and user_input.alt:    return {'fullscreen': True}
    elif user_input.key == 'ESCAPE':                    return {'exit': True}

    return {}

def handle_player_post_movement_keys(user_input):
    if user_input.key == 'ENTER' and user_input.alt:    return {'fullscreen': True}
    elif user_input.key == 'ESCAPE':                    return {'exit': True}
    
    return {}

def handle_player_pre_attack_keys(user_input):
    if user_input.key == 'ENTER' and user_input.alt:    return {'fullscreen': True}
    elif user_input.key == 'ESCAPE':                    return {'exit': True}
    
    return {}

def handle_player_attack_keys(user_input):
    if user_input.key == 'ENTER' and user_input.alt:    return {'fullscreen': True}
    elif user_input.key == 'ESCAPE':                    return {'exit': True}
    
    return {}

def handle_player_post_attack_keys(user_input):
    if user_input.key == 'ENTER' and user_input.alt:    return {'fullscreen': True}
    elif user_input.key == 'ESCAPE':                    return {'exit': True}
    
    return {}