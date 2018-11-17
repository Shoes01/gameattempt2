import tdl

from entity import Entity
from game_messages import MessageLog, Message
from game_states import GameStates
from input_handlers import handle_keys
from map_utils import make_map
from render_functions import clear_all, render_all

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

    colors = {
        'dark_wall': (0, 0, 100),
        'dark_ground': (50, 50, 150),
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'red': (255, 0, 0),
        'orange': (255, 127, 0),
        'light_red': (255, 114, 114),
        'darker_red': (127, 0, 0)
    }

    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', (255, 255, 255), "player")
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', (255, 255, 0), "NPC")
    entities = [npc, player]

    tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)

    root_console = tdl.init(screen_width, screen_height, title='MVP v0.0')
    con = tdl.Console(screen_width, screen_height)
    panel = tdl.Console(screen_width, panel_height)

    game_map = tdl.map.Map(map_width, map_height)
    make_map(game_map)

    message_log = MessageLog(message_x, message_width, message_height)

    mouse_coordinates = (0, 0)

    game_state = GameStates.PLAYERS_TURN

    while not tdl.event.is_window_closed():
        render_all(con, panel, entities, game_map, root_console, message_log, screen_width, screen_height, bar_width, panel_height, panel_y, mouse_coordinates, colors)

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
                
        if not user_input:
            continue

        action = handle_keys(user_input, game_state)

        move = action.get('move')
        exit = action.get('exit')
        continue_ = action.get('continue')
        fullscreen = action.get('fullscreen')

        if game_state == GameStates.PLAYERS_TURN:
            message_log.add_message(Message('It is your turn! Press ENTER to go to Movement Phase.', colors.get('white')))
        elif game_state == GameStates.MOVEMENT_PHASE:
            message_log.add_message(Message('You can move! When you are done, you will go to Attack Phase.', colors.get('white')))
        elif game_state == GameStates.ATTACK_PHASE:
            message_log.add_message(Message('You are attacking! When you are done, it will be the enemy turn.', colors.get('white')))

        if continue_ and game_state == GameStates.PLAYERS_TURN:
            game_state == GameStates.MOVEMENT_PHASE

        if move:
            dx, dy = move
            if game_map.walkable[player.x + dx, player.y + dy]:
                player.move(dx, dy)

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