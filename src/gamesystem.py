import os
import sys
from colorama import *


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


def setup_player():
    question1 = "\n Enter Your Character's Name\n"
    question2 = "\n Are you male or female?\n"
    question3 = "\n Pick your class:\n" \
                     " Warrior\n" \
                     " Mage\n" \
                     " Thief\n"

    os.system('clear')
    print(question1)
    player_name = input(" Name > ")

    while player_name == '':
        player_name = input(" Name > ")

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
        player_job = player_job.capitalize()
        print('correct')
    while player_job.lower() not in all_jobs:
        player_job = input("Class > ")
        if player_job.lower() in all_jobs:
            player_job = player_job.capitalize()

    question4 = f"\n {Fore.BLUE}{player_name.title()}{Style.RESET_ALL}, {Fore.BLUE}{player_gender}" \
                f"{Style.RESET_ALL}, {Fore.BLUE}{player_job}{Style.RESET_ALL} is correct? [y] " \
                f"yes or [n] no?\n"
    os.system('clear')
    print(question4)
    result = input(" Correct? > ")

    if result.lower() in ['yes', 'y']:
        print("Success")
        # Setup player
    else:
        setup_player()
