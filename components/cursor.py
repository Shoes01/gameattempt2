class Cursor:
    def __init__(self):
        self.minimum = 0        # The minimum amount of tiles the cursor must highlight.
        self.maximum = 0        # The maximum amount of tiles the cursor must highlight.
        self.so_far = 0         # The amount of tiles highlited so far.
        self.target_list = []   # Keep track of which coordinates have been targeted.