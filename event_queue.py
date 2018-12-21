import heapq

from global_variables import TICKS_PER_TURN

class EventQueue:
    """
    The Event Queue that controls who does what, when.

The player entity needs to start in control.
When the player is ready to move, the event queue is filled.
The topmost (smallest value) entity is removed from the Q and executes their turn.
If they have ticks remaining, they are reentered into the Q.
Once the Q is empty, the turn changes, and the Q is refilled.

    """
    def __init__(self):
        self.queue = []
        heapq.heapify(self.queue)

    def empty(self):
        """
        Check to see if the queue is empty.
        """
        if len(self.queue) == 0:
            return True 
        return False

    def register_list(self, entities):
        """
        Add an entire list of entities to the queue.
        """
        for entity in entities:
            self.register(entity)

    def register(self, entity):
        """
        Add an entity to the queue.
        """
        criteria_a = -1 * entity.action_points
        criteria_b = -1 * entity.mech.speed
        heapq.heappush(self.queue, (criteria_a, criteria_b, entity.uuid)) # TODO: I used a UID instead of the actual entity last time... may need to do that here too.
    
    def release(self, entity):
        """
        Remove an entity from the queue.
        """
        self.queue.remove(entity)
        heapq.heapify(self.queue)

    def fetch(self):
        """
        Fetch the next entity's uuid to have a turn.
        This removes them from the queue.
        """
        if len(self.queue) > 0:
            return heapq.heappop(self.queue)[2]

        return None