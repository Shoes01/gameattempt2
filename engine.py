import tcod as libtcod

import factory

from death_functions import kill_enemy, kill_player
from fov_functions import initialize_fov, recompute_fov
from game_messages import MessageLog, Message
from game_states import GameStates, TurnStates
from input_handlers import handle_keys, handle_mouse
from loader_functions.initialize_new_game import get_constants, get_game_variables
from map_objects.game_map import GameMap
from render_functions import clear_all, erase_cell, render_all, RenderOrder

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
    event_queue = None

    player, cursor, entities, game_map, message_log, game_state, turn_state, event_queue = get_game_variables(constants)

    previous_game_state = game_state    

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    fov_recompute = True
    fov_map = initialize_fov(game_map)
    
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.location.x, player.location.y, constants['fov_radius'], constants['fov_light_walls'], constants['fov_algorithm'])

        entities_extended = entities.copy()
        entities_extended.append(cursor)

        render_all(
            con, panel, entities_extended, game_map, fov_map, fov_recompute, message_log, 
            constants['screen_width'], constants['screen_height'], constants['bar_width'], constants['panel_height'], constants['panel_y'],
            mouse, constants['colors'], status, constants['status_height'], constants['status_width'], constants['status_x'], game_state, turn_state, player, cursor)

        libtcod.console_flush()

        clear_all(con, entities_extended)

        fov_recompute = False
            
        """
        Handle the Player Actions.
        """
        action = handle_keys(key, game_state)
        mouse_action = handle_mouse(mouse)
        impulse = None # This is to avoid logic problems.

        move = action.get('move')                               # Attempt to move.
        impulse = action.get('impulse')                         # Adjust mech impulse.
        next_turn_phase = action.get('next_turn_phase')         # Move to the next phase.
        reset_targets = action.get('reset_targets')             # Reset targets.
        select = action.get('select')                           # A target has been selected via keyboard.
        show_weapons_menu = action.get('show_weapons_menu')     # Show the weapons menu in order to choose a weapon to fire.
        weapons_menu_index = action.get('weapons_menu_index')   # Choose an item from the weapons menu.
        look = action.get('look')                               # Enter the LOOK game state.
        exit = action.get('exit')                               # Exit whatever screen is open.
        fullscreen = action.get('fullscreen')                   # Set game to full screen.      

        left_click = mouse_action.get('left_click')  
        right_click = mouse_action.get('right_click')


        # TODO: Figure out where this should go.
        if look and game_state == GameStates.PLAYER_TURN:
            previous_game_state = game_state
            game_state = GameStates.LOOK
            cursor.cursor.turn_on(player)
            continue

        """
        Handle the turn.
        """
        if game_state == GameStates.ENEMY_TURN or game_state == GameStates.PLAYER_TURN:
            turn_results = []
            active_entity = None

            # Choose the active entity.
            if not event_queue.empty():
                entity_uuid = event_queue.fetch()
                for entity in entities:
                    if entity.uuid == entity_uuid:
                        active_entity = entity

            # This phase is not for the active_entity.
            if turn_state == TurnStates.UPKEEP_PHASE:
                for entity in entities:
                    if entity.required_game_state == game_state:
                        entity.reset()
                    else:
                        entity.reset(only_action_points=True)
                
                event_queue.register_list(entities)
                turn_state = TurnStates.PRE_MOVEMENT_PHASE

            # This phase is for the player only.
            if turn_state == TurnStates.PRE_MOVEMENT_PHASE:

                # Highlight the legal tiles (persistently).
                green_list, yellow_list, red_list = player.propulsion.get_movement_range()
                game_map.set_highlighted(green_list, color=libtcod.light_green)
                game_map.set_highlighted(yellow_list, color=libtcod.yellow)
                game_map.set_highlighted(red_list, color=libtcod.dark_red)
                if player.propulsion.chosen_tile:
                    game_map.set_highlighted(player.propulsion.path, color=libtcod.blue)
                    fov_recompute = True
                
                # Hovering the mouse draws a path to the cursor.
                if mouse and not player.propulsion.chosen_tile:
                    temp_path = player.propulsion.fetch_path_to_tile(mouse=mouse)
                    game_map.set_highlighted(temp_path, color=libtcod.blue)
                    fov_recompute = True

                # Clicking locks the path.
                if left_click:
                    # This should actually select the tile, and then
                    player.propulsion.reset()
                    player.propulsion.choose_tile(left_click)
                    game_map.set_highlighted(player.propulsion.path, color=libtcod.blue)
                    fov_recompute = True
                
                # Right clicking unlocks the path.
                if right_click:
                    player.propulsion.reset()
                    fov_recompute = True

                if next_turn_phase:
                    next_turn_phase = False
                    player.propulsion.update_speed()
                    turn_state = TurnStates.MOVEMENT_PHASE   
                
                elif game_state == GameStates.ENEMY_TURN:
                    turn_state = TurnStates.MOVEMENT_PHASE

            # This phase is the big one. All entities act, except for projectiles of this game_state.
            # This phase ends when all entities have spent their action_points.
            if turn_state == TurnStates.MOVEMENT_PHASE:
                if active_entity:
                    if active_entity is player:
                        turn_results.extend(player.propulsion.move())
                        
                        if active_entity.required_game_state == game_state:
                            if move:
                                dx, dy = move
                                if not game_map.tiles[player.location.x + dx][player.location.y + dy].blocked:
                                    player.mech.move(dx, dy)
                                    fov_recompute = True
                            
                            if next_turn_phase:
                                next_turn_phase = False
                                player.action_points = 0
                        
                        elif not active_entity.required_game_state == game_state:
                            turn_results.extend(player.arsenal.fire_active_weapon())
                
                    else:
                        turn_results.extend(active_entity.ai.take_turn(game_state, turn_state))
                        fov_recompute = True
                
                if active_entity is None and event_queue.empty():
                    turn_state = TurnStates.POST_MOVEMENT_PHASE
                    
            # This phase is not for the active_entity.
            if turn_state == TurnStates.POST_MOVEMENT_PHASE:
                game_map.reset_flags()                
                fov_recompute = True
                turn_state = TurnStates.PRE_ATTACK_PHASE

            # This phase is not for the active_entity.
            # Entities have their action points refilled in order to use their weapons.
            if turn_state == TurnStates.PRE_ATTACK_PHASE:
                if game_state == GameStates.PLAYER_TURN:
                    message_log.add_message(Message('Press f to target. Press ESC to stop targeting. Enter to change phase. Press r to choose new targets.', libtcod.orange))

                for entity in entities:
                    entity.reset(only_action_points=True)
                
                event_queue.register_list(entities)
                turn_state = TurnStates.ATTACK_PHASE
            
            # This phase is for active_entity of the required game_state.
            # They choose their weapons and targets.
            if turn_state == TurnStates.ATTACK_PHASE:
                if active_entity:
                    if active_entity is player:
                        if active_entity.required_game_state == game_state:
                            if show_weapons_menu:
                                previous_game_state = game_state
                                game_state = GameStates.SHOW_WEAPONS_MENU

                            if reset_targets:
                                active_entity.arsenal.reset()
                                message_log.add_message(Message('Targeting reset.', libtcod.light_blue))
                                game_map.reset_flags()
                                fov_recompute = True

                            if next_turn_phase:
                                next_turn_phase = False
                                active_entity.action_points = 0

                        else:
                            active_entity.action_points = 0

                    elif active_entity.ai:
                        turn_results.extend(active_entity.ai.take_turn(game_state, turn_state))
                
                if active_entity is None and event_queue.empty():
                    turn_state = TurnStates.POST_ATTACK_PHASE

            # This phase is not for active_entity.
            if turn_state == TurnStates.POST_ATTACK_PHASE:
                fov_recompute = True
                game_map.reset_flags()
                w = player.arsenal.get_active_weapon()
                if w is not None:
                    for x, y in w.targets:
                        erase_cell(con, x, y)

                turn_state = TurnStates.CLEANUP_PHASE
            
            # This phase is useless?
            if turn_state == TurnStates.CLEANUP_PHASE:
                if game_state == GameStates.PLAYER_TURN:
                    game_state = GameStates.ENEMY_TURN
                elif game_state == GameStates.ENEMY_TURN:
                    game_state = GameStates.PLAYER_TURN
                
                turn_state = TurnStates.UPKEEP_PHASE
            
            # Refill the queue with the active_entity, if appropriate.
            if active_entity and active_entity.action_points > 0:
                event_queue.register(active_entity)

            # Communicate turn_results.
            for result in turn_results:
                message = result.get('message')
                dead_entity = result.get('dead')
                remove_entity = result.get('remove')
                new_projectile = result.get('new_projectile')

                if dead_entity:
                    if dead_entity == player:
                        message, game_state = kill_player(dead_entity)
                    else:
                        message = kill_enemy(dead_entity)
                
                    event_queue.release(dead_entity)
                
                if new_projectile:
                    entity_type, location, target, APs, required_game_state = new_projectile
                    projectile = factory.entity_factory(entity_type, location, entities)
                    projectile.action_points = APs
                    xo, yo = location
                    xd, yd = target
                    projectile.projectile.path = list(libtcod.line_iter(xd, yd, xo, yo))
                    projectile.projectile.path.pop()
                    projectile.required_game_state = required_game_state

                    event_queue.register(projectile)

                if remove_entity:
                    entities.remove(remove_entity)
                                
                if message: 
                    message_log.add_message(Message(message, libtcod.yellow))
                
        """
        Handle the targeting cursor.
        """
        if game_state == GameStates.TARGETING:
            targeting_results = []

            if move:
                cursor.cursor.move(move, player.arsenal.get_active_weapon(), player)

            elif select:
                cursor.cursor.target(game_map, player.arsenal.get_active_weapon())
                fov_recompute = True
            
            for result in targeting_results:
                message = result.get('message')
                target = result.get('target')
                
                if message:
                    message_log.add_message(Message(message, libtcod.red))
                
                if target:
                    pass                

        """
        Handle the Show Weapons Menu state.
        """
        if game_state == GameStates.SHOW_WEAPONS_MENU:
            menu_results = []

            if weapons_menu_index is not None and weapons_menu_index < len(player.arsenal.weapons) and previous_game_state != GameStates.PLAYER_DEAD:
                menu_results.append(player.arsenal.weapons[weapons_menu_index].activate())
                cursor.cursor.turn_on(player, player.arsenal.weapons[weapons_menu_index].targets)
                game_state = GameStates.TARGETING
            
            for result in menu_results:
                message = result.get('message')
                
                if message:
                    message_log.add_message(Message(message, libtcod.dark_green))

        """
        Handle the Look game state.
        """
        if game_state == GameStates.LOOK:
            if move:
                dx, dy = move
                cursor.location.move(dx, dy)
       
        """
        Handle the death of the player.
        """
        if game_state == GameStates.PLAYER_DEAD:
            print('You have died.')
            return True
        
        """
        Handle commands that activate regardless of game state.
        """
        if exit:
            if game_state == GameStates.SHOW_WEAPONS_MENU or game_state == GameStates.LOOK:
                game_state = previous_game_state
                cursor.cursor.turn_off()
            
            elif game_state == GameStates.TARGETING:
                cursor.cursor.turn_off()    

                fov_recompute = True
                game_state = previous_game_state
            
            else:
                return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

if __name__ == '__main__':
    main()