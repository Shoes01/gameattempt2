from global_variables import get_blocking_entity, TICKS_PER_TURN
from systems.damage import obstacle_damage

"""
The Movement System governs how an entity may move.
"""

def movement(entity, entities, game_map):
    results = []

    # TODO: Put collision detection here.

    if entity.projectile: # TODO: Is it odd that projectiles get special treatement?
        if len(entity.projectile.path) > 0:
            xd, yd = entity.projectile.path.pop()
            if game_map.tiles[xd][yd].blocked or get_blocking_entity(entities, (xd, yd)):
                results.append({'remove': entity})
            else:
                entity.location.x = xd
                entity.location.y = yd
                entity.action_points -= TICKS_PER_TURN // entity.propulsion.speed
        else:
            results.append({'remove': entity})

    elif not entity.propulsion or not entity.propulsion.path:
        entity.action_points = 0
    elif entity.action_points == 0:
        print('How did the user manage to move the entity so far that they spent all their APs?')
    elif entity.location:
        xd, yd = entity.propulsion.path.pop(0)
        if game_map.tiles[xd][yd].blocked:
            results.append(obstacle_damage(entity, (xd, yd)))

        else:
            entity.location.x = xd
            entity.location.y = yd
            entity.action_points -= TICKS_PER_TURN // entity.propulsion.speed
    
    return results

def cursor_movement(cursor, dx, dy):
    cursor.location.x += dx
    cursor.location.y += dy