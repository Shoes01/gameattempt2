### TODO: Need to plug this into the engine. Maybe wrap it in a class.

from collections import deque

class EventQueue:
    """
    The Event Queue that controls who does what, when.
    """
    def __init__(self):
        self.queue = deque()

    def register(self, entity):
        """
        Add an entity to the queue.
        TODO: There should be an entity manager that adds the entity to the queue.
        """
        self.queue.append(entity)

    def release(self, entity):
        """
        Remove an entity from the queue.
        TODO: The death function should call this.
        """
        self.queue.remove(entity)

    def tick(self):
        """
        Handles the queue.
        """
        if len(self.queue) > 0:
            entity = self.queue[0]                       # Take the first entity from the list,
            if entity.action_points > 0:                 # If the pool of points is positive, use this entity.
                return entity                            # Taking turns drains from the pool of points. It may drain into the negative, and so the next time this entity comes up, it may do nothing.
            else:
                self.queue.rotate()                          # Move it to the back of the list, because it does not have enough action points.
                entity.action_points += 27720 # TODO: constants
                return None

        return None

        # QUESTION: Does this accurately allow entities to take turns "out of order"?
        ### I think so, but I think that means most entitiy will have negative points most of them. Which is fine.
        # TODO: The speed of the entitiy will be based on their momentum. As they begin to move, the number of speed goes up.
        # CONSIDERATION: Taking a turn will take _a lot_ of action points, I think.
        ### This means that the queue will be rotated a lot of times with few actions taken.... this might cause problems.
        # CONSIDERATION: I don't need to stricly quantify how fast projectiles move and such. This queue will take care of things.
        ### However, it will be hard to predict where projectiles will be when you move.
        # QUESTION: If I am using an event queue... then "turns" aren't really a thing. It's the player's turn when they are at the top of the queue.
        ### Does this mean I don't need to player/enemy game states?
        ##### But I think I need them to manage the phases..