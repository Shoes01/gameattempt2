# INERTIAL COMBAT
A simple mech arena shooter centered around managing momentum.

## DEPENDENCIES
Requires python 3 and python-tcod. 
Run engine.py.

## BUGS
__General__

Movement highlighting logic: when h_mov = 2, v_mom = 1 and impulse = -1, the mech can move to three places. That's not right.
  Mech should really just be: highlight tile (x + h_mov, y + v_mom)