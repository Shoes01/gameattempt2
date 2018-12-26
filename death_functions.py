import libtcodpy as libtcod

from game_states import GameStates
from render_functions import RenderOrder

def kill_player(player):
    player.render.char = '%'
    player.render.color = libtcod.dark_red
    player.action_points = 0

    return 'You died!', GameStates.PLAYER_DEAD

def kill_enemy(enemy):
    death_message = '{0} is dead!'.format(enemy.name.capitalize())

    enemy.render.char = '%'
    enemy.render.color = libtcod.dark_red
    enemy.blocks = False
    enemy.fighter = None
    enemy.ai = None
    enemy.name = 'remains of ' + enemy.name
    enemy.render_order = RenderOrder.CORPSE
    enemy.action_points = 0

    return death_message