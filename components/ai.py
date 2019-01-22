import tcod as libtcod

from game_states import GameStates, TurnStates
from global_variables import distance_to, get_blocking_entity, TICKS_PER_TURN
from random import randrange
from systems.movement import movement

class TowerAI:
    """
    This AI is used for towers.
    """
    def take_turn(self, game_state, turn_state, entities, game_map=None):
        results = []

        entity = self.owner

        if entity.required_game_state == game_state:
            if turn_state == TurnStates.ATTACK_PHASE:
                """ The Entity may choose a weapon this phase. """

                entity.action_points -= TICKS_PER_TURN

                number_of_weapons = len(entity.arsenal.weapons)
                random_number = randrange(number_of_weapons)
                weapon = entity.arsenal.weapons[random_number]

                results.extend(entity.arsenal.activate_weapon(weapon))

        elif not entity.required_game_state == game_state:
            if turn_state == TurnStates.MOVEMENT_PHASE:
                """ The Entity may fire its chosen weapon this phase. """

                for target in entities:
                    if target.required_game_state == GameStates.PLAYER_TURN and not target.projectile:
                        # We have found an entity to fire at.
                        if entity.arsenal:
                            location = (entity.location.x, entity.location.y)
                            target = (target.location.x, target.location.y)
                            w = entity.arsenal.get_active_weapon()
                            
                            if w and distance_to(location, target) <= w.range:
                                w.targets = [target]
                                results.extend(w.fire())
                            else:
                                entity.action_points -= TICKS_PER_TURN
        
        if len(results) == 0:
            results.append({'end_turn': True})

        return results

class DoNothing:
    """
    This is a place holder AI.
    """
    def take_turn(self, game_state, turn_state, entities, game_map=None):
        results = []

        enemy = self.owner

        if enemy.required_game_state == game_state:
            if turn_state == TurnStates.MOVEMENT_PHASE:
                """ The Entity may move during this phase. """
                enemy.action_points -= TICKS_PER_TURN // 2
                results.append({'message': '{0} does not move.'.format(enemy.name.capitalize())})

            if turn_state == TurnStates.ATTACK_PHASE:
                """ The Entity may choose a weapon this phase. """
                enemy.action_points -= TICKS_PER_TURN
                results.append({'message': '{0} does not choose a weapon.'.format(enemy.name.capitalize())})

        if not enemy.required_game_state == game_state:
            if turn_state == TurnStates.MOVEMENT_PHASE:
                """ The Entity may fire its chosen weapon this phase. """
                enemy.action_points -= TICKS_PER_TURN
                results.append({'message': '{0} does not fire its weapon.'.format(enemy.name.capitalize())})

            if turn_state == TurnStates.ATTACK_PHASE:
                """ The Entity does nothing this phase. """
                enemy.action_points = 0

        return results

class ProjectileAI:
    """
    This AI moves an entity along a given path.
    """
    def take_turn(self, game_state, turn_state, entities, game_map):
        results = []

        projectile = self.owner

        if projectile.required_game_state == game_state:
            if turn_state == TurnStates.MOVEMENT_PHASE:
                # Move.
                results.extend(movement(projectile, entities, game_map))
            if turn_state == TurnStates.ATTACK_PHASE:
                projectile.action_points = 0
        if not projectile.required_game_state == game_state:
            if turn_state == TurnStates.MOVEMENT_PHASE:
                projectile.action_points = 0
            if turn_state == TurnStates.ATTACK_PHASE:
                projectile.action_points = 0

        return results