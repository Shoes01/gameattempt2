import tcod as libtcod

import factory

from death_functions import kill_enemy, kill_player
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
    entities_player_turn = []
    entities_enemy_turn = []
    entities_special = []
    game_map = None
    message_log = None
    game_state = None
    turn_state = None
    event_queue = None

    player, cursor, entities_player_turn, entities_enemy_turn, entities_special, game_map, message_log, game_state, turn_state, event_queue = get_game_variables(constants)

    previous_game_state = game_state    

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    fov_recompute = True
    fov_map = initialize_fov(game_map)
    
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.location.x, player.location.y, constants['fov_radius'], constants['fov_light_walls'], constants['fov_algorithm'])

        all_entities = []
        all_entities.extend(entities_player_turn)
        all_entities.extend(entities_enemy_turn)
        all_entities.extend(entities_special)

        render_all(
            con, panel, all_entities, game_map, fov_map, fov_recompute, message_log, 
            constants['screen_width'], constants['screen_height'], constants['bar_width'], constants['panel_height'], constants['panel_y'],
            mouse, constants['colors'], status, constants['status_height'], constants['status_width'], constants['status_x'], game_state, turn_state, player, cursor)

        libtcod.console_flush()

        clear_all(con, all_entities)

        fov_recompute = False

        """
        Handle the turn order, and the entity whose turn it is.
        """
        entity_to_act = None

        # If the queue is empty, it's because the turn is over.
        if event_queue.empty() and turn_state == TurnStates.CLEANUP_PHASE:
            if game_state == GameStates.PLAYER_TURN:
                game_state = GameStates.ENEMY_TURN
                turn_state = TurnStates.UPKEEP_PHASE
                event_queue.register_list(entities_enemy_turn)

            elif game_state == GameStates.ENEMY_TURN:
                game_state = GameStates.PLAYER_TURN
                turn_state = TurnStates.UPKEEP_PHASE
                event_queue.register_list(entities_player_turn)
            else:
                print('Why is the queue empty?')
                return True
                
        entity_uuid = event_queue.fetch()
        
        if game_state == GameStates.ENEMY_TURN:
            for entity in entities_enemy_turn:
                if entity_uuid == entity.uuid:
                    entity_to_act = entity

        elif game_state == GameStates.PLAYER_TURN:
            for entity in entities_player_turn:
                if entity_uuid == entity.uuid:
                    entity_to_act = entity
            
        """
        Handle the Player Actions.
        """
        action = handle_keys(key, game_state)
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

        """
        Handle the Player Turn.
        """
        if game_state == GameStates.PLAYER_TURN:
            # Handle results from the player actions.
            player_turn_results = []

            # Decide the nature of the entity.
            projectile = None
            
            if entity_to_act and entity_to_act.projectile:
                projectile = entity_to_act
            
            # The player may look around during any game state.
            if look:
                previous_game_state = game_state
                game_state = GameStates.LOOK
                cursor.cursor.turn_on(player)
                continue

            if turn_state == TurnStates.UPKEEP_PHASE:
                message_log.add_message(Message('Choose impulse. PAGEUP, PAGEDOWN or HOME.', libtcod.orange))
                turn_state = TurnStates.PRE_MOVEMENT_PHASE
                highlight_legal_moves(player, game_map)
                fov_recompute = True

            elif turn_state == TurnStates.PRE_MOVEMENT_PHASE:
                if impulse is not None and abs(player.mech.impulse) <= abs(player.mech.max_impulse): 
                    player.mech.change_impulse(impulse)
                    message_log.add_message(Message('Impulse set to {0}.'.format(player.mech.impulse), libtcod.orange))                    
                    highlight_legal_moves(player, game_map)
                    fov_recompute = True
                
                if move or next_turn_phase:
                    turn_state = TurnStates.MOVEMENT_PHASE                

            if turn_state == TurnStates.MOVEMENT_PHASE: # This is not elif, so that the "move" action from above moves the player.
                # Player movement code.
                if entity_to_act is player:
                    if move:
                        dx, dy = move
                        if not game_map.tiles[player.location.x + dx][player.location.y + dy].blocked:
                            player.mech.move(dx, dy)
                            fov_recompute = True
                
                # Enemy projectile code.
                elif projectile is not None and projectile.moves_with_player is True: # TODO: The moves with player variable is deprecated.
                    player_turn_results.extend(projectile.ai.take_turn())
                    fov_recompute = True
                
                # End of movement code.
                if next_turn_phase:
                    turn_state = TurnStates.POST_MOVEMENT_PHASE

            elif turn_state == TurnStates.POST_MOVEMENT_PHASE:        
                game_map.reset_flags()                
                fov_recompute = True
                turn_state = TurnStates.PRE_ATTACK_PHASE

            elif turn_state == TurnStates.PRE_ATTACK_PHASE:
                message_log.add_message(Message('Press f to target. Press ESC to stop targeting. Enter to change phase. Press r to choose new targets.', libtcod.orange))
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
                player_turn_results.extend(player.fire_active_weapon(entities_enemy_turn, event_queue))

                # Reset map flags and remove targets.
                game_map.reset_flags()
                w = player.get_active_weapon()
                if w is not None:
                    for x, y in w.targets:
                        erase_cell(con, x, y)
                
                fov_recompute = True
                turn_state = TurnStates.CLEANUP_PHASE
            
            if turn_state == TurnStates.CLEANUP_PHASE:
                for entity in entities_player_turn:
                    entity.reset()
            
            for result in player_turn_results:
                message = result.get('message')
                dead_entity = result.get('dead')
                remove_entity = relust.get('remove')

                if dead_entity:
                    if dead_entity == player:
                        message, game_state = kill_player(dead_entity)
                    else:
                        message = kill_enemy(dead_entity)
                
                    event_queue.release(dead_entity)
                
                if remove_entity:
                    entities_player_turn.remove(remove_entity)
                    
                
                if message: 
                    message_log.add_message(Message(message, libtcod.yellow))
            
            # Put the entity back in the queue, if it has action points left.
            if entity_to_act and entity_to_act.action_points > 0 and entity_to_act is not cursor and turn_state is not TurnStates.CLEANUP_PHASE:
                event_queue.register(entity_to_act)
                
        """
        Handle the targeting cursor.
        """
        if game_state == GameStates.TARGETING:
            targeting_results = []

            if move:
                cursor.cursor.move(move, player.get_active_weapon(), player)

            elif select:
                cursor.cursor.target(game_map, player.get_active_weapon())
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

            if weapons_menu_index is not None and weapons_menu_index <= len(player.weapon) and previous_game_state != GameStates.PLAYER_DEAD:
                menu_results.append(player.weapon[weapons_menu_index].activate())
                cursor.cursor.turn_on(player, player.weapon[weapons_menu_index].targets)
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
        Handle the Enemy Turn.
        """
        if game_state == GameStates.ENEMY_TURN:
            enemy_turn_results = []

            # Decide the nature of the entity
            enemy = None
            projectile = None
            if entity_to_act:
                if entity_to_act.projectile:
                    projectile = entity_to_act
                elif entity_to_act.ai:
                    enemy = entity_to_act

            if turn_state == TurnStates.UPKEEP_PHASE:
                turn_state = TurnStates.PRE_MOVEMENT_PHASE

            elif turn_state == TurnStates.PRE_MOVEMENT_PHASE:
                turn_state = TurnStates.MOVEMENT_PHASE

            elif turn_state == TurnStates.MOVEMENT_PHASE:
                if enemy and not enemy.moves_with_player: # TODO: moves with player may be deprecated?
                    enemy_turn_results.extend(enemy.ai.take_turn())
                    fov_recompute = True
                
                if projectile and not projectile.moves_with_player:
                    enemy_turn_results.extend(projectile.ai.take_turn())
                    fov_recompute = True
                    
                if event_queue.empty() and not enemy and not projectile:
                    turn_state = TurnStates.POST_MOVEMENT_PHASE

            elif turn_state == TurnStates.POST_MOVEMENT_PHASE:
                turn_state = TurnStates.PRE_ATTACK_PHASE    
            
            elif turn_state == TurnStates.PRE_ATTACK_PHASE:
                turn_state = TurnStates.ATTACK_PHASE    
            
            elif turn_state == TurnStates.ATTACK_PHASE:
                turn_state = TurnStates.POST_ATTACK_PHASE

            elif turn_state == TurnStates.POST_ATTACK_PHASE:
                turn_state = TurnStates.CLEANUP_PHASE
            
            if turn_state == TurnStates.CLEANUP_PHASE:
                for entity in entities_enemy_turn:
                    entity.reset()

            for result in enemy_turn_results:
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
                    overseer, weapon = new_projectile
                    if len(weapon.targets) > 0:
                        xo, yo = overseer.location.x, overseer.location.y                
                        xd, yd = weapon.targets.pop()

                        overseer_projectile = factory.entity_factory(weapon.projectile, (xo, yo), entities_enemy_turn)                
                        overseer_projectile.projectile.path = list(libtcod.line_iter(xd, yd, xo, yo))
                        overseer_projectile.projectile.path.pop() # I want to remove the first entry.
                        overseer_projectile.action_points = overseer.action_points

                        event_queue.register(overseer_projectile)

                if remove_entity:
                    entities_enemy_turn.remove(remove_entity)
                    
                if message:
                    message_log.add_message(Message(message, libtcod.yellow))
            
            # Put the entity back in the queue, if it has action points left.
            if entity_to_act and entity_to_act.action_points > 0 and entity_to_act is not cursor and turn_state is not TurnStates.CLEANUP_PHASE:
                event_queue.register(entity_to_act)
                
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