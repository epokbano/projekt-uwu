import time
import random
import math
from Item import Item


EXP_CAP = 100
EXP_MIN = 40
EXP_MAX = 60
POISON_CHANCE = 0
LIFE_STEAL_MULTI = 0.25
POISON_DMG = 5
POISON_REMOVE_CHANCE = 40
CRIT_MULTI = 1.5
HEAVY_HIT_MULTI = 3
HEAVY_HIT_CHANCE_MULTI = 0.7  
MULTI_HIT_DMG = 0.5
MULIT_HIT_CHANCE = 0.9
RUN_CHANCE = 30

########### CLASSES ###################################################################################################
class Creature:
    creature_name = None
    creature_maxHP = None
    creature_curHP = None
    creature_atk = None
    creature_crit = None
    creature_armor = None
    creature_hit = None
    creature_lvl = 1
    creature_exp = 0
    creature_is_poisoned = False
    creature_applies_poison = False    
    creature_life_steal = False
    creature_is_escaping = False
    creature_equipment_slots = [None, None, None, None, None] 




    def __init__(self, name, HP, atk, crit, armor, hit):
        self.creature_name = name
        self.creature_maxHP = HP
        self.creature_curHP = HP
        self.creature_atk = atk
        self.creature_crit = crit
        self.creature_armor = armor
        self.creature_hit = hit

    def printStat(self):
        print("Status of:\t", self.creature_name)
        print("Level:\t\t", self.creature_lvl )
        print("EXP:\t\t", self.creature_exp, "/", EXP_CAP)
        print("HP:\t\t", self.creature_curHP, "/", self.creature_maxHP)
        print("Atk:\t\t", self.creature_atk)
        print("Hit chance:\t", self.creature_hit)
        print("Crit. chance:\t", self.creature_crit)
        print("Armor:\t\t", self.creature_armor)

    def gainEXP(self):
        roll = random.randint(EXP_MIN, EXP_MAX)
        print("You have gained ", roll, " experience points!")
        self.creature_exp += roll
        if self.creature_exp >= EXP_CAP:
            self.levelUp()
            
    def levelUp(self):
        self.creature_lvl += 1
        self.creature_exp -= EXP_CAP
        print("LEVEL UP! Current level is: ", self.creature_lvl)
        self.creature_maxHP += 10
        self.creature_atk += 5
        self.creature_armor += 1
        if self.creature_lvl % 5 == 0:
            self.creature_crit += 5
    
    def receiveDMG(self, dmg):
        if dmg > self.creature_curHP:
            print(self.creature_name, " has received ", self.creature_curHP, " damage.")
            self.creature_curHP = 0
        else:
            print(self.creature_name, " has received ", int(dmg), " damage.")
            self.creature_curHP -= math.ceil(dmg)

    def inflictPoison(self, enemy):
        if self.creature_applies_poison == True:
            roll = random.randint(1,100)
            if roll <= POISON_CHANCE:
                print(enemy.creature_name, " has been poisoned!")
                enemy.creature_is_poisoned = True
    
    def dealPoisonDamage(self):
        if self.creature_is_poisoned == True:
            self.creature_curHP -= POISON_DMG
            print(self.creature_name, " lost ", POISON_DMG, " due to poison!")
            roll = random.randint(1,100)
            if roll <= POISON_REMOVE_CHANCE:
                print("Poison has ended!")
                self.creature_is_poisoned = False

    def heal(self, recoverHP):
        diff = self.creature_maxHP - self.creature_curHP
        if diff >= recoverHP:
            self.creature_curHP += recoverHP
            print (self.creature_name, " healed ", recoverHP, " HP points. Current HP: ", self.creature_curHP)
        else:
            self.creature_curHP += diff
            print (self.creature_name, " healed ", diff, "(out of", self.creature_maxHP, ") HP points. Current HP: ", self.creature_curHP)
        if self.creature_curHP > self.creature_maxHP:
            self.creature_curHP = self.creature_maxHP
        
    def lifeSteal(self, final_dmg):
        if self.creature_life_steal == True:
            life_stolen = math.ceil(final_dmg * LIFE_STEAL_MULTI)
            print("Stealing life!")
            self.heal(life_stolen)

    def attack (self, enemy):
        roll = random.randint(1,100)
        if roll > self.creature_hit:
            print(self.creature_name ," missed the attack!")
        else:
            self.inflictPoison(enemy)
            if roll <= self.creature_crit: 
                print(self.creature_name, " attacks!")
                print("CRITICAL HIT!")                
                final_dmg = self.creature_atk * CRIT_MULTI - enemy.creature_armor
                if final_dmg < 0: 
                    final_dmg = 1
                enemy.receiveDMG(final_dmg)
                self.lifeSteal(final_dmg)
                print(enemy.creature_name, " has ", enemy.creature_curHP, "/", enemy.creature_maxHP, " HP")
            else:
                print(self.creature_name, " attacks!")
                final_dmg = self.creature_atk - enemy.creature_armor
                if final_dmg < 0: 
                    final_dmg = 1
                enemy.receiveDMG(final_dmg)
                self.lifeSteal(final_dmg)
                print(enemy.creature_name, " has ", enemy.creature_curHP, "/", enemy.creature_maxHP, " HP")
        self.dealPoisonDamage()
        if enemy.creature_curHP <= 0:
            print(enemy.creature_name, " has died!")

    def heavyAttack (self, enemy):
        roll = random.randint(1,100)
        if roll > (self.creature_hit * HEAVY_HIT_CHANCE_MULTI) :
            print(self.creature_name ," missed the attack!")
        else:
            self.inflictPoison(enemy)
            if roll <= self.creature_crit: 
                print(self.creature_name, " attacks!")
                print("CRITICAL HIT!")
                final_dmg = self.creature_atk * HEAVY_HIT_MULTI * CRIT_MULTI - enemy.creature_armor
                if final_dmg < 0:  
                    final_dmg = 1
                enemy.receiveDMG(final_dmg)
                self.lifeSteal(final_dmg)
                print(enemy.creature_name, " has ", enemy.creature_curHP, "/", enemy.creature_maxHP, " HP")
            else:
                print(self.creature_name, " attacks!")
                final_dmg = self.creature_atk * HEAVY_HIT_MULTI - enemy.creature_armor
                if final_dmg < 0: 
                    final_dmg = 1
                enemy.receiveDMG(final_dmg)
                self.lifeSteal(final_dmg)
                print(enemy.creature_name, " has ", enemy.creature_curHP, "/", enemy.creature_maxHP, " HP")
        self.dealPoisonDamage()
        if enemy.creature_curHP <= 0:
            print(enemy.creature_name, " has died!")
    def multiHit (self, enemy):
        roll = random.randint(1,100)
        if roll > (self.creature_hit * MULIT_HIT_CHANCE) :
            print(self.creature_name ," missed the attack!")
        else:
            self.inflictPoison(enemy)
            if roll <= self.creature_crit: 
                print(self.creature_name, " attacks!")
                print("CRITICAL HIT!")
                final_dmg = self.creature_atk * MULTI_HIT_DMG * CRIT_MULTI - enemy.creature_armor
                if final_dmg < 0:  
                    final_dmg = 1
                enemy.receiveDMG(final_dmg)
                self.lifeSteal(final_dmg)
                print(enemy.creature_name, " has ", enemy.creature_curHP, "/", enemy.creature_maxHP, " HP")
            else:
                print(self.creature_name, " attacks!")
                final_dmg = self.creature_atk * MULTI_HIT_DMG - enemy.creature_armor
                if final_dmg < 0: 
                    final_dmg = 1
                enemy.receiveDMG(final_dmg)
                self.lifeSteal(final_dmg)
                print(enemy.creature_name, " has ", enemy.creature_curHP, "/", enemy.creature_maxHP, " HP")
        self.dealPoisonDamage()
        if enemy.creature_curHP <= 0:
            print(enemy.creature_name, " has died!")
        if roll > (self.creature_hit * MULIT_HIT_CHANCE) :
            print(self.creature_name ," missed the attack!")
        else:
            self.inflictPoison(enemy)
            if roll <= self.creature_crit: 
                print(self.creature_name, " attacks!")
                print("CRITICAL HIT!")
                final_dmg = self.creature_atk * MULTI_HIT_DMG * CRIT_MULTI - enemy.creature_armor
                if final_dmg < 0:  
                    final_dmg = 1
                enemy.receiveDMG(final_dmg)
                self.lifeSteal(final_dmg)
                print(enemy.creature_name, " has ", enemy.creature_curHP, "/", enemy.creature_maxHP, " HP")
            else:
                print(self.creature_name, " attacks!")
                final_dmg = self.creature_atk * MULTI_HIT_DMG - enemy.creature_armor
                if final_dmg < 0: 
                    final_dmg = 1
                enemy.receiveDMG(final_dmg)
                self.lifeSteal(final_dmg)
                print(enemy.creature_name, " has ", enemy.creature_curHP, "/", enemy.creature_maxHP, " HP")
        self.dealPoisonDamage()
        if enemy.creature_curHP <= 0:
            print(enemy.creature_name, " has died!")
        if roll > (self.creature_hit * MULIT_HIT_CHANCE) :
            print(self.creature_name ," missed the attack!")
        else:
            self.inflictPoison(enemy)
            if roll <= self.creature_crit: 
                print(self.creature_name, " attacks!")
                print("CRITICAL HIT!")
                final_dmg = self.creature_atk * MULTI_HIT_DMG * CRIT_MULTI - enemy.creature_armor
                if final_dmg < 0:  
                    final_dmg = 1
                enemy.receiveDMG(final_dmg)
                self.lifeSteal(final_dmg)
                print(enemy.creature_name, " has ", enemy.creature_curHP, "/", enemy.creature_maxHP, " HP")
            else:
                print(self.creature_name, " attacks!")
                final_dmg = self.creature_atk * MULTI_HIT_DMG - enemy.creature_armor
                if final_dmg < 0: 
                    final_dmg = 1
                enemy.receiveDMG(final_dmg)
                self.lifeSteal(final_dmg)
                print(enemy.creature_name, " has ", enemy.creature_curHP, "/", enemy.creature_maxHP, " HP")
        self.dealPoisonDamage()
        if enemy.creature_curHP <= 0:
            print(enemy.creature_name, " has died!")
        

    def displayCombatOptions(self, enemy):
        print("1. Normal attack")
        print("2. Heavy attack")
        print("3. Multi Attack")
        print("4. Run (", RUN_CHANCE, "%)")
        choice = input()
        while choice not in ["1", "2", "3", "4"]:
            print("Invalid input, please try again")
            choice = input()
        if choice == "1":
            self.attack(enemy)
        elif choice == "2":
            self.heavyAttack(enemy)
        elif choice == "3":
            self.multiHit(enemy)
        else:
            roll = random.randint(1,100)
            if roll > RUN_CHANCE:
                print(self.creature_name, " has failed to escape, skipping attack")
            else:
                print(self.creature_name," has succsesfuly escaped!")
                self.creature_is_escaping = True
    
