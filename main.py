import time
import random
import math
from Creature import Creature
from Item import Item      
from Item import ItemSlots

EXP_CAP = 100
EXP_MIN = 20
EXP_MAX = 30

########### functions ##################################################################################################
def combat(enemy):
    global player
    player.creature_is_escaping = False
    while player.creature_curHP > 0 and enemy.creature_curHP > 0:
        player.displayCombatOptions(enemy)
        if player.creature_is_escaping == True:
            return
        if enemy.creature_curHP == 0:
            break
        enemy.attack(player)
    if player.creature_curHP > 0:
        player.gainEXP()
    else:
        print("GAME OVER!")
        exit()

def room_wishing_fontaine():
        fontaine = input("You find a wishing fountain! Do you wish to restore health? Y/N\n")
        if fontaine.lower() == "y":
            player.creature_maxHP += 10
            print("Your HP points have risen. ")
        else:
            print("You forgot about the fountain and just continued on your journey...")

def room_dead_soldier():
        print("You found a body of a dead soldier; he must have been here before you. You decided to take his weapon and progress on your journey.")
        Rusty_Sword = Item("Rusty Sword", ItemSlots(0), 10, 0, 0 , False, False)
        Rusty_Sword.foundItem(player)

def encounter_enemy(enemy_name, enemy_curhp, enemy_atk, enemy_crit, enemy_armor, enemy_hit):
        enemy = Creature(enemy_name, enemy_curhp, enemy_atk, enemy_crit, enemy_armor, enemy_hit)
        enemy_choice = input("You encountered a wild enemy! Do you wish to fight him or escape? F/E \n")
        while enemy_choice.lower() not in ["f", "e"]:
            print("Invalid choice! try again...")
            enemy_choice = input("You encountered a wild enemy! Do you wish to fight him or escape? F/E \n")
        if enemy_choice.lower() == "f":
            print("You chose to fight.")
            combat(enemy)
        elif enemy_choice.lower() == "e":
            roll = random.randint(1, 20)
            if roll >= 10:
                print("You have successfully escaped!")
            else:
                print("You have failed to escape...")
                time.sleep(1)
                combat(enemy)

     
####### MAIN CODE

name_confirm =""
while name_confirm != "Y" and name_confirm != "y":
    char_name = input("Your name: ")
    name_confirm = input("Are you sure? This cant be changed in the future (Y/N) ")

class_choice = ""
char_class = ""

while class_choice != "1" and class_choice != "2" and class_choice != "3":
    print("Availble classes: ")
    print("1. Archer")
    print("2. Warrior")
    print("3. Assasin")
    class_choice = input("Wpisz numer wybranej klasy:")
    match class_choice:
        case "1":
            char_class = "Archer"
            player = Creature(char_name, 80, 30, 20, 3, 95)                
        case "2":
            char_class = "Warrior"
            player = Creature(char_name, 110, 20, 10, 5, 93)
        case "3":
            char_class = "Assasin"
            player = Creature(char_name, 70, 40, 30, 2, 100)
        case _:
            print("Choice incorrect, try again \n")


print("Your class is: \t", char_class)
player.printStat()
time.sleep(1)

print("...A story about a greedy person, their name was ", char_name, " ,they were so greedy that they decided to save a princess from a dungeon just because the king himself offered huge money for it, but what will they come across? what really will happen on their journey is unknown... ")
time.sleep(2)

dun_choice = input("You enter a dungeon, what will you do? turn left, right, or just go straight forward? L/R/F\n" )
while dun_choice.lower() not in ["l", "r", "f"]:
    print("Invalid choice, please try again")
    dun_choice = input("You enter a dungeon, what will you do? turn left, right, or just go straight forward? L/R/F\n" )
if dun_choice.lower() == "r":
    encounter_enemy("slime", 50, 10, 2, 10, 90)
elif dun_choice.lower() == "l":
    room_wishing_fontaine()
elif dun_choice.lower() == "f":
    room_dead_soldier()

print("You find yourself within the darkness almost as dark as the void, you feel as if you were consumed by the dungeon by now, just then you stumble across a giant monster that blocks your path.")
print("You're forced to fight the monster")
Minotaur = Creature("Minotaur", 150, 5, 10, 10, 90)
combat(Minotaur)
Poisonus_Sword = Item("Poisonus Sword", ItemSlots.HAND, 10, 0, 0, True, False)
Poisonus_Sword.foundItem(player)
dun_choice_2 = input("The dungeon expands... there are two ways, which do you choose? Left or Right? L/R ")
while dun_choice_2.lower() not in ["l", "r"]:
    print("Invalid choice, please try again")
    dun_choice_2 = input("The dungeon expands... there are two ways, which do you choose? Left or Right? L/R ")
if dun_choice_2.lower() == "l":
    print("You fell into a trap! you loose 10 hp... ")
    player.creature_curHP -= 10
elif dun_choice_2.lower() == "r":
    encounter_enemy("skeleton", 50, 9, 10, 0, 91)

dun_choice_3 = input("The dungeon goes even further and the way splits once again, you can go either left front or right L/F/R")
while dun_choice_3.lower() not in ["l", "r", "f"]:
    print("Invalid choice, please try again")
    dun_choice = input("The dungeon goes even further and the way splits once again, you can go either left front or right L/F/R\n" )
if dun_choice_3.lower() == "r":
    encounter_enemy("Troll", 60, 10, 2, 10, 93)
elif dun_choice_3.lower() == "l":
    Vampire_Sword = Item("Vampire Sword", ItemSlots.HAND, 10, 0, 10, False, True)
    Vampire_Sword.foundItem(player)
elif dun_choice_3.lower() == "f":
    encounter_enemy("Hobgoblin", 50, 6, 10, 3, 93)
print("As you go even further you find a Giants Belt laying on the ground, you decide to take it because why not! \n +30 max hp")
player.creature_maxHP += 30
player.heal(30)
dun_choice_4 = input("guess what, the dungeon expands once again, L/R/F?")
while dun_choice_4.lower() not in [ "l", "r", "f"]:
    print("Invalid choice, please try again!")
    dun_choice_4 = input("guess what, the dungeon expands once again, L/R/F?")
if dun_choice_4.lower() == "l":
    print("You stumble across three wild slimes!")
    encounter_enemy("Slime 1", 30, 1, 1, 1, 90)
    encounter_enemy("Slime 2", 30, 1, 1, 1, 90)
    encounter_enemy("Slime 3", 30, 1, 1, 1, 90)
elif dun_choice_4.lower() == "r":
    room_dead_soldier()
elif dun_choice_4.lower == "f":
    room_wishing_fontaine()
print("Finally the ultimate enemy youve been waiting for... okay maybe not quite but now you gotta fight him theres no turning back")
boss = Creature("THE BOSS", 300, 15, 10, 10, 80)
combat(boss)
print("Ha! you thought! nah its not the end duh its not even half of the game yet! you continue on your journey...")
dun_choice_5 = input("there you go the dungeon again... tho there are no ways there is just a wishing fontaine-")
room_wishing_fontaine()
print("You found an armor... i mean it looks okay- you decided to wear it!")
iron_chestplate = Item("Iron Chestplate", 3, ItemSlots(2), 15, 0, False, False)
real_boss = Creature("THE REAL BOSS", 500, 60, 10, 10, 85)
print("now... now it is time... for ", real_boss.creature_name, "!!  ")
combat(real_boss)
print("yeah.... YOU WON!\n i think...")


