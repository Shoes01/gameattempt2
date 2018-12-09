import tcod as libtcod

def draw_card(console, x, y, w, h, color, **kwargs):
    """
    A card is a UI element that displays information to the player.
    For example, the status of the player will be displayed on a card.
    """
    # The console on which things are drawn.
    # The x position on the console.
    # The y position on the console.
    # The width of the card.
    # The height of the card.
    # The dict of colors.
    # The color of the card.

    offset = 0

    for key, value in kwargs.items():
        libtcod.console_set_default_foreground(console, color)
        libtcod.console_print_ex(console, x, y + offset, libtcod.BKGND_NONE, libtcod.LEFT, '{0}: {1}'.format(key, value))
        offset += 1
        if offset == h:
            break
    