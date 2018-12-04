# INERTIAL COMBAT
A simple mech arena shooter centered around managing momentum.

## DEPENDENCIES
Requires python 3 and python-tcod. 
Run engine.py.

## BUGS
__General__

Need to find a way to ensure the enemy turn will eventually become the player turn.
    Move the enemy loop inside each turn state individually.

## ROAD MAP
- [x] Momentum Based Momement
- [x] Basic obstacles
- [x] Single Tile Targeting
- [x] First Weapon System: Laser
- [x] Multi Tile Targeting
- [x] Basic UI
  - [x] Display momentum and impulse levels
  - [x] Display weapon information (number of current targets, max targets, total damage output)
  - [x] Display remaining HP
- [x] QoL Maintenance
  - [x] Allow the player to "set and forget" momentum level
  - [x] Allow the player to cancel targeting entirely and restart
  - [X] Implement a RenderOrder
- [ ] Enemy NPC: Destroyable
  - [ ] Implement death function
  - [ ] Implement weapon damage
  - [ ] Implement a turn summary variable (found in part 6)
- [ ] Animation
- [ ] Event Queue
- [ ] Second Weapon System: Ballistics
  - [ ] Code logic to handle an entity with multiple weapons
  - [ ] Allow the player to target a tile multiple times
- [ ] Improve code
  - [ ] Provide adequate documentation
  - [ ] Decouple what can be decoupled
  - [ ] Move things out of engine.py
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
- [ ] Revisit UI
  - [ ] Consider changing fonts
  - [ ] Implement a more cohesive UI
- [ ] QoL Maintenance II
- [ ] Enemy NPC: Firing logic
- [ ] Momentum based weapons
  - [ ] Weapons impart momentum on user and target
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