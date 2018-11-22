import math

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
        """
        How movement works:

        TODO: Enforce a minimum tile movement.
        TODO: Use Peak Momentum as well
        TODO: Figure out how to track where the impulse point goes. 

        A mech may only move in a direction that matches their momentum. 
        If their momentum is 0, it can move in either direction, provided it has an impule point left.
        """

        max_h_mom = self.mech.maximum_horizontal_momentum
        acc_h_mom = self.mech.accumulated_horizontal_momentum
        max_v_mom = self.mech.maximum_vertical_momentum
        acc_v_mom = self.mech.accumulated_vertical_momentum
                
        # Attempt to move.
        if self.mech.calculate_accumulated_momentum() < self.mech.calculate_maximum_momentum(): # Ensure that the max momentum is not exceeded. This takes into account impulse.
            if abs(acc_h_mom) < abs(max_h_mom) and math.copysign(1, dx) == math.copysign(1, max_h_mom):                     # Ensure there is usable horizontal momentum and that it is in the correction direction.
                self.x += dx
                self.mech.accumulated_horizontal_momentum += dx
            elif abs(acc_v_mom) < abs(max_v_mom) and math.copysign(1, dx) == math.copysign(1, max_v_mom):                   # Ensure there is usable vertical momentum and that it is in the correction direction.
                self.y += dy
                self.mech.accumulated_vertical_momentum += dy
            elif self.mech.remaining_impulse == 1:                                                                          # At this point, momentum is maxed out. Spend impulse.
                # There is no diagonal movement, so one of these will be 0 anyway.
                # Having spent the impulse to move in that direction, increase its momentum.
                self.x += dx
                self.mech.bonus_h_mom += dx
                self.y += dy
                self.mech.bonus_v_mom += dy
                self.mech.remaining_impulse = 0
            elif self.mech.remaining_impulse == -1:                                                                         # At this point, momentum is maxed out. Reduce momentum.
                if abs(acc_h_mom) < abs(max_h_mom):
                    self.mech.maximum_horizontal_momentum -= 1
                elif abs(acc_v_mom) < abs(max_v_mom):
                    self.mech.maximum_vertical_momentum -= 1