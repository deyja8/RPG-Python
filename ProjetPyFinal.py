#Python project

import cmd
import textwrap
import sys
import os
import time
import random

#Player Setup#

class player:
    def __init__(self):
        self.name = ''
        self.inventory = []
        self.location = 'Garage'
        self.game_won = False
myPlayer = player()

####### GAME MAP ########

"""
          
          '╔═════════════════╦═════════════╦═════════════════════╗\n'
          '║   Ranger truck  ║   Tunnel    ║    Rusted Tankers   ║\n'
          '╠═════════════════╬═════════════╬═════════════════════╣\n'
          '║  Weeping willow ║   Garage    ║    Abandonned camp  ║\n'
          '╠═════════════════╬═════════════╬═════════════════════╣\n'
          '║    Large Rocks  ║  Watchtower ║    Ranger house     ║\n'
          '╚═════════════════╩═════════════╩═════════════════════╝\n')

"""
    
DESCRIPTION = 'description'
EXAMINATION = 'examine'
OBJECTIVE = 'objective'
SOLVED = 'solved'
SIDE_UP = 'up'
SIDE_DOWN = 'down'
SIDE_LEFT = 'left'
SIDE_RIGHT = 'right'
ITEM = 'item'
FOUND_ITEM = 'found item sentence'

solved_places = {
                'Ranger truck': False, 'Tunnel': False, 'Rusted Tankers':False,
                'Weeping willow': False, 'Garage': False, 'Abandonned camp':False,
                'Large Rocks': False, 'Watchtower': False, 'Ranger House':False,
                }

game_map = {
          'Ranger truck': { 
                DESCRIPTION:"The Ranger truck! Maybe someone is in the area or maybe I could get away with this?\n",
                EXAMINATION: "Ok... Tires are dead, and it looks like there have been a fight here..\nBroken glass and footprints everywhere...\nWait... Is that blood?!\nI think I shouldn't stay there much longer...",
                OBJECTIVE: "...But maybe something in this car could help me? What should I do?\n",
                SOLVED: False,
                SIDE_UP: 'Large Rocks',
                SIDE_DOWN: 'Weeping willow',
                SIDE_LEFT: 'Rusted Tankers',
                SIDE_RIGHT: 'Tunnel',
                ITEM: 'Battery',
                FOUND_ITEM: "It seems fitting for the car... better be good.",
           },
          'Tunnel': { 
                DESCRIPTION: "You are now outdoor, facing a deep dark tunnel not really reassuring..\nIt's strange, because it looks like the wind is coming from it...\n",
                EXAMINATION: "You can hardly see anything.\nBut it seems like there would be some interesting stuffs in there...\n",
                OBJECTIVE: "Stop. something is watching you in the dark.\nIt's coming to you, and it doesn't look friendly. What are you going to do!?\n",
                SOLVED: False,
                SIDE_UP: 'Watchtower', 
                SIDE_DOWN: 'Garage',
                SIDE_LEFT: 'Ranger truck',
                SIDE_RIGHT: 'Rusted Tankers',
            },
          'Rusted Tankers': { 
                DESCRIPTION: " That place is a wasteland, with rusted tankers.\nLooks creepy as hell...\nI have a bad feeling about that place.\n",
                EXAMINATION: "Looks like nobody came here for a good while.\nNot really surprising, place has a real spooky vibe.",
                OBJECTIVE: "But maybe one of these tank has still some fuel in it? Should definitely check this out.",
                SOLVED: False,
                SIDE_UP: 'Ranger House',
                SIDE_DOWN: 'Abandonned camp',
                SIDE_LEFT: 'Tunnel',
                SIDE_RIGHT: 'Ranger truck',
                ITEM: 'Fuel',
                FOUND_ITEM: "Car had no more gas, so that's a  pretty good step forward.",
            },
          'Weeping willow': { 
                DESCRIPTION: "A big old tree. Looks like he's alive, I mean... Like a human being.\nThat place is really scary...\n",
                EXAMINATION: "Lookin' at it carefully, I can see something's shining at the base of the tree...\n",
                OBJECTIVE: "Yes, there's definitely something here,\nI should have a more closer look at it, could be useful.",
                SOLVED: False,
                SIDE_UP: 'Ranger truck',
                SIDE_DOWN: 'Large Rocks',
                SIDE_LEFT: 'Abandonned camp',
                SIDE_RIGHT: 'Garage',
                ITEM: 'Music Box',
                FOUND_ITEM: "A... Music box?\nMmh..There are some writing on it but... mostly unreadable.\nSeems like it was put here on purpose...\nWho would put that kind of objects here..?\nAnyway, it looks broken, I can't even open it.\n",
            },
          'Garage': { 
                DESCRIPTION: "That's a really cold, dark place...\nFloor is moist, slippery, and the smell is awful in there.\n",
                EXAMINATION: "There's absolutely nothing in this area, but you and an old car.\nSomething seems wrong with that place, I feel kind of observed..\n",
                OBJECTIVE: "No keys, battery looks dead, and probably no gas'...\nWe won't get far with that...\n",
                SOLVED: False,
                SIDE_UP: 'Tunnel',
                SIDE_DOWN: 'Watchtower',
                SIDE_LEFT: 'Weeping willow',
                SIDE_RIGHT: 'Abandonned camp',
            },
          'Abandonned camp': { 
                DESCRIPTION: "An Abandonned camp. Looks like there were people here, but everything has been left off.\nWhat the hell is wrong..?\n",
                EXAMINATION: "No one is here, but there are footprints everywhere has if the people tried to escape quickly from that place...\nCampers stuffs are spread everwyhere on the area...\n",
                OBJECTIVE: "Maybe I can have a look in all that mess to find something interesting.",
                SOLVED: False,
                SIDE_UP: 'Rusted Tankers',
                SIDE_DOWN: 'Ranger House',
                SIDE_LEFT: 'Garage',
                SIDE_RIGHT: 'Weeping willow',
                ITEM: 'Rope',
                FOUND_ITEM: "Mmh.. Everything was useless or unusable but I found this. Don't know if I can use this but, well...",
            },
          'Large Rocks': { 
                DESCRIPTION: "Large rocks in the middle of nowhere.\nCould be dangerous if I get lost...\n",
                EXAMINATION: "Nothing but a maze of huge rocks...\nI don't see what I could find in there but I can have a look.",
                OBJECTIVE: "Something was written on some of these rocks, but it's unreadable... There are a bunch of pieces of paper in the area too.",
                SOLVED: False,
                SIDE_UP: 'Weeping willow',
                SIDE_DOWN: 'Ranger truck',
                SIDE_LEFT: 'Ranger House',
                SIDE_RIGHT: 'Watchtower',
                ITEM: 'Girl picture',
                FOUND_ITEM: "An early teenage girl picture... Photo have been half torn, looks like she was next to someone."
            },
          'Watchtower': {
                DESCRIPTION: "A huge watchtower. Probably used by the ranger of the area. Looks abandoned.\n",
                EXAMINATION: "Ladders steps are broken here and there... Looks dangerous to get up there.\n",
                OBJECTIVE: "There's a bunch of objects & dirts here and there... Was that thrown intentionnaly or not? I May have a look.",
                SOLVED: False,
                SIDE_UP: 'Garage',
                SIDE_DOWN: 'Tunnel',
                SIDE_LEFT: 'Large Rocks',
                SIDE_RIGHT: 'Ranger House',
                ITEM: 'Phone',
                FOUND_ITEM: "Battery's dead... but it looks like it has been lost not so long ago."
            },
          'Ranger House': {
                DESCRIPTION: "Yes, the Ranger House! I can see lights through the windows, maybe I will finally find some help here!\nLet's find out.",
                EXAMINATION: "...Place is deserted. No one's in there...",
                OBJECTIVE: "I'll try looking for some objects, there's definitely something for me here.\n",
                SOLVED: False,
                SIDE_UP: 'Abandonned camp',
                SIDE_DOWN: 'Rusted Tankers',
                SIDE_LEFT: 'Watchtower',
                SIDE_RIGHT: 'Large Rocks',
                ITEM: 'Keys',
                FOUND_ITEM: "Looks like the car keys from that one in the garage!",
            }
} 


def title_screen_selections(): #Title screen selections
    option = input("> ")
    if option.lower() == ("play"):
        setup_game() # placeholder until written
    elif option.lower() == ("help"):
        help_menu()
    elif option.lower() == ("quit"):
        sys.exit()
    while option.lower() not in ['play', 'help', 'quit']:
        print("Please enter a valid command.")
        option = input("> ")
        if option.lower() == ("play"):
            setup_game()
        elif option.lower() == ("help"):
            help_menu()
        elif option.lower() == ("quit"):
            sys.exit()

def title_screen(): #Game Menu
    os.system('clear')
    print('###########################')
    print('# WELCOME TO THE TEXT RPG #')
    print('###########################')
    print('           PLAY            ')
    print('           HELP            ')
    print('           QUIT            ')
    title_screen_selections()

def help_menu(): #Help Menu
    print('###########################')
    print('# WELCOME TO THE TEXT RPG #')
    print('###########################')
    print(' Use "move", "walk", "travel", "go", "escape" or "run" to travel on the map')
    print(' Use "left", "right", "up", or "down" to choose your direction on the map')
    print(' Use "examine", "inspect" or "interact" to inspect something in the area')
    print(' Use "get item" to pick an item on the map')
    print(' Enjoy yourself! ;) ')
    title_screen_selections()

#GAME INTERACTIVITY#
def print_location(): #Prints the map when player moves
  print('\n' + ('#' * (4 +len(myPlayer.location)))) 
  print('# ' + myPlayer.location.upper() + ' #')  
  print('#' * (4 +len(myPlayer.location)))
  print('\n' + (game_map[myPlayer.location][DESCRIPTION])) 


def instructions(): #Takes player actions in count
  acceptable_actions = ['move', 'go', 'travel', 'walk', 'quit', 'inspect', 'examine', 'interact', 'look', 'search', 'search', 'escape', 'run', 'get item']
  print("\n" + "=============================" )  
  print("What would you like to do?")
  print("You can either 'move', 'examine' or 'get item'")
  action = input("> ") 
  while action.lower() not in acceptable_actions:
    print("That is not an acceptable action.\n") 
    action = input("> ")  
  if action.lower() == 'quit':
    sys.exit()  
  elif action.lower() in ['move', 'travel', 'go', 'walk', 'escape', 'run']:
    player_move(action.lower()) 
  elif action.lower() in ['inspect', 'examine', 'look']:
    player_examine(action.lower())
  elif action.lower() == 'get item':
    player_get_item()

def player_move(my_player_action): #Map travelling
  askString = "Where would you like to "+my_player_action+" to?\n> "
  destination = input(askString)  
  if destination == 'up':
    move_destination = game_map[myPlayer.location][SIDE_UP]  
    move_player(move_destination)  
  elif destination == 'down':
    move_destination = game_map[myPlayer.location][SIDE_DOWN]  
    move_player(move_destination)  
  elif destination == 'left':
    move_destination = game_map[myPlayer.location][SIDE_LEFT]  
    move_player(move_destination)  
  elif destination == 'right':
    move_destination = game_map[myPlayer.location][SIDE_RIGHT] 
    move_player(move_destination)  
  else:
    print("Invalid command, try using up, down, left, or right.\n")  
    player_move(my_player_action) 


def move_player(move_destination): #Tell the player where he is on the map upon travelling
  print("\nYou have moved to the "+move_destination+".")
  myPlayer.location = move_destination
  print_location()
  if myPlayer.location == 'Garage':
    trigger_endgame()

def player_examine(action): #Fonction examination
  if solved_places[myPlayer.location] == False:
    print((game_map[myPlayer.location][EXAMINATION]))
    print((game_map[myPlayer.location][OBJECTIVE]))
  else:
    print("You've nothing else to do here.")

def player_get_item(): #Used to get item in the player inventory
  current_map = game_map[myPlayer.location]
  if ITEM in current_map:
      if current_map[ITEM] in myPlayer.inventory:
        print("You already found the item named "+current_map[ITEM]+".")
      else:
        myPlayer.inventory.append(current_map[ITEM])
        print("You found the "+ current_map[ITEM] +".")
        print(current_map[FOUND_ITEM])
  else:
   print("There's no item here")

def trigger_endgame(): #If player comes back to the 'Garage', endgame is triggered
  found_items = 0
  required_items = ['Keys', 'Fuel', 'Battery', 'Music Box']
  for inventory_item in myPlayer.inventory:
    if inventory_item in required_items:
      found_items += 1
  if found_items == 3 and 'Music Box' not in myPlayer.inventory: #Sentence if the player doesn't have all the recquired items and then lose
    print("Yes, it seems like I have all the goods to restart the car!\nWait... Something's wrong. Someone is there.\n- 'Hey, Who's there!? Who are you, and what do you want from me?\nI just want to leave that place, please let me go!'\n...No answer. I can feel the temperature going lower, it's freezing in there...\n...Someone is definitely there, at the back of the room.\nI can see him getting closer in the dark.\nI can't move... Hardly breath...My body feel so numb.\nPlace is getting filled with some kind of mist... What's going on...?\nI see 'him' now. There's a ghostly presence just in front of me.\n\nHe's whispering continuously, but I can't hear that spectral voice of his.\nI'm petrified.\nI can see him lifting his arm toward me...\nHe's now pointing his index at me.\nI think that he is asking for something...But what..?\n")
    print("I can hear him much clearly now... He's sobbing deeply.\nHe's now approaching his hand and grabs my throat firmly.\n")
    print("As the seconds pass, I can feel a pressure in my chest and my mind leaving my body.\nI.. I'm passing out..\n")
    print("==========================================================")
    print("                        Game over                         ")
    print("==========================================================")
    
  elif found_items == 4 and 'Music Box' in myPlayer.inventory: #Sentence if the player has all the items recquired and win
    print("Yes, it seems like I have all the goods to restart the car!\nWait... Something's wrong. Someone is there.\n- 'Hey, Who's there!? Who are you, and what do you want from me? I just want to leave that place, please let me go!'\n...No answer. I can feel the temperature going lower, it's freezing in there...\n...Someone is definitely there, at the back of the room.\nI can see him getting closer in the dark.\nI can't move... Hardly breath...My body feel so numb.\nPlace is getting filled with some kind of mist... What's going on...?\nI see 'him' now. There's a ghostly presence just in front of me.\n\nHe's whispering continuously, but I can't hear that spectral voice of his.\nI'm petrified.\nI can see him lifting his arm toward me...\nHe's now pointing his index at me.\nI think that he is asking for something...But what..?\n")
    print("I can hear him mumbling much clearly now. It seems like he is... humming a song..?\n")
    print("Ye..Yeah! He's definitely humming some kind of tune...\n..I know! The Music Box! I think that's what he wants...\nBut how does he know?\n")
    print("I find the strength to get the object from my purse and hand it to him.\n")
    print("He takes it slowly from my hand, and the music box opens itself...\nA song is playing from it.\n")
    print("Somehow, that tune is remembering me something, but I doesn't come back to me.\n")
    print("After what seemd an eternity, music box closes itself.\nHaunting presence slowly retreats in the dark as I begin to finally get back the control of my whole body.\n")
    print("What a strange encounter. It was scary, but that ethereal experience makes me feel... relieved.\n")
    print("...I think it's time to finally leave that place for good.")
    print("==========================================================")
    print("       Congratulation, you escaped and won the game!       ")
    print("==========================================================")


#GAME FUNCTIONALITIES#
def main_game_loop(): # handles maps, examination of the places, getting items,  etc
  while myPlayer.game_won == False:
      instructions()

def setup_game():
  os.system('clear')

#COLLECT PLAYER NAME
  question1 = "Hey. What's your name, stranger?\n"
  for character in question1:
      sys.stdout.write(character)
      sys.stdout.flush()
      time.sleep(0.1)
  player_name = input("> ")
  myPlayer.name = player_name
    
#TOOL HANDLING (NOT USED IN GAME)
#  question2 = "Which object would you like to begin with?\nChoose wisely.\nOptions:\nflashlight\nknife\npaperclip"
#  player_tool = input("> ")
#  valid_tool = ['flashlight', 'knife', 'paperclip']
#  if player_tool.lower() == valid_tool:
#     myPlayer.tool = player_tool
#     print("You now have a " + player_tool + " on you.\n")
#  while player_tool.lower() not in valid_tool:
#      print("Please chose one of the proposed tools.")
#      player_tool = input("> ")

    # INTRODUCTION
  question2 = "Okay, so you are " +player_name+ ".\nNow let's begin.\n"
  for character in question2:
      sys.stdout.write(character)
      sys.stdout.flush()
      time.sleep(0.01)

  
  plot1 = "==========================================================\n"
  plot2 = "Whe..Where am I..?\nWow, my head hurts so much...\nIt's so cold in there, and I can barely see anything..\nI can't even remember where I was and what I was doing...\nHow the hell did I get here..?\n-Hey, is there anybody here?!?\nNo one's answering... Guess I will have to find myself what happened...\n"
  for character in plot1:
      sys.stdout.write(character)
      sys.stdout.flush()
      time.sleep(0.02)
  for character in plot2:
      sys.stdout.write(character)
      sys.stdout.flush()
      time.sleep(0.01)


  os.system('clear')
  print("")
  main_game_loop()
  
title_screen()