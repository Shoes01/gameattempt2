class DoNothing:
    def take_turn(self):
        results = []

        enemy = self.owner

        results.append({'message': '{0} does nothing.'.format(enemy.name.capitalize())})

        return results