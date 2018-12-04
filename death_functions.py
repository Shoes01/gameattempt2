import libtcodpy as libtcod

from game_states import GameStates


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

    return death_message