from enum import auto, Enum


class GameStates(Enum):
   PLAYER_TURN = auto()
   ENEMY_TURN = auto()
   TARGETING = auto()
   PLAYER_DEAD = auto()
   SHOW_WEAPONS_MENU = auto()
   LOOK = auto()

class TurnStates(Enum):

   """

   Structure of a turn


   PLAYER_TURN begins.

   UPKEEP_PHASE
   1) The player is informed of things that happened last turn, such as the enemy weapon choice.
   PRE_MOMVEMENT_PHASE
   1) The player may adjust their impulse.
   2) Legal tiles to which the player can move are highlighted.
   3) This phase ends when the player begins to move.
   3.1) At this time, the player is given action points for their pool, equal to TICKS_PER_TURN / speed.
   3.2) TICKS_PER_TURN is the LCM(1:25) = 26771144400
   MOVEMENT_PHASE
   1) The player is given a limit of moves, based on their momentum. This determines time needed to move one tile.
      The player is free to use the moves in the order they wish; they are not forced to start with horizontal moves, then do vertical.
      The player may not "undo" moves.
      When the player begins to move, impulse can no longer be changed.
   2) As the player moves, the fov is updated.
   3) As the player moves, enemy projectiles move too, based on their own speed. Faster projectiles will move more tiles for each single tile the player moves.
   4) If the player rams into projectiles, it will affect their next turn's momentum.
   5) If the player rams into obstacles, it will affect their next turn's momentum.
      Example: if they are forced to ram into a wall for three turns, that's a lot more damaging than ramming into a wall for one turn! The wall may also collapse.
   POST_MOVEMENT_PASE
   1) Legal tiles to which the player can move are unhighlighted.
   2) Any relevant message is passed to the player.
   PRE_ATTACK_PHASE
   1) Any relevant message is passed to the player.
   ATTACK_PHASE
   1) The player is reminded of their current momentum.
   2) The player chooses a weapon.
   3) The player chooses a targeting pattern.
      Targeting pattern options: vertical line, diagonal line, horizontal line, focused on one point
      Targeting pattern options: Tight line, spread out line
   4) The player locks in their choice, ending the phase.
   POST_ATTACK_PHASE
   1) Any relevant message is passed to the player.
   PLAYER_TURN ends.

   ENEMY_TURN begins.
   The enemy AI goes through the same hoops.

   """

   UPKEEP_PHASE = auto()        # Messages related to the previous enemy turn are relayed.
   PRE_MOVEMENT_PHASE = auto()  # Impulse is chosen, legal tiles are highlighted for the player.
   MOVEMENT_PHASE = auto()      # Mech moves to a permitted position, projectiles move as well.
   POST_MOVEMENT_PHASE = auto() # Legal tiles are unhighlighted.
   PRE_ATTACK_PHASE = auto()    # Messages are displayed for the player.
   ATTACK_PHASE = auto()        # Mech decides what to fire where.
   POST_ATTACK_PHASE = auto()   # Final cleanup.