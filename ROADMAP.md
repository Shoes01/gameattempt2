## PROJECTILE BRANCH
The weapon component will use the entity_factory() to create a projectile.
The factory will create a projectile Entity with the following:
  - name, char, color
  - projectile component: speed, damage
    - path and moves_with_player are set after the fact (entity needs a faction component!)
  - location component: the first tile on the path
  - ai component: simply moves to a new tile

Player projectiles move on the enemy's turn. Vice versa.

Need to rewrite how damage is done, as the gun is not the one doing damage.
    Damage_type: pulse_laser
        The "entity" that is created should be more of a manager. It has no location.
        It is given a path and a speed. It deals damage to first target in the path. (Also draws a line)

    Damage_type: ballistic
        The "entity" that is created is a moving bullet.
        When it moves into something blockable, it deals damage.
    
    Damage_type: missile
        The "entity" that is created is a moving missile.
        It is given the tile where the player is currently standing at the start of the turn.
        It updates position at the beginning of every turn.
            This allows the player to outurn the missile, or to put an obstacle between them and it.

# BUG #
Not moving spends no time, so the player may shoot indefinitely. APs need to be zeroed after the move phase.
QUESTION: Why have ticks at all? The turn order shouldn't change, so speed should just be how many moves per turn a player can do.

# TICKS PER TURN #
Entities can't overload their turn. Their speed means "moves per turn", and will never go into the negatives.

# TURN ORDER #
Player Turn and Enemy Turn seem to be artificial, or at least only serve to ensure everyone gets their turn.

Things that move on Player Turn:
Player controlled entities
Enemey fired projectiles

Things that move on Enemy Turn:
Enemy controlled entities
Enemy fired projectiles

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
- [ ] Second Weapon System: Ballistics
  - [x] Code logic to handle an entity with multiple weapons
  - [x] Allow the player to target a tile multiple times
  - [ ] Handle projectiles
  - [ ] Instant speed projectiles need to communicate which tile is being hit every turn
- [ ] Improve code II
  - [ ] Lot's of messy features have been added
  - [ ] Ensure all player "actions" use the results variable to track events
    - [ ] Is this an Observer pattern?
  - [ ] Rename Mech class to Propulsion class
  - [x] Create global_variables.py to store some constants
    - [ ] Should other constants be moved there..?
  - [ ] Remove Cursor from list of entities, and update the rendering code to reflect this
  - [ ] The move function should be the one that cares about obstacles
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
  - [ ] Cursor can't be seen in the fog of war
- [ ] QoL Maintenance II
  - [ ] Visually indicate to the user that a tile has been targeted multiple times (display a numeral on it)
  - [ ] Improve SHOW_WEAPONS_MENU 
    - [ ] Have names in color. RED: can't use, WHITE: usable, GREEN: online.
    - [ ] Allow to deactivate weapons.
    - [ ] Include the state of the weapon in its name.
- [ ] Animation
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
- [ ] Player controlled entities
  - [ ] PRE_MOVE phase: set all the impulses
  - [ ] MOVE phase: draw a path for the entity to travel (or have it do this automatically)
  - [ ] POST_MOVE phase: move the entities to their target according to their speed, simultaneously and according to the path
  - [ ] COMBAT phase: choose and fire weapons for each entity