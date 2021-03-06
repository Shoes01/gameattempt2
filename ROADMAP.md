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
- [x] Improve code
  - [x] Provide adequate documentation
  - [x] Decouple what can be decoupled
  - [x] Move things out of engine.py
  - [x] Create component managers
  - [x] Consider splitting the Mech class into a Propulsion class and a Chassis class (or something else that handles defense, HP, etc)    
    - [x] Move movement code to the Propulsion class
    - [x] Move damage code to the Chassis class
  - [x] Create a Location component
  - [x] Create a look function
- [x] Event Queue
  - [x] Create an entity manager which adds entities to the queue
  - [x] Update death function to remove from the queue
  - [x] Weapons and movement are different. 
    - [x] Movement uses the EQ, and is based on speed. 
    - [x] Weapons simply have a cooldown, and ticks down at the end of the turn
- [x] Priority Queue
- [x] Second Weapon System: Ballistics
  - [x] Code logic to handle an entity with multiple weapons
  - [x] Allow the player to target a tile multiple times
  - [x] Handle projectiles
- [x] Refactor ballistic code
  - [x] All weapons should trigger Overseer entities that control the rate of fire during the next move phase.
- [x] Improve code II
  - [x] Rename Mech class to Propulsion class
  - [x] Create global_variables.py to store some constants
  - [x] Rendering component
  - [x] The "weapon component" of the Entity is really just a list of Weapon Components. Fix this.
  - [x] Cooldown is tied to rate_of_fire
- [x] Pathing Improvements
  - [x] Allow the player to set the speed at which the entity moves
  - [x] Clean up code
- [x] Collision detection
  - [x] Entities having their movement blocked
  - [x] Projectiles are blocked
  - [x] Projectiles continue indefinitely until blocked or outside map
- [ ] Damage Model
  - [ ] Entities take damage from projectiles
  - [ ] Entities inherit some momentum from projectiles
- [ ] Enemy NPC: Unintelligent movement
  - [ ] Make enemy entities spend their action points on moving.
  - [ ] Make enemy entities attempt to move in a square.
    - [ ] Move in one direction, then slow down to a stop, then change direction.
- [ ] Terrain
  - [ ] Consider using NumPy arrays to store map information
  - [ ] Create terrain that blocks movement
  - [ ] Create terrain that slows movement
  - [ ] Create terrain that makes turning difficult?
- [ ] Revisit turn structure
  - [ ] Consider using the Run & Gun Action/Planning turn structure
  - [ ] Decide where radar detection should happen
  - [ ] Decide where staggering should happen
  - [ ] Decide where damage should happen
  - [x] Add a cleanup phase
- [-] Revisit momentum logic
  - [ ] Define how staggering, staggering badly and falling down will work
  - [x] Generalize the logic to allow for impulses greater than 1
- [ ] Revisit UI
  - [ ] Consider changing fonts
  - [ ] Implement a more cohesive UI
  - [ ] Cursor can't be seen in the fog of war
- [ ] QoL Maintenance II
  - [ ] Allow the player to choose a tile outside of their legal tiles to move to, and handle pathing to it over several turns.
  - [ ] Visually indicate to the user that a tile has been targeted multiple times (display a numeral on it)
  - [ ] Improve SHOW_WEAPONS_MENU 
    - [ ] Have names in color. RED: can't use, WHITE: usable, GREEN: online.
    - [ ] Allow to deactivate weapons.
    - [ ] Include the state of the weapon in its name.
    - [ ] Include cooldown and descriptiono of weapons.
  - [ ] Show more pathing information to player
    - [ ] Decouple legal tiles calculation by moving the function to global variables.
    - [ ] Preview second order paths
    - [ ] Draw the "real" path to final destination
- [ ] Revisit projectile code
  - [ ] Optimize code
  - [ ] Allow projectiles to move indefinitely
  - [ ] Highlight the path projectiles are taking
  - [ ] Add variety to weapons by changing their properties when dealing with long distances
    - [ ] Lasers: Damage loss over distance
    - [ ] Ballistics: Accuracy loss over distance
- [ ] Enemy NPC: Firing logic
  - [ ] Ensure the player is able to die correctly
  - [ ] Ensure the NPC properly targets the player
- [ ] Momentum based weapons
  - [ ] Weapons impart momentum on user and target
- [ ] Radar Based Detection
- [ ] Third Weapon System: Missiles
  - [ ] Speed may change during flight
  - [ ] Must target the ground
- [ ] Fourth Weapon System: Artillery
- [ ] Enemy NPC: Moving Logic
  - [ ] Having the AI move will require it lock in its momentum before starting, so that it's speed is constant
- [ ] Fifth Weapon System: Shock Combo
- [ ] Sixth Weapon System: Denial of Area
  - [ ] May be fire, acid, EMP, or some other element
  - [ ] Is less effective against fast moving targets
- [ ] Seventh Weapon System: Auxillary Systems
  - [ ] Speed boosting system
  - [ ] Speed halting system
  - [ ] Smoke screen
  - [ ] Active camouflage
- [ ] Radar Based Stealth
- [ ] Animation
- [ ] City Generation
- [ ] Objectives
- [ ] Mission Hub
- [ ] Experience Gain
- [ ] Loot
- [ ] Lore
- [ ] Player controlled entities
  - [ ] PRE_MOVE phase: set all the impulses
  - [ ] MOVE phase: Choose the tile the entity will end on. AI will move it there.
  - [ ] POST_MOVE phase: move the entities to their target according to their speed, simultaneously and according to the path
  - [ ] COMBAT phase: choose and fire weapons for each entity
- [ ] Pilot Skills
  - [ ] Use a system like FFTA
- [ ] Improve Code III
  - [ ] User input component
  - [ ] Ensure all player "actions" use the results variable to track events
  - [ ] Consider not using the Entity class for the cursor