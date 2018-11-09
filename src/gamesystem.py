import os
import sys
import time
import textwrap
from colorama import *

from jobs import jobs
from rooms import room
from items import items
from player import Player
from characters import player
from colorama import Fore
from colorama import Style
from item import Lightsource


# Draws the title screen
def draw_title():
    col = f"{Fore.GREEN}"
    s = (""
         "                      ___________        .__                     _____ \n"
         "                      \__    ___/_____   |  |    ____     ____ _/ ____\ \n"
         "                        |    |   \__  \  |  |  _/ __ \   /  _ \   __\ \n"
         "                        |    |    / __ \_|  |__\  ___/  (  <_> )|  | \n"
         "                        |____|   (____  /|____/ \___  >  \____/ |__| \n"
         "                                      \/            \/\n"
         "                                                                                          \n"
         "                  ___________\n"
         "                  \__    ___/_____     ____ _______   ____    ____    ____ _______ _____ \n"
         "                    |    |   \__  \  _/ ___\_  __ \ /  _ \  /    \  /  _ \_  __ \__  \ \n"
         "                    |    |    / __ \_\  \___ |  | \/(  <_> )|   |  \(  <_> )|  | \/ / __ \_ \n"
         "                    |____|   (____  / \___  >|__|    \____/ |___|  / \____/ |__|   (____  / \n"
         "                                  \/      \/                     \/                     \/ \n"
         f"{Style.RESET_ALL}\n"
         "                              ~ Type P to start H for help or Q for quit ~ \n"
         "                                     Copyright Jeremy Boggs MIT 2018 \n")

    os.system('clear')
    print(col)
    print(s)


# Handles the commands for the title screen
def handle_title_selections():
    option = input("> ")

    if option.lower() in ['play', 'p']:
        setup_player()
    elif option.lower() in ['quit', 'q']:
        print('Play again!\n', 0.03)
        sys.exit()

    # Keep the menu going if not a recognized input
    while option.lower() not in ['play', 'quit', 'p', 'q']:
        handle_title_selections()


# Displays each character of the string in intervals, produces
# a typewriter effect
def tprint(string, speed=0.05):
    for character in string:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(speed)


# Sets up the player
def setup_player():
    question1 = "\n Enter Your Character's Name\n"
    question2 = "\n Are you male or female?\n"
    question3 = "\n Pick your class:\n" \
                     " Warrior\n" \
                     " Mage\n" \
                     " Thief\n"

    os.system('clear')
    print(question1)
    player_name = input("> ")

    while player_name == '':
        setup_player

    os.system('clear')
    print(question2)
    player_gender = input(" Gender > ")
    genders = ['male', 'female']

    if player_gender.lower() in genders:
        player_gender = player_gender.capitalize()
    while player_gender.lower() not in genders:
        player_gender = input("> ")
        if player_gender.lower() in genders:
            player_gender = player_gender.capitalize()

    os.system('clear')
    print(question3)
    player_job = input(" Class > ")
    all_jobs = ['warrior', 'mage', 'thief']

    if player_job.lower() in all_jobs:
        player.job = jobs[player_job.capitalize()]
        print('correct')
    while player_job.lower() not in all_jobs:
        player_job = input("Class > ")
        if player_job.lower() in all_jobs:
            player.job = jobs[player_job.capitalize()]

    question4 = f"\n {Fore.BLUE}{player_name.title()}{Style.RESET_ALL}, {Fore.BLUE}{player_gender}" \
                f"{Style.RESET_ALL}, {Fore.BLUE}{player_job}{Style.RESET_ALL} is correct? [y] " \
                f"yes or [n] no?\n"
    os.system('clear')
    print(question4)
    result = input(" Correct? > ")

    if result.lower() in ['yes', 'y']:
        # Setup player
        player.name = player_name.title()
        player.sex = player_gender
        player.room = room['outside']
        player.weapon = items['EmptyW']
        player.armour = items['EmptyA']
        player.shield = items['EmptyS']
        player.hand = items['EmptyL']
        player.hp = 100
        player.max_hp = 100
        player.mp = 100
        player.max_mp = 100
        player.gold = 0
        player.game_over = False

        room_message()
        main_game_loop()
    else:
        setup_player()


# TODO: Simplify/Abstract this
# Check if the item exists in the Items dict, and if exists,
# Use the player pickup method to pickup the item, if not,
# return a message printing item not found
def item_exists(item):
    bl = False
    for itm in items:
        if itm == item.title():
            bl = True
            return True

    if bl is False:
        return False


# Display the room message
def room_message():
    os.system('clear')
    tprint(f'\n {player.room.name}\n', 0.03)
    if player.room.is_light or isinstance(player.hand, Lightsource):
        desc = textwrap.wrap(player.room.description, width=70)
        for element in desc:
            tprint(f' {element}\n', 0.03)


# TODO: Simplify/Pretty up the actions
# Where the action happens
# Ask's the player what to do next and
# then handles the command that the player
# has given it.
def prompt():
    tprint(f'\n {Fore.CYAN}What do you do?{Style.RESET_ALL}', 0.03)

    # Input for the action to be taken - split into list
    action = input(" > ").split()
    combined_action = ' '.join(action[:2])

    # Complete list of all the actions to be done
    valid_actions = ['quit', 'character', 'char', 'i', 'inventory', 'get', 'take', 'pickup', 'drop', 'go', 'move',
                     'look around', 'examine room', 'equip', 'unequip', 'score', 'gold']

    # If the action is not a valid action
    while action[0].lower() not in valid_actions:
        # Break the loop if combined_action is in it
        # This makes the parsing of double-texted actions workable
        if combined_action in valid_actions:
            break

        tprint('Unknown action, try again\n')
        action = input(" > ").split()
        combined_action = ' '.join(action[:2])

    if combined_action.lower() in ['look around', 'examine room']:
        player.look_around()

    if action[0].lower() == 'quit':
        tprint('Play again!\n', 0.03)
        os.system('clear')
        sys.exit()

    elif action[0].lower() in ['go', 'move']:
        player.movedir(action[1].lower())
        player.random_encounter()
        # room_message()

    elif action[0].lower() in ['get', 'take', 'pickup']:
        item = ' '.join(action[1:])
        if item_exists(item):
            player.pickup_item(items[item.title()])
        else:
            print(f'You looked for a {item}, but did not find anything')

    elif action[0].lower() == 'drop':
        item = ' '.join(action[1:])
        if item_exists(item):
            player.drop_item(items[item.title()])
        else:
            print(f'You tried to drop {item}, but it\'s not in your inventory')

    elif action[0].lower() in ['character', 'i', 'inventory']:
        player.player_info()

    elif action[0].lower() in ['equip']:
        item = ' '.join(action[1:])
        if item_exists(item):
            player.equip_weapon(items[item.title()])
        else:
            print(f'You tried to equip {item}, but it\'s not in your inventory')

    elif action[0].lower() in ['unequip']:
        item = ' '.join(action[1:])
        if item_exists(item.title()):
            player.unequip_weapon(items[item.title()])
        else:
            print(f'You tried to un-equip {item}, but it\'s not equipped')

    elif action[0].lower() in ['gold', 'score']:
        tprint(f'You have {player.gold} GOLD', 0.05)


# Keep the game going until the player gets a game over
def main_game_loop():
    while player.game_over is False:
        prompt()
