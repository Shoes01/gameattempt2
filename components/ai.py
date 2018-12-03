class DoNothing:
    def take_turn(self):
        results = []

        monster = self.owner

        results.append({'message': '{0} does nothing.'.format(monster.name.capitalize())})

        return results