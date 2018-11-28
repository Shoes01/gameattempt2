import tdl

from components.cursor import Cursor
from components.mech import Mech
from components.weapon import Weapon
from entity import Entity
from game_messages import MessageLog, Message
from game_states import GameStates, TurnStates
from input_handlers import handle_keys
from map_utils import GameMap, make_map, reset_flags, set_targeted
from render_functions import clear_all, erase_cell, highlight_legal_moves, render_all

def main():
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
        'light red': (255, 100, 100),
        'red': (255, 0, 0),
        'yellow': (255, 255, 0),
        'orange': (255, 127, 0),
        'green': (0, 255, 0,),
        'light_red': (255, 114, 114),   
        'darker_red': (127, 0, 0),
        'highlight': (199, 234, 70)
    }

    mech_component = Mech(max_hp=30, peak_momentum=6)
    weapon_component = Weapon(name="Laser", damage=5, min_targets=0, max_targets=5, color=colors.get('green'), range=10)
    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', colors.get('white'), "player", mech=mech_component, weapon=weapon_component)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', colors.get('yellow'), "NPC")
    cursor_component = Cursor()
    cursor = Entity(-1, -1, ' ', colors.get('red'), "cursor", cursor=cursor_component) # The ' ' isn't actually "nothing". To have nothing, I would have to mess with a render order.
    entities = [npc, player, cursor]

    tdl.set_font('rexpaint_cp437_10x10.png')

    root_console = tdl.init(screen_width, screen_height, title='MVP v0.0')
    con = tdl.Console(screen_width, screen_height)
    panel = tdl.Console(screen_width, panel_height)
    status = tdl.Console(status_width, status_height)

    game_map = GameMap(map_width, map_height)
    make_map(game_map)

    message_log = MessageLog(message_x, message_width, message_height)

    mouse_coordinates = (0, 0)

    game_state = GameStates.PLAYER_TURN
    previous_game_state = game_state
    turn_state = TurnStates.UPKEEP_PHASE

    fov_recompute = True
    
    while not tdl.event.is_window_closed():
        if fov_recompute:
            game_map.compute_fov(player.x, player.y, fov=fov_algorithm, radius=fov_radius, light_walls=fov_light_walls)

        render_all(
            con, panel, entities, game_map, fov_recompute, root_console, message_log, screen_width, screen_height, bar_width, panel_height, panel_y, mouse_coordinates, colors, 
            status, status_height, status_width, status_x, game_state, turn_state, player)

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

        fov_recompute = False

        action = handle_keys(user_input, game_state)
        impulse = None           # This is to avoid logic problems.
        change_game_state = None # This is to avoid logic problems.

        move = action.get('move')                           # Attempt to move.
        impulse = action.get('impulse')                     # Adjust mech impulse.
        next_turn_phase = action.get('next turn phase')     # Move to the next phase.
        change_game_state = action.get('change game state') # Go to different game_state
        select = action.get('select')                       # A target has been selected via keyboard.
        exit = action.get('exit')                           # Exit whatever screen is open.
        fullscreen = action.get('fullscreen')               # Set game to full screen.
        
        if exit:
            if game_state == GameStates.TARGETING:
                # Turn off cursor
                cursor.char = ' '
                cursor.x = -1
                cursor.y = -1

                fov_recompute = True
                game_state = previous_game_state
            
            else:
                return True

        if fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())

        if game_state == GameStates.PLAYER_TURN:
            # See game_states.py for the turn structure.
            # Turns order is reversed so ensure that the loop runs once for each
            if turn_state == TurnStates.POST_ATTACK_PHASE:
                # Reset map flags and remove targets.
                reset_flags(game_map)
                for x, y in player.weapon.targets:
                    erase_cell(con, x, y)
                turn_state = TurnStates.UPKEEP_PHASE
                game_state = GameStates.ENEMY_TURN
                
            if turn_state == TurnStates.ATTACK_PHASE:
                if change_game_state == GameStates.TARGETING:
                    # Turn on cursor.
                    cursor.char = 'X'
                    # If there were no previous targets, start on the player.
                    if len(player.weapon.targets) == 0:                        
                        cursor.x = player.x
                        cursor.y = player.y
                    else:
                        cursor.x, cursor.y = player.weapon.targets[-1]

                    fov_recompute = True
                    previous_game_state = game_state
                    game_state = GameStates.TARGETING

                if next_turn_phase:
                    turn_state = TurnStates.POST_ATTACK_PHASE
                    
            if turn_state == TurnStates.PRE_ATTACK_PHASE:
                message_log.add_message(Message('Begin ATTACK PHASE.', colors.get('white')))
                message_log.add_message(Message('Press f to target. Press ESC to stop targeting. Enter to change phase.', colors.get('orange')))
                fov_recompute = True

                turn_state = TurnStates.ATTACK_PHASE
                
            if turn_state == TurnStates.POST_MOVEMENT_PHASE:        
                reset_flags(game_map)
                player.reset() # Reset the mech for the next turn. ### Move this to the post-attack phase
                fov_recompute = True

                turn_state = TurnStates.PRE_ATTACK_PHASE

            if turn_state == TurnStates.MOVEMENT_PHASE:
                if move:
                    dx, dy = move
                    if game_map.walkable[player.x + dx, player.y + dy]:
                        player.move(dx, dy)

                        fov_recompute = True
                
                if next_turn_phase and player.mech.has_spent_minimum_momentum():
                    turn_state = TurnStates.POST_MOVEMENT_PHASE
                elif next_turn_phase and not player.mech.has_spent_minimum_momentum():
                    message_log.add_message(Message('Must spend more momentum.', colors.get('red')))

            if turn_state == TurnStates.PRE_MOVEMENT_PHASE:
                if impulse is not None: 
                    player.mech.impulse = impulse
                    turn_state = TurnStates.MOVEMENT_PHASE
                    message_log.add_message(Message('Impulse set to {0}.'.format(impulse), colors.get('orange')))
                    fov_recompute = True
                    highlight_legal_moves(player, game_map)

            if turn_state == TurnStates.UPKEEP_PHASE and game_state == GameStates.PLAYER_TURN: # This is added to avoid starting the Upkeep Phase when the turn just ended.
                message_log.add_message(Message('Begin PLAYER TURN.', colors.get('white')))
                message_log.add_message(Message('Begin MOVEMENT PHASE.', colors.get('white')))
                message_log.add_message(Message('Choose impulse. PAGEUP, PAGEDOWN or HOME.', colors.get('orange')))
                turn_state = TurnStates.PRE_MOVEMENT_PHASE
                fov_recompute = True

        if game_state == GameStates.ENEMY_TURN:
            message_log.add_message(Message('Begin ENEMY TURN.', colors.get('white')))
            fov_recompute = True

            game_state = GameStates.PLAYER_TURN
        
        if game_state == GameStates.TARGETING:
            if move:
                dx, dy = move
                # Ensure the first target is in firing range.
                if len(player.weapon.targets) == 0:
                    if player.distance(cursor.x + dx, cursor.y + dy) <= player.weapon.range:
                        cursor.fly(dx, dy)
                        fov_recompute = True
                    else:
                        message_log.add_message(Message('Out of range.', colors.get('red')))
                # Ensure that the next targets are adjacent to the previous target
                elif len(player.weapon.targets) > 0:
                    tar_x, tar_y = player.weapon.targets[-1] # Get the most recent target added.
                    if abs(tar_x - (cursor.x + dx)) + abs(tar_y - (cursor.y + dy)) <= 1:
                        cursor.fly(dx, dy)
                        fov_recompute = True
                    else:
                        message_log.add_message(Message('Invalid target.', colors.get('red')))

            if select:
                if len(player.weapon.targets) < player.weapon.max_targets:
                    if set_targeted(game_map, cursor.x, cursor.y):  # At the moment, this always returns True. In the future, this may change.
                        fov_recompute = True
                        player.weapon.targets.append((cursor.x, cursor.y))
                else:
                    message_log.add_message(Message('Targeting failed.', colors.get('red')))

if __name__ == '__main__':
    main()