"""
The Damage System governs how entities are damaged.
"""
def obstacle_damage(entity, obstacle):
    " Damage here is taken due to running into an obstacle. "
    # TODO: In the future, running into an obstacle shouldn't result in a full stop.
    xo, yo = obstacle   

    entity.action_points = 0
    
    entity.chassis.hp -= entity.propulsion.speed
    
    entity.propulsion.speed_x = 0
    entity.propulsion.speed_y = 0

    return {'message': 'The {0} ran into an obstacle.'.format(entity.name.capitalize())}

def take_damage(entity, projectile=None):
    " Damage here is taken due to being hit by a projectile. "
    " Momentum is also transfered. "
    pass