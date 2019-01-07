import tcod as libtcod

from game_states import GameStates, TurnStates
from global_variables import TICKS_PER_TURN

class TowerAI:
    """
    This AI is used for towers.
    """
    def take_turn(self, game_state, turn_state, entities):
        results = []

        entity = self.owner

        for target in entities:
            if target.required_game_state == GameStates.PLAYER_TURN and not target.projectile:
                # We have found an entity to fire at.
                if entity.arsenal:
                    # Choose first weapon. Always.
                    w = entity.arsenal.weapons[0]
                    
                    w.targets.append((target.location.x, target.location.y))
                    results.extend(w.fire())

        return results

class DoNothing:
    """
    This is a place holder AI.
    """
    def take_turn(self, game_state, turn_state, entities):
        results = []

        enemy = self.owner

        if enemy.required_game_state == game_state:
            if turn_state == TurnStates.MOVEMENT_PHASE:
                enemy.action_points -= TICKS_PER_TURN // 2 # TODO: This is debug code.
                results.append({'message': '{0} does not move.'.format(enemy.name.capitalize())})
            if turn_state == TurnStates.ATTACK_PHASE:
                enemy.action_points -= TICKS_PER_TURN      # TODO: This is debug code.
                results.append({'message': '{0} does not choose a weapon.'.format(enemy.name.capitalize())})
        if not enemy.required_game_state == game_state:
            if turn_state == TurnStates.MOVEMENT_PHASE:
                enemy.action_points -= TICKS_PER_TURN      # TODO: This is debug code.
                results.append({'message': '{0} does not fire its weapon.'.format(enemy.name.capitalize())})
            if turn_state == TurnStates.ATTACK_PHASE:
                enemy.action_points = 0

        return results

class MoveAlongPath:
    """
    This AI moves an entity along a given path.
    """
    def take_turn(self, game_state, turn_state, entities):
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
                projectile.action_points = 0
        if not projectile.required_game_state == game_state:
            if turn_state == TurnStates.MOVEMENT_PHASE:
                projectile.action_points = 0
            if turn_state == TurnStates.ATTACK_PHASE:
                projectile.action_points = 0

        return results