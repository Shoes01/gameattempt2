# INERTIAL COMBAT
A simple mech arena shooter centered around managing momentum.

## DEPENDENCIES
Requires python 3 and tdl. 
Run engine.py.

## TODO
* Inform the player of their h_mom and v_mom, and how much of each is remaining.

   The "+1" in the mech_momentum code represents acceleration, decceleration, or maintenance  
   Allow the player to set what they want their maximum momentum to be, and automagically manage the impulse for them? And highlight differently the legal tiles too?

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
__General__
None reported.

## DEVELOPEMENT MILESTONES
- [x] Momentum Based Momement
- [x] Basic obstacles
- [x] Single Tile Targeting
- [x] First Weapon System: Laser
- [ ] Multi Tile Targeting
  - [ ] Enforce a range limit on the multi-tiles
- [ ] Basic UI
  - [ ] Display momentum and impulse levels
  - [ ] Display weapon information (number of current targets, max targets, total damage output)
  - [ ] Display remaining HP
- [ ] QoL Maintenance
  - [ ] Allow the player to "set and forget" momentum level
  - [ ] Allow the player to cancel targeting entirely, or confirm targeting. Highlight the tiles red instead of marking them with an X?
- [ ] Enemy NPC: Destroyable
  - [ ] Implement weapon damage
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