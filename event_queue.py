import heapq

from global_variables import TICKS_PER_TURN

class EventQueue:
    """
    The Event Queue that controls who does what, when.

At the start of a turn, the queue is filled.
The topmost (smallest value) entity is removed from the Q and executes their turn.
If they have ticks remaining, they are reentered into the Q.
Once the Q is empty, the turn changes, and the Q is refilled.

    """
    def __init__(self):
        self.queue = []
        heapq.heapify(self.queue)

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
        heapq.heappush(self.queue, (-1 * entity.action_points_used, -1 * entity.mech.speed, entity))
    
    def release(self, entity):
        """
        Remove an entity from the queue.
        """
        self.queue.remove(entity)
        heapq.heapify(self.queue)

    def fetch(self):
        """
        Fetch the next entity have a turn.
        This removes them from the queue.
        """
        if len(self.queue) > 0:
            return heapq.heappop(self.queue)[2]

        return None