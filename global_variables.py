"""
This file contains global variables and methods.
"""

TICKS_PER_TURN = 26771144400   # LCM(1:26)

def distance_to(location, target):
    xl, yl = location
    xt, yt = target

    distance = abs(xl - xt) + abs(yl - yt)

    return distance