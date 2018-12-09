import tcod as libtcod

from components.ai import DoNothing
from components.cursor import Cursor
from components.mech import Mech
from components.weapon import Weapon
from death_functions import kill_enemy, kill_player
from entity import Entity
from fov_functions import initialize_fov, recompute_fov
from game_messages import MessageLog, Message
from game_states import GameStates, TurnStates
from input_handlers import handle_keys
from loader_functions.initialize_new_game import get_constants, get_game_variables
from map_objects.game_map import GameMap
from render_functions import clear_all, erase_cell, highlight_legal_moves, render_all, RenderOrder

def main():
    constants = get_constants()

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(constants['screen_width'], constants['screen_height'], title='MVP v0.0')

    con = libtcod.console_new(constants['screen_width'], constants['screen_height'])
    panel = libtcod.console_new(constants['screen_width'], constants['screen_height'])
    status = libtcod.console_new(constants['screen_width'], constants['screen_height'])  

    player = None
    cursor = None
    entities = []
    game_map = None
    message_log = None
    game_state = None
    turn_state = None

    player, cursor, entities, game_map, message_log, game_state, turn_state = get_game_variables(constants)

    previous_game_state = game_state    

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    fov_recompute = True
    fov_map = initialize_fov(game_map)
    
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, constants['fov_radius'], constants['fov_light_walls'], constants['fov_algorithm'])

        render_all(
            con, panel, entities, game_map, fov_map, fov_recompute, message_log, 
            constants['screen_width'], constants['screen_height'], constants['bar_width'], constants['panel_height'], constants['panel_y'],
            mouse, constants['colors'], status, constants['status_height'], constants['status_width'], constants['status_x'], game_state, turn_state, player)

        libtcod.console_flush()

        clear_all(con, entities)

        fov_recompute = False

        """
        Handle the Player Turn.
        """
        action = handle_keys(key, game_state)
        impulse = None           # This is to avoid logic problems.

        move = action.get('move')                               # Attempt to move.
        impulse = action.get('impulse')                         # Adjust mech impulse.
        next_turn_phase = action.get('next_turn_phase')         # Move to the next phase.
        reset_targets = action.get('reset_targets')             # Reset targets.
        select = action.get('select')                           # A target has been selected via keyboard.
        show_weapons_menu = action.get('show_weapons_menu')     # Show the weapons menu in order to choose a weapon to fire.
        weapons_menu_index = action.get('weapons_menu_index')   # Choose an item from the weapons menu.
        exit = action.get('exit')                               # Exit whatever screen is open.
        fullscreen = action.get('fullscreen')                   # Set game to full screen.
        
        """
        Handle the Player Turn.
        """
        if game_state == GameStates.PLAYER_TURN:
            # Handle results from the player actions.
            player_turn_results = []

            # See game_states.py for the turn structure.                                                    
            if turn_state == TurnStates.UPKEEP_PHASE:
                message_log.add_message(Message('Choose impulse. PAGEUP, PAGEDOWN or HOME.', libtcod.orange))
                turn_state = TurnStates.PRE_MOVEMENT_PHASE
                fov_recompute = True

            elif turn_state == TurnStates.PRE_MOVEMENT_PHASE:
                highlight_legal_moves(player, game_map)
                turn_state = TurnStates.MOVEMENT_PHASE
                fov_recompute = True

            elif turn_state == TurnStates.MOVEMENT_PHASE:
                if impulse is not None and not player.has_moved and abs(player.mech.impulse) <= abs(player.mech.max_impulse): 
                    player.mech.change_impulse(impulse)
                    message_log.add_message(Message('Impulse set to {0}.'.format(player.mech.impulse), libtcod.orange))                    
                    fov_recompute = True
                    highlight_legal_moves(player, game_map)

                if move:
                    dx, dy = move
                    if not game_map.tiles[player.x + dx][player.y + dy].blocked:
                        player.mech.move(dx, dy)

                        fov_recompute = True
                
                if next_turn_phase and player.mech.has_spent_minimum_momentum():
                    turn_state = TurnStates.POST_MOVEMENT_PHASE
                elif next_turn_phase and not player.mech.has_spent_minimum_momentum():
                    message_log.add_message(Message('Must spend more momentum.', libtcod.red))

            elif turn_state == TurnStates.POST_MOVEMENT_PHASE:        
                game_map.reset_flags()                
                fov_recompute = True

                turn_state = TurnStates.PRE_ATTACK_PHASE

            elif turn_state == TurnStates.PRE_ATTACK_PHASE:
                message_log.add_message(Message('Press f to target. Press ESC to stop targeting. Enter to change phase. Press r to choose new targets.', libtcod.orange))
                fov_recompute = True

                turn_state = TurnStates.ATTACK_PHASE

            elif turn_state == TurnStates.ATTACK_PHASE:
                if show_weapons_menu:
                    previous_game_state = game_state
                    game_state = GameStates.SHOW_WEAPONS_MENU

                if reset_targets:
                    player.weapon.reset()
                    message_log.add_message(Message('Targeting reset.', libtcod.light_blue))
                    game_map.reset_flags()
                    fov_recompute = True

                if next_turn_phase:
                    turn_state = TurnStates.POST_ATTACK_PHASE

            elif turn_state == TurnStates.POST_ATTACK_PHASE:
                # Fire the weapon
                player_turn_results.extend(player.fire_active_weapon(entities))

                # Reset the mech for the next turn.
                player.reset()
                
                # Reset map flags and remove targets.
                game_map.reset_flags()
                w = player.get_active_weapon()
                if w is not None:
                    for x, y in w.targets:
                        erase_cell(con, x, y)
                
                fov_recompute = True
                turn_state = TurnStates.UPKEEP_PHASE
                game_state = GameStates.ENEMY_TURN
            
            for result in player_turn_results:
                message = result.get('message')
                dead_entity = result.get('dead')

                if dead_entity:
                    if dead_entity == player:
                        message, game_state = kill_player(dead_entity)
                    else:
                        message = kill_enemy(dead_entity)
                
                if message: 
                    message_log.add_message(Message(message, libtcod.yellow))
                    fov_recompute = True
                
        """
        Handle the targeting cursor.
        """
        if game_state == GameStates.TARGETING:
            targeting_results = []

            if move:
                cursor.cursor.move(move, player.get_active_weapon(), player)

            if select:
                cursor.cursor.target(game_map, player.get_active_weapon())
                fov_recompute = True
            
            for result in targeting_results:
                message = result.get('message')
                target = result.get('target')
                
                if message:
                    message_log.add_message(Message(message, libtcod.red))
                    fov_recompute = True
                
                if target:
                    pass

        """
        Handle the Show Weapons Menu state.
        """
        if game_state == GameStates.SHOW_WEAPONS_MENU:
            menu_results = []

            if weapons_menu_index is not None and weapons_menu_index <= len(player.weapon) and previous_game_state != GameStates.PLAYER_DEAD:
                menu_results.append(player.weapon[weapons_menu_index].activate())
                cursor.cursor.turn_on(player, player.weapon[weapons_menu_index].targets)
                game_state = GameStates.TARGETING
            
            for result in menu_results:
                message = result.get('message')
                
                if message:
                    message_log.add_message(Message(message, libtcod.dark_green))
                    fov_recompute = True

        """
        Handle the Enemy Turn.
        """
        if game_state == GameStates.ENEMY_TURN:
            enemy_turn_results = {}

            if turn_state == TurnStates.UPKEEP_PHASE:
                turn_state = TurnStates.PRE_MOVEMENT_PHASE

            elif turn_state == TurnStates.PRE_MOVEMENT_PHASE:
                turn_state = TurnStates.MOVEMENT_PHASE

            elif turn_state == TurnStates.MOVEMENT_PHASE:
                for enemy in entities:
                    if enemy.ai:
                        enemy_turn_results = enemy.ai.take_turn()

                turn_state = TurnStates.POST_MOVEMENT_PHASE

            elif turn_state == TurnStates.POST_MOVEMENT_PHASE:
                turn_state = TurnStates.PRE_ATTACK_PHASE    
            
            elif turn_state == TurnStates.PRE_ATTACK_PHASE:
                turn_state = TurnStates.ATTACK_PHASE    
            
            elif turn_state == TurnStates.ATTACK_PHASE:
                turn_state = TurnStates.POST_ATTACK_PHASE

            elif turn_state == TurnStates.POST_ATTACK_PHASE:
                turn_state = TurnStates.UPKEEP_PHASE
                game_state = GameStates.PLAYER_TURN
            
            for result in enemy_turn_results:
                message = result.get('message')
                dead_entity = result.get('dead')

                if message:
                    message_log.add_message(Message(message, libtcod.yellow))
                    fov_recompute = True
                
                if dead_entity:
                    if dead_entity == player:
                        message, game_state = kill_player(dead_entity)
                    else:
                        message = kill_enemy(dead_entity)
                    message_log.add_message(Message(message, libtcod.yellow))
                    fov_recompute = True
                
        """
        Handle the death of the player.
        """
        if game_state == GameStates.PLAYER_DEAD:
            print('You are dead.')
            break
        
        """
        Handle commands that activate regardless of game state.
        """
        if exit:
            if game_state == GameStates.SHOW_WEAPONS_MENU:
                game_state = previous_game_state
            
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
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

if __name__ == '__main__':
    main()