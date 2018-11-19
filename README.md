# gameattempt2
Attempt 2 at making a game

# ISSUES
The Message log renders after the first click, which means it is one click behind what the player is doing.
Fix: None. It's place holder code anyway...

# TODO
Add Tile logic
  * Allow tiles to be highlighted
Add FOV logic
Add more phases (ex: pre-movement phase)
  * pre-* phases will print messages once
  * post-* phases will clear highlighted tiles and the like
Allow player to change their momentum delta during the pre-movement phase
  * This means the "speed" of movement and a tick is determined before the player starts to move
  * This affects the "+1" in the mech_momentum code
Inform the player of their h_mom and v_mom, and how much of each is remaining.
  * The "+1" in the mech_momentum code represents acceleration, decceleration, or maintenance