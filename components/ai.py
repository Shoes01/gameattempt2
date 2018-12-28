import tcod as libtcod

from global_variables import TICKS_PER_TURN

class DoNothing:
    """
    This is a place holder AI.
    """
    def take_turn(self):
        results = []

        enemy = self.owner

        enemy.action_points -= TICKS_PER_TURN // 2

        results.append({'message': '{0} does nothing.'.format(enemy.name.capitalize())})

        return results

class MoveAlongPath:
    """
    This AI moves an entity along a given path.
    """
    def take_turn(self):
        results = []

        projectile = self.owner

        if len(projectile.projectile.path) > 0:
            x, y = projectile.projectile.path.pop()
            dx = x - projectile.location.x
            dy = y - projectile.location.y

            projectile.location.move(dx, dy)
        else:
            results.append({'remove': projectile})

        return results

class Overseer:
    """
    This AI controls how projectiles are made.
    """
    def take_turn(self):
        results = []

        overseer = self.owner
        weapon = overseer.weapon[0]

        if overseer.action_points == 0 or len(weapon.targets) == 0:
            results.append({'remove': overseer})
        else:
            overseer.action_points -= TICKS_PER_TURN // weapon.rate_of_fire
            results.append({'new_projectile': (overseer, weapon)})
        
        return results