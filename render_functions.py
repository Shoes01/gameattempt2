import math

def get_names_under_mouse(mouse_coordinates, entities, game_map):
    x, y = mouse_coordinates

    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and game_map.fov[entity.x, entity.y]]
    names = ', '.join(names)

    return names.capitalize()

def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color, string_color):
    # Render a bar (HP, experience, etc). first calculate the width of the bar
    bar_width = int(float(value) / maximum * total_width)

    # Render the background first
    panel.draw_rect(x, y, total_width, 1, None, bg=back_color)

    # Now render the bar on top
    if bar_width > 0:
        panel.draw_rect(x, y, bar_width, 1, None, bg=bar_color)

    # Finally, some centered text with the values
    text = name + ': ' + str(value) + '/' + str(maximum)
    x_centered = x + int((total_width-len(text)) / 2)

    panel.draw_str(x_centered, y, text, fg=string_color, bg=None)

def render_all(con, panel, entities, game_map, fov_recompute, root_console, message_log, screen_width, screen_height, bar_width, panel_height, panel_y, mouse_coordinates, colors):
    if fov_recompute:
        # Draw all the tiles in the game map
        for x, y in game_map:
            wall = not game_map.transparent[x, y]

            if game_map.fov[x, y]:
                if wall:
                    con.draw_char(x, y, None, fg=None, bg=colors.get('light_wall'))
                else:
                    con.draw_char(x, y, None, fg=None, bg=colors.get('light_ground'))

                    game_map.explored[x][y] = True
            elif game_map.explored[x][y]:
                if wall:
                    con.draw_char(x, y, None, fg=None, bg=colors.get('dark_wall'))
                else:
                    con.draw_char(x, y, None, fg=None, bg=colors.get('dark_ground'))
            
            if game_map.highlight[x][y]:
                con.draw_char(x, y, None, fg=None, bg=colors.get('highlight'))

    # Draw all entities in the list
    for entity in entities:
        draw_entity(con, entity, game_map.fov)

    root_console.blit(con, 0, 0, screen_width, screen_height, 0, 0)

    panel.clear(fg=colors.get('white'), bg=colors.get('black'))

    # Print the game messages, one line at a time
    y = 1
    for message in message_log.messages:
        panel.draw_str(message_log.x, y, message.text, bg=None, fg=message.color)
        y += 1

    render_bar(panel, 1, 1, bar_width, 'TEST', 20, 30,
               colors.get('light_red'), colors.get('darker_red'), colors.get('white'))

    panel.draw_str(1, 0, get_names_under_mouse(mouse_coordinates, entities, game_map))

    root_console.blit(panel, 0, panel_y, screen_width, panel_height, 0, 0)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov):
    if fov[entity.x, entity.y]:
        con.draw_char(entity.x, entity.y, entity.char, entity.color, bg=None)

def clear_entity(con, entity):
    # erase the character that represents this object
    con.draw_char(entity.x, entity.y, ' ', entity.color, bg=None)

def highlight_legal_moves(player, game_map):
    h_mom = player.mech.maximum_horizontal_momentum
    v_mom = player.mech.maximum_vertical_momentum
    mech_momentum = player.mech.calculate_maximum_momentum()

    minimum = 0 - abs(mech_momentum)
    maximum = 0 + abs(mech_momentum) + 1

    for x in range(minimum, maximum):
        for y in range(minimum, maximum):
            if (abs(x) + abs(y) >= mech_momentum - 2 and    # Ensure the tile exceeds the minimum.
                abs(x) <= abs(h_mom) + 1 and                # Ensure the x value is below the horizontal momentum.
                abs(y) <= abs(v_mom) + 1 and                # Ensure the y value is below the vertical momentum.
                abs(x) + abs(y) <= mech_momentum):          # Ensure that the x and y values are below the mech momentum. (This is to avoid the +1 being counted each way)
                # Now check to see that the direction matches the momentum.
                if h_mom == 0:                                                                      # x can be anything.
                    if v_mom == 0:                                                                      # y can be anything (this is the trivial case).
                        game_map.highlight[player.x + x][player.y + y] = True
                    elif v_mom != 0 and ( y == 0 or math.copysign(1, y) == math.copysign(1, v_mom) ):   # y must be 0 or have the same sign as v_mom.
                        game_map.highlight[player.x + x][player.y + y] = True
                elif h_mom != 0 and ( x == 0 or math.copysign(1, x) == math.copysign(1, h_mom) ):   # x must be 0 or have the same sign as h_mom.
                    if v_mom == 0:                                                                      # y can be anything.
                        game_map.highlight[player.x + x][player.y + y] = True
                    elif v_mom != 0 and ( y == 0 or math.copysign(1, y) == math.copysign(1, v_mom) ):   # y must be 0 or have the same sign as v_mom.
                        game_map.highlight[player.x + x][player.y + y] = True