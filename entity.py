class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, char, color, name, mech=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.mech = mech

        if self.mech:
            self.mech.owner = self

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy