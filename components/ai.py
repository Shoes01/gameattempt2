class DoNothing:
    """
    This is a place holder AI.
    """
    def take_turn(self):
        results = []

        enemy = self.owner

        enemy.action_points -= 26771144400 + 1

        results.append({'message': '{0} does nothing.'.format(enemy.name.capitalize())})

        return results