import math

"""
This file contains global variables and methods.
"""

TICKS_PER_TURN = 26771144400   # LCM(1:26)

def distance_to(location, target, manhattan=True):
    xl, yl = location
    xt, yt = target

    if manhattan:
        distance = abs(xl - xt) + abs(yl - yt)
    else:
        distance = math.sqrt( (xl - xt)*(xl - xt) + (yl - yt)*(yl - yt) )

    return distance

def fill_in_line(line):
    new_line = []
    new_line.append(line.pop(0))

    while(len(line)):
        x1, y1 = new_line[-1]
        x2, y2 = line[0]

        if (x1 - x2)*(y1 - y2) == 0:
            # These points are good.
            new_line.append(line.pop(0))
        else:
            # These points are diagonal. Insert a new point, with a new x value but the same y value.
            dx = x2 - x1
            new_point = (x1 + dx, y1)
            new_line.append(new_point)
    
    # Remove the tile where the line starts.
    if new_line:
        new_line.pop(0)
    
    return new_line