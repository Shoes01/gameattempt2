# gameattempt2
Attempt 2 at making a game

# ISSUES
Things only refresh after there is user_input.
  * Have a pre-phase where messages are displayed

# TODO
Use new phases.
Allow player to change their momentum delta during the pre-movement phase
  * This means the "speed" of movement and a tick is determined before the player starts to move
  * This affects the "+1" in the mech_momentum code
Inform the player of their h_mom and v_mom, and how much of each is remaining.
  * The "+1" in the mech_momentum code represents acceleration, decceleration, or maintenance
Decide on what happens when a player is hit by projectiles.
  * If momentum is reduced by 1: stagger, may not accelerate
  * If momentum is reduced by 2: stagger badly, must slow down
  * If momentum is reduced by 3: fall down
  * There should be a bonus resistance to stagger/falling based on??
Decide on what kind of targeting patterns the player can use.
  * Draw the line manually?
  * Rotate the line / spread the line out?
  * Only have | / - patterns? Plus a spread?
Things currently missing from the Turn Structure comment in game_states.py
  * How radar detection will work.
  * How stagger / falling will work.
  * How damage will work.