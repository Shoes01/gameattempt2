class DoNothing:
    """
    This is a place holder AI.
    """
    def take_turn(self):
        results = []

        enemy = self.owner

        enemy.action_points -= 26771144400 / 2

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

            results.append({'message': '{0} hopefully moved.'.format(projectile.name.capitalize())})

        else:
            results.append({'message': '{0} hopefully stopped.'.format(projectile.name.capitalize())})
            results.append({'dead': projectile})

        return results