from global_variables import get_blocking_entity, TICKS_PER_TURN
from systems.damage import obstacle_damage

"""
The Movement System governs how an entity may move.
"""

def movement(entity, entities, game_map):
    results = []
    xd, yd = -1, -1
    is_projectile = False

    if entity.action_points == 0:
        print('How did this entity get a chance to move?')
        return results

    if entity.projectile:
        if len(entity.projectile.path) > 0:
            xd, yd = entity.projectile.path.pop()
            is_projectile = True
        else:
            results.append({'remove': entity})
            return results
    elif entity.propulsion and len(entity.propulsion.path) > 0:
        xd, yd = entity.propulsion.path.pop(0)
    else:
        entity.action_points = 0
        return results

    # Running into a wall.
    if game_map.is_blocked(xd, yd):
        if is_projectile:
            results.append({'remove': entity})
        else:
            results.append(obstacle_damage(entity, (xd, yd)))
        
        return results
    
    # Running into another entity.
    blocking_entity = get_blocking_entity(entities, (xd, yd))
    if blocking_entity:
        print('{0} walked into {1}.'.format(entity.name, blocking_entity.name))
        if is_projectile:
            results.append({'remove': entity})
        else:
            if blocking_entity.projectile:
                results.append({'remove': blocking_entity})
        
        #return results
    
    entity.location.x = xd
    entity.location.y = yd
    entity.action_points -= TICKS_PER_TURN // entity.propulsion.speed

    return results

def cursor_movement(cursor, dx, dy):
    cursor.location.x += dx
    cursor.location.y += dy