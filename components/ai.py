import tcod as libtcod

from game_states import GameStates, TurnStates
from global_variables import TICKS_PER_TURN

class DoNothing:
    """
    This is a place holder AI.
    """
    def take_turn(self, game_state, turn_state):
        results = []

        enemy = self.owner

        if enemy.required_game_state == game_state:
            if turn_state == TurnStates.MOVEMENT_PHASE:
                results.append({'message': '{0} does not move.'.format(enemy.name.capitalize())})
            if turn_state == TurnStates.ATTACK_PHASE:
                results.append({'message': '{0} does not choose a weapon.'.format(enemy.name.capitalize())})
        if not enemy.required_game_state == game_state:
            if turn_state == TurnStates.MOVEMENT_PHASE:
                results.append({'message': '{0} does not fire its weapon.'.format(enemy.name.capitalize())})

        return results

class MoveAlongPath:
    """
    This AI moves an entity along a given path.
    """
    def take_turn(self, game_state, turn_state):
        results = []

        projectile = self.owner

        if projectile.required_game_state == game_state:
            if turn_state == TurnStates.MOVEMENT_PHASE:
                # Move.
                if len(projectile.projectile.path) > 0:
                    x, y = projectile.projectile.path.pop()
                    dx = x - projectile.location.x
                    dy = y - projectile.location.y

                    projectile.location.move(dx, dy)
                else:
                    results.append({'remove': projectile})

            if turn_state == TurnStates.ATTACK_PHASE:
                # Nothing... unless it has an arsenal, then it fires its weapons.
                ### Notice that the projectiles fired by projectiles maintains the required_game_state.
                pass
        if not projectile.required_game_state == game_state:
            if turn_state == TurnStates.MOVEMENT_PHASE:
                # Nothing.
                pass
            if turn_state == TurnStates.ATTACK_PHASE:
                # Nothing.
                pass

        return results