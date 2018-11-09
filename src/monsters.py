from item import *
from items import items
from jobs import jobs
from player import Monster

# Initialize all the monsters
slime = Monster()
slime.name = 'Slime'
slime.description = 'Slime slime'
slime.attack = 5
slime.exp = 10
slime.gold = 10
slime.hp = 50
slime.max_hp = 50
slime.mp = 50
slime.max_mp = 50
slime.inventory = [items['Book']]
slime.dead = False
slime.message = ''

bat = Monster()
bat.name = 'Bat'
bat.description = 'A dark nat'
bat.attack = 5
bat.exp = 10
bat.gold = 10
bat.hp = 50
bat.max_hp = 50
bat.mp = 50
bat.max_mp = 50
bat.inventory = []
bat.dead = False
bat.message = ''

monsters = {'Slime': slime, 'Bat': bat}
