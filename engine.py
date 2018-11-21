import tdl

from components.mech import Mech
from entity import Entity
from game_messages import MessageLog, Message
from game_states import GameStates, TurnStates
from input_handlers import handle_keys
from map_utils import GameMap, make_map, reset_highlight
from render_functions import clear_all, highlight_legal_moves, render_all

def main():
    screen_width = 80
    screen_height = 50

    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height

    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    map_width = 80
    map_height = 43

    fov_algorithm = 'BASIC'
    fov_light_walls = True
    fov_radius = 10

    colors = {
        'dark_wall': (0, 0, 100),
        'dark_ground': (50, 50, 150),
        'light_wall': (130, 110, 50),
        'light_ground': (200, 180, 50),
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'red': (255, 0, 0),
        'orange': (255, 127, 0),
        'light_red': (255, 114, 114),
        'darker_red': (127, 0, 0),
        'highlight': (199, 234, 70)
    }

    mech_component = Mech(hp=30, peak_momentum=6)
    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', (255, 255, 255), "player", mech=mech_component)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', (255, 255, 0), "NPC")
    entities = [npc, player]

    tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)

    root_console = tdl.init(screen_width, screen_height, title='MVP v0.0')
    con = tdl.Console(screen_width, screen_height)
    panel = tdl.Console(screen_width, panel_height)

    game_map = GameMap(map_width, map_height)
    make_map(game_map)

    message_log = MessageLog(message_x, message_width, message_height)

    mouse_coordinates = (0, 0)

    game_state = GameStates.PLAYER_TURN
    turn_state = TurnStates.UPKEEP_PHASE

    fov_recompute = True
    
    while not tdl.event.is_window_closed():
        if fov_recompute:
            game_map.compute_fov(player.x, player.y, fov=fov_algorithm, radius=fov_radius, light_walls=fov_light_walls)

        render_all(con, panel, entities, game_map, fov_recompute, root_console, message_log, screen_width, screen_height, bar_width, panel_height, panel_y, mouse_coordinates, colors)

        tdl.flush()

        clear_all(con, entities)

        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                break
            elif event.type == 'MOUSEMOTION':
                mouse_coordinates = event.cell
        else:
            user_input = None

        # FIX: user_input double dips, key is CHAR once and then TEXT, with the same input.
        # The event type KEYDOWN is triggered twice when clicking a key once. The key is CHAR first, and then TEXT. 

        if not user_input and not fov_recompute:
            continue

        fov_recompute = False

        action = handle_keys(user_input, game_state, turn_state)

        move = action.get('move')
        increase_impulse = action.get('increase impulse')
        decrease_impulse = action.get('decrease impulse')
        maintain_impulse = action.get('maintain impulse')
        exit = action.get('exit')
        next_turn_phase = action.get('next_turn_phase')
        fullscreen = action.get('fullscreen')
        
        if exit:
            return True

        if fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())

        if game_state == GameStates.PLAYER_TURN:
            # See game_states.py for the turn structure.

            
            if turn_state == TurnStates.UPKEEP_PHASE:    
                message_log.add_message(Message('Begin MOVEMENT PHASE.', colors.get('white')))
                turn_state = TurnStates.PRE_MOVEMENT_PHASE
                fov_recompute = True
                
            if turn_state == TurnStates.PRE_MOVEMENT_PHASE:
                # Prompt to change impulse
                # TODO: A lot of repeat code here. Fix that.
                message_log.add_message(Message('Choose impulse. PAGEUP, PAGEDOWN or HOME.', colors.get('orange')))
                if increase_impulse: 
                    player.mech.impulse =  1
                    player.mech.remaining_impulse = player.mech.impulse
                    turn_state = TurnStates.MOVEMENT_PHASE
                    message_log.add_message(Message('Impulse increased.', colors.get('orange')))
                    fov_recompute = True
                    highlight_legal_moves(player, game_map)
                elif decrease_impulse: 
                    player.mech.impulse = -1
                    player.mech.remaining_impulse = player.mech.impulse
                    turn_state = TurnStates.MOVEMENT_PHASE
                    message_log.add_message(Message('Impulse decreased.', colors.get('orange')))
                    fov_recompute = True
                    highlight_legal_moves(player, game_map)
                elif maintain_impulse: 
                    player.mech.impulse =  0
                    player.mech.remaining_impulse = player.mech.impulse
                    turn_state = TurnStates.MOVEMENT_PHASE
                    message_log.add_message(Message('Impulse maintained.', colors.get('orange')))
                    fov_recompute = True
                    highlight_legal_moves(player, game_map)
            
            if turn_state == TurnStates.MOVEMENT_PHASE:
                if move:
                    dx, dy = move
                    if game_map.walkable[player.x + dx, player.y + dy]:
                        player.move(dx, dy)

                        fov_recompute = True
                    
                if next_turn_phase:
                    turn_state = TurnStates.POST_MOVEMENT_PHASE


            if turn_state == TurnStates.POST_MOVEMENT_PHASE:        
                reset_highlight(game_map)
                player.mech.reset() # Reset the mech for the next turn.
                fov_recompute = True

                turn_state = TurnStates.PRE_ATTACK_PHASE
            
            if turn_state == TurnStates.PRE_ATTACK_PHASE:
                message_log.add_message(Message('Begin ATTACK PHASE.', colors.get('white')))

                turn_state = TurnStates.ATTACK_PHASE
            
            if turn_state == TurnStates.ATTACK_PHASE:
                # Do nothing

                turn_state = TurnStates.POST_MOVEMENT_PHASE
            
            if turn_state == TurnStates.POST_MOVEMENT_PHASE:
                message_log.add_message(Message('Begin ENEMY TURN.', colors.get('white')))

                turn_state = TurnStates.UPKEEP_PHASE
                game_state = GameStates.ENEMY_TURN

        if game_state == GameStates.ENEMY_TURN:
            message_log.add_message(Message('Begin PLAYER TURN.', colors.get('white')))
            fov_recompute = True

            game_state = GameStates.PLAYER_TURN

if __name__ == '__main__':
    main()