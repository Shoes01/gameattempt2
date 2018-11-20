import tdl

from components.mech import Mech
from entity import Entity
from game_messages import MessageLog, Message
from game_states import GameStates
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

    mech_component = Mech(hp=30, max_momentum=6)
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

    game_state = GameStates.PLAYERS_TURN

    fov_recompute = True
    
    while not tdl.event.is_window_closed():
        if fov_recompute:
            game_map.compute_fov(player.x, player.y, fov=fov_algorithm, radius=fov_radius, light_walls=fov_light_walls)

        render_all(con, panel, entities, game_map, fov_recompute, root_console, message_log, screen_width, screen_height, bar_width, panel_height, panel_y, mouse_coordinates, colors)

        tdl.flush()

        clear_all(con, entities)

        fov_recompute = False

        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                break
            elif event.type == 'MOUSEMOTION':
                mouse_coordinates = event.cell
        else:
            user_input = None
                
        if not user_input and not fov_recompute:
            continue

        action = handle_keys(user_input, game_state)

        move = action.get('move')
        exit = action.get('exit')
        begin_movement_phase = action.get('begin movement phase')
        end_movement_phase = action.get('end movement phase')
        end_attack_phase = action.get('end attack phase')
        fullscreen = action.get('fullscreen')

        if game_state == GameStates.PLAYERS_TURN:
            message_log.add_message(Message('It is your turn! Press ENTER to go to Movement Phase.', colors.get('white')))
        elif game_state == GameStates.MOVEMENT_PHASE:
            message_log.add_message(Message('You can move! When you do, you will go to Attack Phase.', colors.get('white')))
            highlight_legal_moves(player, game_map)
            fov_recompute = True

        elif game_state == GameStates.ATTACK_PHASE:
            reset_highlight(game_map)
            fov_recompute = True
            message_log.add_message(Message('You are attacking! Press ENTER to go to Enemy Turn.', colors.get('white')))

        if begin_movement_phase:
            game_state = GameStates.MOVEMENT_PHASE
            message_log.add_message(Message('Going to Movement Phase.', colors.get('orange')))

        if end_movement_phase:
            game_state = GameStates.ATTACK_PHASE
            message_log.add_message(Message('Going to Attack Phase.', colors.get('orange')))

        if end_attack_phase:
            game_state = GameStates.ENEMY_TURN
            message_log.add_message(Message('Going to the Enemy Turn.', colors.get('orange')))

        if move:
            dx, dy = move
            if game_map.walkable[player.x + dx, player.y + dy]:
                player.move(dx, dy)

                fov_recompute = True

        if exit:
            return True

        if fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity != player:
                    print('The ' + entity.name + ' ponders the meaning of its existence.')

            game_state = GameStates.PLAYERS_TURN

if __name__ == '__main__':
    main()