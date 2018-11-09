
# Write a class to hold player information, e.g. what room they are in
# currently.

"""Return a player object

Player holds player name, room and direction information and movement
methods.
"""
import textwrap
import os
import sys
import time
import random
from colorama import *
from items import items
from item import *


# Displays each character of the string in intervals, produces
# a typewriter effect
def tprint(string, speed=0.05):
    for character in string:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(speed)


# TODO: Refactore os.system('clear') to be better implemented - maybe with a DRAW GUI function

class Player:
    # Initialize the properties of the class
    def __init__(self, name=None, job=None, sex="Male", room=None,):
        self.game_over = False
        self.room = room
        self.name = name
        self.job = job
        self.sex = sex
        self.weapon = {}
        self.armour = {}
        self.shield = {}
        self.hand = {}
        self.direction = 'north'
        self.inventory = []
        self.level = 1
        self.exp = 0
        self.next_exp = 100
        self.hp = 100
        self.max_hp = 100
        self.mp = 100
        self.max_mp = 100
        self.gold = 1000
        self.message = ''

    # Return a formatted value of the Player class
    def __str__(self):
        return f"Name: {self.name}, Room: {self.room}"

    # Displays the player information onto the screen
    def player_info(self):
        # Inventory Formatting
        vita = self.weapon.vit + self.shield.vit + self.armour.vit
        dext = self.weapon.dex + self.shield.dex + self.armour.dex
        inte = self.weapon.int + self.shield.int + self.armour.int
        wisd = self.weapon.wis + self.shield.wis + self.armour.wis
        atk = self.weapon.attack + self.shield.attack + self.armour.attack
        max_hp = self.hp + self.weapon.hp + self.shield.hp + self.armour.hp
        max_mp = self.mp + self.weapon.mp + self.shield.mp + self.armour.mp

        os.system('clear')
        info = (f'  NAME: {Fore.GREEN}{self.name}{Style.RESET_ALL} <[{Fore.CYAN}{self.level}{Style.RESET_ALL}]> '
                f'[{self.job.name} - {self.sex}] - [{self.room.name}]\n'
                f'   WEAP: {self.weapon.name} - {self.weapon.description}\n'
                f'   ARMR: {self.armour.name} - {self.armour.description}\n'
                f'   SHLD: {self.shield.name} - {self.shield.description}\n'
                f'   HAND: {self.hand.name} - {self.hand.description}\n'
                f'    VIT: [{self.job.vitality}] + {vita}\n'
                f'    INT: [{self.job.dexterity}] + {dext}\n'
                f'    DEX: [{self.job.intelligence}] + {inte}\n'
                f'    WIS: [{self.job.wisdom}] + {wisd}\n\n'
                f'    HP {Fore.GREEN}{self.hp}{Style.RESET_ALL}/{Fore.GREEN}{max_hp}{Style.RESET_ALL}   '
                f'ATK: {Fore.LIGHTRED_EX}[{self.job.attack}] + {atk}{Style.RESET_ALL}   MP: {Fore.CYAN}'
                f'{self.mp}{Style.RESET_ALL}/{Fore.CYAN}{max_mp}{Style.RESET_ALL}   EXP: <{Fore.LIGHTRED_EX}'
                f'{self.exp}{Style.RESET_ALL}/{Fore.LIGHTRED_EX}{self.next_exp}{Style.RESET_ALL}>   GOLD: {Fore.YELLOW}'
                f'{self.gold}{Style.RESET_ALL}\n'
                f'  +----------------------------------------------------------------------+\n'
                f'  | INVENTORY:                                                           |\n'
                f'  +----------------------------------------------------------------------+')

        print('')
        print(info)

        if len(self.inventory) < 1:
            print("    No items in inventory")
            print('  +----------------------------------------------------------------------+\n')
            return
        count = 0
        for item in self.inventory:
            count += 1
            print(f'     [{Fore.GREEN}{count}{Style.RESET_ALL}] {item.name} - {item.description}')
        print('  +----------------------------------------------------------------------+\n')

    # Add an item to the inventory
    def pickup_item(self, item):
        os.system('clear')
        if self.room.is_light is False and isinstance(self.hand, Lightsource) is False:
            tprint('\n Good luck finding that item in the dark!\n')

        if self.room.contains(item):
            tprint(f'\n {Fore.GREEN}{item.name}{Style.RESET_ALL} picked up.')
            self.inventory.append(item)
            self.room.remove_item(item)

            if isinstance(item, Treasure):
                if item.is_taken() is False:
                    self.gold += item.gold

                item.on_take()
        else:
            tprint(f'\n {item.name} not found.', 0.02)

    # Drop an item from inventory to the current room
    def drop_item(self, item):
        os.system('clear')
        bl = False
        for itm in self.inventory:
            if itm == item:
                bl = True
                if isinstance(item, Lightsource):
                    item.on_drop()

                self.inventory.remove(item)
                self.room.add_item(item)
                tprint(f'\n {Fore.GREEN}{item.name}{Style.RESET_ALL} {Fore.RED}has been dropped{Style.RESET_ALL}')

        if bl is False:
            tprint(f'\n {Fore.GREEN}{item.name}{Style.RESET_ALL} {Fore.RED}is not in the inventory{Style.RESET_ALL}')

    # Equip the weapon
    def equip_weapon(self, target):
        os.system('clear')
        if target in self.inventory:

            # Checks if we don't have any other weapon equipped, if we do,
            # go ahead and swap the weapons out, bringing the already equipped to the
            # inventory
            if isinstance(target, Weapon):
                if self.weapon == items['EmptyW']:
                    self.weapon = target
                    self.inventory.remove(target)
                else:
                    self.inventory.append(self.weapon)
                    self.inventory.remove(target)
                    self.weapon = target
            elif isinstance(target, Armour):
                if self.armour == items['EmptyA']:
                    self.armour = target
                    self.inventory.remove(target)
                else:
                    self.inventory.append(self.armour)
                    self.inventory.remove(target)
                    self.armour = target
            elif isinstance(target, Shield):
                if self.shield == items['EmptyS']:
                    self.shield = target
                    self.inventory.remove(target)
                else:
                    self.inventory.append(self.shield)
                    self.inventory.remove(target)
                    self.shield = target
            elif isinstance(target, Lightsource):
                if self.hand == items['EmptyL']:
                    self.hand = target
                    self.inventory.remove(target)
                else:
                    self.inventory.append(self.hand)
                    self.inventory.remove(target)
                    self.hand = target
            elif isinstance(target, Item):
                if self.hand == items['EmptyL']:
                    self.hand = target
                    self.inventory.remove(target)
                else:
                    self.inventory.append(self.hand)
                    self.inventory.remove(target)
                    self.hand = target

            tprint(f'\n {Fore.GREEN}{target.name}{Style.RESET_ALL} was equipped.')
        else:
            tprint(f'\n {Fore.GREEN}{target.name}{Style.RESET_ALL} not in inventory')

    # Un-equip the weapon
    def unequip_weapon(self, target):
        os.system('clear')
        if isinstance(target, Weapon):
            if target == self.weapon:
                self.weapon = items['EmptyW']
                self.inventory.append(target)
                tprint(f'\n {Fore.GREEN}{target.name}{Style.RESET_ALL} was un-equipped.')
        elif isinstance(target, Shield):
            if target == self.shield:
                self.shield = items['EmptyS']
                self.inventory.append(target)
                tprint(f'\n {Fore.GREEN}{target.name}{Style.RESET_ALL} was un-equipped.')
        elif isinstance(target, Armour):
            if target == self.armour:
                self.armour = items['EmptyL']
                self.inventory.append(target)
                tprint(f'\n {Fore.GREEN}{target.name}{Style.RESET_ALL} was un-equipped.')
        elif isinstance(target, Lightsource):
            if target == self.hand:
                self.hand = items['EmptyL']
                self.inventory.append(target)
                tprint(f'\n {Fore.GREEN}{target.name}{Style.RESET_ALL} was un-equipped.')
        elif isinstance(target, Item):
            if target == self.hand:
                self.hand = items['EmptyL']
                self.inventory.append(target)
                tprint(f'\n {Fore.GREEN}{target.name}{Style.RESET_ALL} was un-equipped.')
        else:
            tprint(f'\n {Fore.GREEN}{target.name}{Style.RESET_ALL} is not equipped')

    # Look around the current room
    def look_around(self):
        os.system('clear')
        if self.room.is_light or isinstance(self.hand, Lightsource):
            if len(self.room.inventory) < 1:
                tprint("\n You looked around the room, but found no items\n")
                return

            tprint(f'\n You looked around the room and found:\n')
            count = 0
            for item in self.room.inventory:
                count += 1
                tprint(f' [{Fore.GREEN}{count}{Style.RESET_ALL}] {Fore.GREEN}{item.name}{Style.RESET_ALL}\n', 0.02)
        else:
            tprint("\n It is pitch black!\n")

    def room_message(self):
        os.system('clear')
        tprint(f'\n {self.room.name}\n', 0.03)
        if self.room.is_light or isinstance(self, Lightsource):
            desc = textwrap.wrap(self.room.description, width=70)
            for element in desc:
                tprint(f' {element}\n', 0.03)

    # Random encounters, 50/50 chance. 0 for safe, 1 for battle
    def random_encounter(self):
        if len(self.room.monsters) > 0:
            result = random.randint(0, 1)
            print(result)
            if result == 1:
                draw_battle_gui(self, self.room.monsters[0])
            else:
                self.room_message()
        else:
            self.room_message()

    # Handles the movement of the Player
    # Side Note: I didn't know about the attr method, this makes the
    # movement direction much much simpler
    def movedir(self, direction):
        self.direction = direction
        key = direction[0] + '_to'

        if not hasattr(self.room, key):
            # os.system('clear')
            tprint(f'\n {self.name} tried to move to {direction} but was blocked. Try another direction.\n')
            return self.room
        else:
            self.room = getattr(self.room, key)
            # self.random_encounter()

    # Player takes damage
    def on_take_dmg(self, dmg):
        if self.hp == 0:
            self.game_over = True
            tprint(f' <{self.name} has been defeated>')

        tprint(f' <{self.name} took {dmg}>')
        self.message = f' <{self.name} took {dmg}>'

    # Player attacks the monster
    def attack(self, target):
        target.hp -= self.job.attack
        target.on_take_dmg(self.job.attack)


# Monster Base Class - handles all the default monster and attributes
class Monster(Player):
    def __init__(self, name=None, job=None, room=None, attack=50, hp=100, max_hp=100, mp=100, max_mp=100, inventory=[],
                 exp=0, gold=0,):
        super().__init__(name, job, room, hp)
        self.mp = mp
        self.max_mp = max_mp
        self.max_hp = max_hp
        self.inventory = inventory
        self.exp = exp
        self.gold = gold
        self.dead = False
        self.attack = attack
        self.message = ''

    # When the monster is dead, drop all the items into the room
    def drop_item(self):
        if self.dead and len(self.inventory) > 0:
            for itm in self.inventory:
                self.room.add_item(itm)
                self.inventory.remove(itm)
                tprint(f'\n {Fore.GREEN}Items were dropped!{Style.RESET_ALL}')

        # Player takes damage

    def on_take_dmg(self, dmg):
        if self.hp == 0:
            self.dead = True
            tprint(f' <{self.name} has been defeated>')

        tprint(f' <{self.name} took {dmg}>')
        self.message = f' <{self.name} took {dmg}>'

    # TODO: Make this a random attack, i.e, if mage, use random skills + physical attacks
    # Monster attacks the player
    def attack(self, player):
        player.hp -= self.attack
        player.on_take_dmg(self.attack)


# TODO: Refactor this into own file
# ---------------------------- BATTLE SYSTEM ----------------------------


def battle_menu_selections(player, enemy):
    if enemy.dead:
        print(f'{player.name} has defeated {enemy.name}')
        player.room_message()
        return

    action = input("[ attack | run ] > ").split()
    combined_action = ' '.join(action[:2])
    valid_actions = ['attack', 'run']

    while action[0].lower() not in valid_actions:
        time.sleep(0.1)
        if combined_action in valid_actions:
            break

        tprint('> \n')
        action = input("[ attack | run ] > ").split()
        combined_action = ' '.join(action[:2])

    if action[0] == 'attack':
        player.attack(enemy)
        time.sleep(0.1)
        draw_battle_gui(player, enemy)
        time.sleep(0.1)
        if enemy.dead is False:
            enemy.attack(player)
            time.sleep(0.1)
            draw_battle_gui(player, enemy)
            time.sleep(0.1)
        else:
            print(f'{player.name} has defeated {enemy.name}')
            player.room_message()
            return
    elif action[0] == 'run':
        print('Player has ran')
        time.sleep(0.1)
        player.room_message()
        return


# TODO: Implement ascii art in separate file and load appropriate monster sprite
def draw_battle_gui(player, enemy):
    os.system('clear')
    print('+----------------------------------------------------------------------+\n'
          f'+ BATTLE                                                              +\n'
          '+----------------------------------------------------------------------+\n'
          '|                                                                      |\n'
          '|           ::::::::::::::::::::///++++osyhddmmmmmmm                   |\n'
          '|           ::::::::::::-.``..-://++++++++yddmmmmmmm                   |\n'
          '|           ::::::::::-..`````.-:/+++++++:-/ymNNNNNN                   |\n'
          '|           ///////::--..```..-://++++++ooo+ohmNNNNN                   |\n'
          '|           //////:://:-...--:://++++++oossyhdmNNNNN                   |\n'
          '|           ////::://+/::+/:///++++++++ossyyhhdmNNNN                   |\n'
          '|           ////:::-:/+++o+++++++++++yyosyyyhhdmNNNN                   |\n'
          '|           ++++/:..:+++++++++++++++oossyyyhhhdmNNNN                   |\n'
          '|           oooo+-.-/+++++++++++++ooosyyyhhhhddmNNNN                   |\n'
          '|           yysss+-:+++++++++++ooossyyhhhhhhddmNNNNN                   |\n'
          '|           yhhddhsoossooooooosssyyhhhhhhhddmmNNNNNN                   |\n'
          '|           /+oshmmdhhyyyyyyyyyyhhhhhhhhddmmmNNNNmmm                   |\n'
          '|           :..://ymmdhhhhhhhhhhhhhhhdddmmNNNNmmdhmN                   |\n'
          '|           /:/++/:smNmddhhhhhdddddmmmmNNNNNmdhso+dN                   |\n'
          '|           +++oossomNmmmmmmmmmmmNNNNNNNNmdhso++/yNN                   |\n'
          '|           +ossyyhdNNmmmmmNNNNNNNNNNNNmdho-.-+ymNNN                   |\n'
          '|           +osyddddmNmmmmmmNNNNNNNNNNmhhhhyshdmmmNN                   |\n'
          '|                                                                      |\n'
          '+----------------------------------------------------------------------+\n'
          f'{player.name.upper()} - <{player.hp} / {player.max_mp}> | {enemy.name.upper()} - <{enemy.hp} / '
          f'{enemy.max_mp}>\n'
          f'{player.message}\n'
          f'{enemy.message}')

    battle_menu_selections(player, enemy)
