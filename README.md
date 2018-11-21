# gameattempt2
Attempt 2 at making a game

# ISSUES
Things only refresh after there is user_input.
  * Have a pre-phase where messages are displayed

# TODO
Use new phases.
  * Rebuild how the keys are handled (to limit code duplication, have "generic" key handlers?)
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
Once enemies are a thing, split GameStates into GameStates (PLAYER/ENEMY TURN) and TurnStates

# DEVELOPMENT MILESTONE - MOMENTUM BASED MOVEMENT
  In progress.
# DEVELOPMENT MILESTONE - TARGETING
# DEVELOPMENT MILESTONE - FIRST WEAPON SYSTEM: LASER
# DEVELOPMENT MILESTONE - ANIMATION
# DEVELOPMENT MILESTONE - SECOND WEAPON SYSTEM: BALLISTICS
# DEVELOPMENT MILESTONE - TERRAIN
# DEVELOPMENT MILESTONE - ENEMY NPC CAPAPBLE OF FIRING
# DEVELOPMENT MILESTONE - RADAR BASED DETECTION
# DEVELOPMENT MILESTONE - THIRD WEAPON SYSTEM: MISSILES
# DEVELOPMENT MILESTONE - FOURTH WEAPON SYSTEM: ARTILLERY
# DEVELOPMENT MILESTONE - ENEMY NPC CAPABLE OF MOVING
# DEVELOPMENT MILESTONE - FIFTH WEAPON SYSTEM: SHOCK COMBO
# DEVELOPMENT MILESTONE - RADAR BASED STEALTH
# DEVELOPMENT MILESTONE - CITY GENERATION
# DEVELOPMENT MILESTONE - OBJECTIVES
# DEVELOPMENT MILESTONE - MISISON HUB
# DEVELOPMENT MILESTONE - EXPERIENCE GAIN
# DEVELOPMENT MILESTONE - LOOT SALVAGE
# DEVELOPMENT MILESTONE - LORE