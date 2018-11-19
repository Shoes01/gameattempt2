# gameattempt2
Attempt 2 at making a game


# ISSUES
The Message log renders after the first click, which means it is one click behind what the player is doing.
Fix: None. It's place holder code anyway...

# TODO
Create a "mech" component in which to store the entity's Momentum.
Read the mech component in order to highlight legal tiles to move to.
Allow the player to choose the tile to move to. 
  * Illegal tiles will cause the mech to fall.
  * The speed of the mech will be determined by the tile chosen.
  * How is the path to the tile decided? 
    Easy: the player doesn't decide, E-W moves first, then N-S. 
    Hard: the player draws the path they want.
Unhighlight the tiles, move the mech to where it wants to go, update it's momentum, start a new turn.
Wrap all this code around the FOV recompute stuff