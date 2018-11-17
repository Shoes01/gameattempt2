from enum import Enum, auto


class GameStates(Enum):
    PLAYERS_TURN = auto()        # Player sees what the enemy mech will fire
    ENEMY_TURN = auto()          # Enemy sees waht the player mech will fire
    MOVEMENT_PHASE = auto()      # Mech moves to a permitted position, projectiles move as well
    ATTACK_PHASE = auto()        # Mech decides what to fire where