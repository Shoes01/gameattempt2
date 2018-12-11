# INERTIAL COMBAT
A simple mech arena shooter centered around managing momentum.

## DEPENDENCIES
Requires python 3 and python-tcod. 
Run engine.py.

## BUGS
__General__

Movement highlighting logic: when h_mov = 2, v_mom = 1 and impulse = -1, the mech can move to three places. That's not right.

## ROAD MAP
- [x] Momentum Based Momement
- [x] Basic obstacles
- [x] Single Tile Targeting
- [x] First Weapon System: Laser
- [x] Multi Tile Targeting
- [x] Basic UI
  - [x] Display momentum and impulse levels
  - [x] Display weapon information
  - [x] Display remaining HP
- [x] QoL Maintenance
  - [x] Allow the player to "set and forget" momentum level
  - [x] Allow the player to cancel targeting entirely and restart
  - [X] Implement a RenderOrder
- [x] Enemy NPC: Destroyable
  - [x] Implement death function
  - [x] Implement weapon damage
  - [x] Implement a turn summary variable
- [-] Improve code
  - [x] Provide adequate documentation
  - [x] Decouple what can be decoupled
  - [x] Move things out of engine.py
  - [x] Create component managers
  - [x] Consider splitting the Mech class into a Propulsion class and a Chassis class (or something else that handles defense, HP, etc)    
    - [-] Move movement code to the Propulsion class
    - [x] Move damage code to the Chassis class
  - [x] Create a Location component
  - [x] Create a look function
- [ ] Animation
- [ ] Event Queue
  - [ ] Create an entity manager which adds entities to the queue
  - [ ] Update death function to remove from the queue
  - [ ] Weapons and movement are different. 
    - [ ] Movement uses the EQ, and is based on speed. 
    - [x] Weapons simply have a cooldown, and ticks down at the end of the turn.
- [ ] Second Weapon System: Ballistics
  - [x] Code logic to handle an entity with multiple weapons
  - [x] Allow the player to target a tile multiple times
  - [ ] Handle projectiles
- [ ] Improve code II
  - [ ] Lot's of messy features have been added
  - [ ] Ensure all player "actions" use the results variable to track events
  - [ ] Rename Mech class to Propulsion class
- [ ] Terrain
  - [ ] Consider using NumPy arrays to store map information
- [ ] Revisit turn structure
  - [ ] Decide where radar detection should happen
  - [ ] Decide where staggering should happen
  - [ ] Decide where damage should happen
- [ ] Revisit momentum logic
  - [ ] Should the player have fewer choices?
  - [ ] Should the player have a harder time slowing time?
  - [ ] Define how staggering, staggering badly and falling down will work
  - [ ] Generalize the logic to allow for impulses greater than 1
  - [ ] Use action points to decide this
- [ ] Revisit UI
  - [ ] Consider changing fonts
  - [ ] Implement a more cohesive UI
- [ ] QoL Maintenance II
  - [ ] Visually indicate to the user that a tile has been targeted multiple times (display a numeral on it)
  - [ ] Improve SHOW_WEAPONS_MENU 
    - [ ] Have names in color. RED: can't use, WHITE: usable, GREEN: online.
    - [ ] Allow to deactivate weapons.
    - [ ] Include the state of the weapon in its name.
- [ ] Enemy NPC: Firing logic
  - [ ] Ensure the player is able to die correctly
- [ ] Momentum based weapons
  - [ ] Weapons impart momentum on user and target
- [ ] Radar Based Detection
- [ ] Third Weapon System: Missiles
- [ ] Fourth Weapon System: Artillery
- [ ] Enemy NPC: Moving Logic
  - [ ] Having the AI move will require it lock in its momentum before starting, so that it's speed is constant
- [ ] Fifth Weapon System: Shock Combo
- [ ] Radar Based Stealth
- [ ] City Generation
- [ ] Objectives
- [ ] Mission Hub
- [ ] Experience Gain
- [ ] Loot
- [ ] Lore