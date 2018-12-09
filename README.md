# INERTIAL COMBAT
A simple mech arena shooter centered around managing momentum.

## DEPENDENCIES
Requires python 3 and python-tcod. 
Run engine.py.

## BUGS
__General__

None reported.

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
- [ ] Improve code
  - [ ] Provide adequate documentation
  - [-] Decouple what can be decoupled
  - [-] Move things out of engine.py
  - [x] Create component managers
  - [ ] Consider splitting the Mech class into a Propulsion class and a Chassis class (or something else that handles defense, HP, etc)
    - [ ] Move movement code to the Propulsion class
    - [x] Move damage code to the Chassis class
  - [ ] Create a Location component
  - [ ] Create a look function
- [ ] Animation
- [ ] Event Queue
- [ ] Second Weapon System: Ballistics
  - [x] Code logic to handle an entity with multiple weapons
  - [x] Allow the player to target a tile multiple times
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
  - [ ] Visually indicate to the user that a tile has been targeted multiple times (display a numeral on it)
- [ ] Enemy NPC: Firing logic
  - [ ] Ensure the player is able to die correctly
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