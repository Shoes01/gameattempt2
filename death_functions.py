import libtcodpy as libtcod

from game_states import GameStates
from render_functions import RenderOrder

def kill_player(player):
    player.char = '%'
    player.color = libtcod.dark_red

    return 'You died!', GameStates.PLAYER_DEAD

def kill_enemy(enemy):
    death_message = '{0} is dead!'.format(enemy.name.capitalize())

    enemy.char = '%'
    enemy.color = libtcod.dark_red
    enemy.blocks = False
    enemy.fighter = None
    enemy.ai = None
    enemy.name = 'remains of ' + enemy.name
    enemy.render_order = RenderOrder.CORPSE

    return death_message