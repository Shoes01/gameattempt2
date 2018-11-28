def draw_card(console, x, y, w, h, colors, color, **kwargs):
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
        console.draw_str(x, y + offset, '{0}: {1}'.format(key, value), fg=colors.get(color), bg=None)
        offset += 1
        if offset == h:
            break
    