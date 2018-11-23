# INERTIAL COMBAT
A simple mech arena shooter centered around managing momentum.

## DEPENDENCIES
Requires python 3 and tdl. 
Run engine.py.

## ISSUES
Things only refresh after there is user_input.
  * Have a pre-phase where messages are displayed

## TODO
* Inform the player of their h_mom and v_mom, and how much of each is remaining.
   The "+1" in the mech_momentum code represents acceleration, decceleration, or maintenance
* Decide on what happens when a player is hit by projectiles.
   If momentum is reduced by 1: stagger, may not accelerate
   If momentum is reduced by 2: stagger badly, must slow down
   If momentum is reduced by 3: fall down
   There should be a bonus resistance to stagger/falling based on??
* Decide on what kind of targeting patterns the player can use.
   Draw the line manually?
   Rotate the line / spread the line out?
   Only have | / - patterns? Plus a spread?
* Things currently missing from the Turn Structure comment in game_states.py
   How radar detection will work.
   How stagger / falling will work.
   How damage will work.

## BUGS
None reported

## DEVELOPEMENT MILESTONES
- [x] Momentum Based Momement
- [ ] Basic obstacles
- [ ] Single Tile Targeting
- [ ] Multi Tile Targeting
- [ ] First Weapon System: Laser
- [ ] Enemy NPC: Destroyable
- [ ] Animation
- [ ] Event Queue
- [ ] Second Weapon System: Ballistics
- [ ] Terrain
- [ ] Enemy NPC: Firing logic
- [ ] Radar Based Detection
- [ ] Third Weapon System: Missiles
- [ ] Fourth Weapon System: Artillery
- [ ] Enemy NPC: Moving Logic
- [ ] Fifth Weapon System: Shock Combo
- [ ] Radar Based Stealth
- [ ] City Generation
- [ ] Objectives
- [ ] Mission Hub
- [ ] Experience Gain
- [ ] Loot
- [ ] Lore