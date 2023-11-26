import time
import random
import math
from enum import Enum

class ItemSlots (Enum):
    HAND = 0
    HEAD = 1 
    CHEST = 2
    LEGS = 3
    FEET = 4

class Item:
    item_name = None
    item_slot = None
    item_atk = 0
    item_armor = 0
    item_crit_chance = 0
    item_poison = False
    item_life_steal = False
    
    def __init__(self, name, slot, atk, armor, crit, poison, life_steal):
        self.item_name = name
        self.item_slot = ItemSlots(slot)
        self.item_atk = atk
        self.item_armor = armor
        self.item_crit_chance = crit 
        self.item_poison = poison
        self.item_life_steal = life_steal

    def displayItem(self):
        print("Item name: ", self.item_name)
        print("Item slot: ", self.item_slot.name)
        if self.item_atk > 0:
            print(" +", self.item_atk, " atk") 
        elif self.item_atk < 0:
            print( " ",self.item_atk, " atk")
        if self.item_armor > 0:
            print(" +", self.item_armor, " armor")
        elif self.item_armor < 0:
            print(" ", self.item_armor, " armor")
        if self.item_crit_chance > 0:
            print(" +", self.item_crit_chance, " crit chance")
        elif self.item_crit_chance < 0:
            print(" ", self.item_crit_chance, " crit chance")
        if self.item_poison == True:
            print(" + Poison")
        if self.item_life_steal == True:
            print(" + Life Steal")

    def removeItem(self, player):
        player.creature_atk -= self.item_atk
        player.creature_armor -= self.item_armor
        player.creature_crit -= self.item_crit_chance
        if self.item_life_steal == True:
            player.creature_life_steal = False
        if self.item_poison == True:
            player.creature_applies_poison = False
        player.creature_equipment_slots[self.item_slot.value] = None
        print("Item '",self.item_name, "' removed!")

    def equipItem(self, player):
        if player.creature_equipment_slots[self.item_slot.value] != None:
            print("Item slot occupied! Error!")
            return
        player.creature_atk += self.item_atk
        player.creature_armor += self.item_armor
        player.creature_crit += self.item_crit_chance
        player.creature_applies_poison = self.item_poison
        player.creature_life_steal = self.item_life_steal 
        player.creature_equipment_slots[self.item_slot.value] = self
        
    def foundItem(self, player):
        print("You have found an item! Let's see...")
        print("Found item:")
        self.displayItem()
        print("Currently equipped:")
        if player.creature_equipment_slots[self.item_slot.value] != None:
            player.creature_equipment_slots[self.item_slot.value].displayItem()
        else:
            print("No item equipped.")
        pick_up_choice = input("Are you willing to take it? Y/N ")   
        while pick_up_choice.lower() not in ["y", "n"]:
            print("Invalid choice, try again.")
            pick_up_choice = input("Are you willing to take it? Y/N ")
        if pick_up_choice.lower() == "y":
            if player.creature_equipment_slots[self.item_slot.value] != None:
                player.creature_equipment_slots[self.item_slot.value].removeItem(player)
            self.equipItem(player)
        else:
            print("Item rejected.")

        
