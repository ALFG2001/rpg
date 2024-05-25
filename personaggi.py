from magia import *
from inventario import *
from random import randint, shuffle, choice

class Character(): # character
    def __init__(self) -> None:
        self.name = ""
        self.stats = {"HP":[1,1], "MANA":[1,1], "STR":1, "CON":1, "AGI":1, "INT":1}
        self.stats_base = {"HP":[1,1], "MANA":[1,1], "STR":1, "CON":1, "AGI":1, "INT":1}
        self.spells = []
        self.inventory = []
        self.drop = []
        self.dead = False
        self.gold = 0

    def printStats(self, num=0, enem=0):
        if num:
            print(f"{num} - {self.name}:")
        else:
            print(f"{self.name}:")
        if not enem:
            for k in self.stats:
                print(f"{k}: {self.stats[k]}")
        else:
            hp = self.stats["HP"][0]
            print(f"HP: {hp}")

    def dropItems(self):
        i = 2
        it = []
        for item in self.inventory:
            print(f"{i} - {item.name}")
            if isinstance(item, Equipment):
                item.equipped = False
            it.append(item)
            i += 1
        return it

    def reset(self):
        self.stats = self.stats_base

    def attack(self, target):
        if isinstance(self, Hero):
            STR_MULTIPLIER = 0.9
        else:
            STR_MULTIPLIER = 1.35
        CON_RESISTANCE = 0.75

        damage = max(0, (self.stats["STR"] * STR_MULTIPLIER) - (target.stats["CON"] * CON_RESISTANCE))
        damage = round(damage)
        
        print(f"{self.name} attacks {target.name} for {damage} damage")
        self.apply_damage(target, damage)

    def castSpell(self, spell:Spell, target):
        if self.stats["MANA"][0] < spell.cost:
            print(f"Not enough mana to cast {spell.name}")
            return

        self.stats["MANA"][0] -= spell.cost

        if isinstance(spell, Damaging):
            if isinstance(self, Hero):
                INT_MULTIPLIER = 0.75
            else:
                INT_MULTIPLIER = 1.1
            CON_RESISTANCE = 0.5
            
            damage = max(0, (spell.damage * self.stats["INT"] * INT_MULTIPLIER) - (target.stats["CON"] * CON_RESISTANCE))
            damage = round(damage)

            print(f"{self.name} casts {spell.name} on {target.name} for {damage} damage")
            self.apply_damage(target, damage)

        elif isinstance(spell, Healing):
            heal = spell.heal + self.stats["INT"]
            self.apply_healing(target, heal)
              
    def apply_damage(self, target, damage):
        target.stats["HP"][0] -= damage
        if target.stats["HP"][0] <= 0:
            target.stats["HP"][0] = 0
            target.dead = True
            print("-" * 60)
            print(f"{target.name} is dead!".center(60))

    def apply_healing(self, target, heal):
        if target.stats["HP"][0] + heal > target.stats["HP"][1]:
            heal = target.stats["HP"][1] - target.stats["HP"][0] 
            target.stats["HP"][0] = target.stats["HP"][1] 
        else:
            target.stats["HP"][0] += heal
        print(f"{self.name} heals {target.name} for {heal} HP")
        print(f"Current HP: {target.stats['HP'][0]}")

    def healPotion(self, item:Utility):
        for key in item.stats:
            if isinstance(self.stats[key], int):
                self.stats[key] += item.stats[key]
            else:
                diff = min(self.stats[key][1], self.stats[key][0] + item.stats[key])
                print("-"*60)
                print(f"{key} increased by {diff-self.stats[key][0]}")
                self.stats[key][0] =  diff
                print(f"Current {key}: {self.stats[key][0]}")
        self.inventory.remove(item)
                
    def harmPotion(self, item:Harmful, target):
        danno = item.damage
        print(f"{self.name} uses {item.name} on {target.name} for {danno} damage")
        target.stats["HP"][0] -= danno
        if target.stats["HP"][0] <= 0:
                target.stats["HP"][0] = 0
                target.dead = True
                print("-"*60)
                print(f"{target.name} is dead!".center(60))
        self.inventory.remove(item)

    def equip(self, item:Equipment):
        if not item.equipped:
            found = False
            for obj in self.inventory:
                if isinstance(obj, Equipment):
                    if isinstance(obj, item.__class__.__base__):
                        if isinstance(obj, item.__class__) and not found:
                            if obj.equipped:
                                obj.equipped = False
                                for key in item.stats:
                                    if isinstance(self.stats[key], int):
                                        self.stats[key] -= item.stats[key]
                                    else:
                                        self.stats[key][0] -= item.stats[key][0]
                                        self.stats[key][1] -= item.stats[key][1]
                            item.equipped = True
                            found = True
                            for key in item.stats:
                                if isinstance(self.stats[key], int):
                                    self.stats[key] += item.stats[key]
                                else:
                                    self.stats[key][0] += item.stats[key][0]
                                    self.stats[key][1] += item.stats[key][1]
        else:
            item.equipped = False
            for key in item.stats:
                if isinstance(self.stats[key], int):
                    self.stats[key] -= item.stats[key]
                else:
                    self.stats[key][0] -= item.stats[key][0]
                    self.stats[key][1] -= item.stats[key][1]

class Hero(Character):
    def __init__(self) -> None:
        super().__init__()
        self.level = 1
        self.name = "Hero"
        self.stats = {"LEVEL":self.level,
                      "HP":[20,20],
                      "MANA":[5,5], 
                      "STR":3,
                      "CON":3, 
                      "AGI":3,
                      "INT":3}
        self.stats_base = {"LEVEL":self.level,
                            "HP":[20,20],
                            "MANA":[5,5], 
                            "STR":3,
                            "CON":3, 
                            "AGI":3, 
                            "INT":3}
        self.spells = []
        self.inventory = []
        self.hasAttacked = False
        self.dead = False

    def levelUp(self):
        self.level += 1
        i = []
        for item in self.inventory:
            if isinstance(item, Equipment):
                if item.equipped:
                    i.append(item)
                    self.equip(item)
        self.stats = {"LEVEL":self.level,
                    "HP":[20+10*(self.level-1),20+10*(self.level-1)],
                    "MANA":[5+5*(self.level-1),5+5*(self.level-1)], 
                    "STR":3+(self.level-1)*2, 
                    "CON":3+(self.level-1)*1, 
                    "AGI":3+(self.level-1)*1, 
                    "INT":3+(self.level-1)*2   }
        self.stats_base = self.stats
        
        for item in i:
            if isinstance(item, Equipment):
                if not item.equipped:
                    self.equip(item)
        print("LEVEL UP!")
        print(f"{self.level-1} --> {self.level}")

        match self.level:
            case 2:
                self.spells.append(Smite())
                print("YOU UNLOCKED SMITE!")
                print("-"*60)
                           
class EnemyMob(Character): # enemy non boss
    def __init__(self) -> None:
        super().__init__()
    
    def __lt__(self, other): 
          return self.__class__ < other.__class__
    
class Slime(EnemyMob):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Slime"
        self.stats = {"HP":[8,8], "MANA":[0,0], "STR":3, "CON":2, "AGI":1, "INT":1}
        self.inventory = [SlimeGoo()]
        self.gold = 20

class GoblinHunter(EnemyMob):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Goblin Hunter"
        self.stats = {"HP":[15,15], "MANA":[0,0], "STR":6, "CON":5, "AGI":6, "INT":2}
        self.inventory = [GoblinEar()]
        self.gold = 30

class GoblinShaman(EnemyMob):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Goblin Shaman"
        self.stats = {"HP":[12,12], "MANA":[15,15], "STR":2, "CON":4, "AGI":3, "INT":5}
        self.inventory = [GoblinEar()]
        self.spells = [FireBolt(), LightningStrike()]
        self.gold = 30

class KoboldScout(EnemyMob):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Kobold Scout"
        self.stats = {"HP":[10,10], "MANA":[0,0], "STR":4, "CON":3, "AGI":6, "INT":2}
        self.inventory = [KoboldEar()]
        self.gold = 25

class KoboldWarrior(EnemyMob):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Kobold Warrior"
        self.stats = {"HP":[15,15], "MANA":[0,0], "STR":5, "CON":4, "AGI":4, "INT":2}
        self.inventory = [KoboldEar(), SmallShield()]
        self.gold = 30

class KoboldShaman(EnemyMob):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Kobold Shaman"
        self.stats = {"HP":[12,12], "MANA":[10,10], "STR":3, "CON":3, "AGI":3, "INT":5}
        self.spells = [FireBolt(), HealingLight()]
        self.inventory = [KoboldEar(), HealingHerb()]
        self.gold = 35

class OrcGrunt(EnemyMob):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Orc Grunt"
        self.stats = {"HP": [20, 20], "MANA": [0, 0], "STR": 8, "CON": 6, "AGI": 3, "INT": 2}
        self.inventory = [OrcTooth()]
        self.gold = 20

class OrcWarrior(EnemyMob):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Orc Warrior"
        self.stats = {"HP": [25, 25], "MANA": [0, 0], "STR": 10, "CON": 8, "AGI": 4, "INT": 3}
        #self.inventory = [OrcTooth(), SmallAxe()]
        self.gold = 25

class OrcShaman(EnemyMob):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Orc Shaman"
        self.stats = {"HP": [22, 22], "MANA": [20, 20], "STR": 5, "CON": 5, "AGI": 4, "INT": 7}
        self.spells = [FireBolt(), HealingLight()]
        self.inventory = [OrcTooth(), HealingHerb()]
        self.gold = 25

class OrcCommander(EnemyMob):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Orc Commander"
        self.stats = {"HP": [30, 30], "MANA": [10, 10], "STR": 12, "CON": 10, "AGI": 5, "INT": 4}
        #self.inventory = [OrcTooth(), CommandersHelmet()]
        self.gold = 30

class Imp(EnemyMob):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Imp"
        self.stats = {"HP": [10, 10], "MANA": [10, 10], "STR": 4, "CON": 3, "AGI": 6, "INT": 4}
        #self.inventory = [ImpClaw()]
        self.gold = 10

class LesserDemon(EnemyMob):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Lesser Demon"
        self.stats = {"HP": [20, 20], "MANA": [20, 20], "STR": 8, "CON": 6, "AGI": 5, "INT": 6}
        self.inventory = [DemonHorn()]
        self.gold = 20

class DemonWarrior(EnemyMob):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Demon Warrior"
        self.stats = {"HP": [25, 25], "MANA": [15, 15], "STR": 10, "CON": 8, "AGI": 6, "INT": 5}
        #self.inventory = [DemonHorn(), DemonSword()]
        self.gold = 25

class DemonMage(EnemyMob):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Demon Mage"
        self.stats = {"HP": [22, 22], "MANA": [30, 30], "STR": 5, "CON": 5, "AGI": 5, "INT": 9}
        self.spells = [DarkFlame(), ShadowBolt()]
        #self.inventory = [DemonHorn(), MagicGem()]
        self.gold = 25

class DemonGeneral(EnemyMob):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Demon General"
        self.stats = {"HP": [30, 30], "MANA": [20, 20], "STR": 12, "CON": 10, "AGI": 7, "INT": 7}
        #self.inventory = [DemonHorn(), GeneralArmor()]
        self.gold = 30

class DragonWhelp(EnemyMob):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Dragon Whelp"
        self.stats = {"HP": [30, 30], "MANA": [20, 20], "STR": 8, "CON": 6, "AGI": 4, "INT": 5}
        self.inventory = [DragonScale()]
        self.gold = 20

class DragonHatchling(EnemyMob):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Dragon Hatchling"
        self.stats = {"HP": [40, 40], "MANA": [30, 30], "STR": 10, "CON": 8, "AGI": 6, "INT": 6}
        #self.inventory = [DragonScale(), DragonClaw()]
        self.gold = 30

class YoungDragon(EnemyMob):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Young Dragon"
        self.stats = {"HP": [50, 50], "MANA": [40, 40], "STR": 12, "CON": 10, "AGI": 8, "INT": 7}
        #self.inventory = [DragonScale(), DragonClaw(), DragonTooth()]
        self.gold = 40

class DragonWarrior(EnemyMob):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Dragon Warrior"
        self.stats = {"HP": [60, 60], "MANA": [50, 50], "STR": 14, "CON": 12, "AGI": 9, "INT": 8}
        #self.inventory = [DragonScale(), DragonSword()]
        self.gold = 50

class ElderDragon(EnemyMob):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Elder Dragon"
        self.stats = {"HP": [80, 80], "MANA": [60, 60], "STR": 16, "CON": 14, "AGI": 10, "INT": 10}
        #self.inventory = [DragonScale(), DragonClaw(), DragonTooth()]
        self.gold = 60

class DragonGuardian(EnemyMob):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Dragon Guardian"
        self.stats = {"HP": [100, 100], "MANA": [80, 80], "STR": 18, "CON": 16, "AGI": 12, "INT": 12}
        #self.inventory = [DragonScale(), DragonClaw(), DragonTooth(), DragonShield()]
        self.gold = 70

class EnemyBoss(Character): # enemy boss
    def __init__(self) -> None:
        super().__init__()

class SlimeKing(EnemyBoss):
    def __init__(self) -> None:
        super().__init__()
        self.stats = {"NAME":"Slime King","HP":[40,40], "MANA":[5,5], "STR":6, "CON":3, "AGI":2, "INT":2}
        self.spells = [PoisonBall()]
        self.inventory = [SlimeGoo(), SlimeGoo(), SlimeGoo(), SlimeCrown()]
        self.gold = 100
        

    def divideSlime(self, ordine:list, indice:int):
        if self.dead:
            lista = summonEnemies(1, 3, False)
            ordine[indice:indice] = lista

class GoblinLord(EnemyBoss):
    def __init__(self) -> None:
        super().__init__()
        self.stats = {"NAME":"Goblin Lord","HP":[50,50], "MANA":[0,0], "STR":6, "CON":4, "AGI":5, "INT":6}
        self.inventory = [GoblinEar(), GoblinEar(), GoblinRing()]
        self.bers = False
        self.gold = 100

    def berserker(self):
        self.dead = False
        self.bers = True
        self.stats["HP"] = [50,50]
        self.stats["STR"] += 15
        self.stats["CON"] += 15

class KoboldHighShaman(EnemyBoss):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Kobold High Shaman"
        self.stats = {"HP": [60, 60], "MANA": [30, 30], "STR": 4, "CON": 5, "AGI": 4, "INT": 8}
        self.spells = [FireBolt(), LightningStrike()]
        self.inventory = [KoboldEar(), KoboldAmulet(), HealingHerb(), MagicScroll()]
        self.gold = 150

    def sacrificeAllies(self, allies):
        if self.dead and allies:
            for ally in allies:
                if not ally.dead:
                    self.stats["HP"][0] = self.stats["HP"][1] // 2  # revive with half HP
                    ally.dead = True
                    print(f"{ally.name} has been sacrificed!".center(60))
                    self.dead = False
                    break

class OrcWarlord(EnemyBoss):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Orc Warlord"
        self.stats = {"HP": [80, 80], "MANA": [10, 10], "STR": 15, "CON": 12, "AGI": 6, "INT": 3}
        self.inventory = [OrcTooth(), WarlordShield()]
        self.gold = 200

    def warCry(self, allies):
        if not self.dead:
            for ally in allies:
                ally.stats["STR"] += 2
                ally.stats["CON"] += 2

class DemonPrince(EnemyBoss):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Demon Prince"
        self.stats = {"HP": [100, 100], "MANA": [50, 50], "STR": 18, "CON": 14, "AGI": 8, "INT": 10}
        self.spells = [DarkFlame(), ShadowBolt()]
        self.inventory = [DemonHorn(), InfernalRobe(), DarkGem()]
        self.gold = 300
        self.buffsleft = 3

    def infernalRage(self):
        self.buffsleft -= 1
        if not self.dead:
            self.stats["STR"] += 5
            self.stats["INT"] += 5

class DragonTyrant(EnemyBoss):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Dragon Tyrant"
        self.stats = {"HP": [150, 150], "MANA": [80, 80], "STR": 20, "CON": 18, "AGI": 10, "INT": 12}
        self.spells = [FireBreath()]
        self.inventory = [DragonScale(), DragonClaws(), DragonHeart()]
        self.gold = 500
        self.roarCounter = 1

    def dragonRoar(self, enemy):
        if not self.dead:
                enemy.stats["STR"] -= 2
                enemy.stats["CON"] -= 2
                enemy.stats["AGI"] -= 2
                enemy.stats["INT"] -= 2
                self.roarCounter += 1

class DarkLord(EnemyBoss):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Dark Lord"
        self.stats = {"HP": [200, 200], "MANA": [100, 100], "STR": 25, "CON": 20, "AGI": 12, "INT": 15}
        self.spells = [DeathCurse(), SoulDrain()]
        self.inventory = [DarkLordCrown()]


    def darkNova(self, enemies):
        if not self.dead:
            for enemy in enemies:
                enemy.stats["HP"][0] -= 20  # Deal flat damage to all mobs
                if enemy.dead:
                    self.stats["HP"][0] = min(self.stats["HP"][1], self.stats["HP"][0]+10)
                    self.stats["STR"] += 2
                    self.stats["CON"] += 2
                    self.stats["AGI"] += 2
                    self.stats["INT"] += 2

def dungeon(num:int) -> list:
    match num:
        case 1:
            tipoNemici_0 = 0
            tipoNemici_1 = 1
            tipoBoss_0 = 0
            tipoBoss_1 = 1
        case 2:
            tipoNemici_0 = 1
            tipoNemici_1 = 3
            tipoBoss_0 = 1
            tipoBoss_1 = 2   
        case 3:
            tipoNemici_0 = 3
            tipoNemici_1 = 6
            tipoBoss_0 = 2
            tipoBoss_1 = 3   
        case 4:
            tipoNemici_0 = 6
            tipoNemici_1 = 10
            tipoBoss_0 = 3
            tipoBoss_1 = 4   
        case 5:
            tipoNemici_0 = 10
            tipoNemici_1 = 15
            tipoBoss_0 = 4
            tipoBoss_1 = 5   
        case 6:
            tipoNemici_0 = 15
            tipoNemici_1 = 21
            tipoBoss_0 = 5
            tipoBoss_1 = 6
        case 7:
            tipoNemici_0 = 0
            tipoNemici_1 = 21
            tipoBoss_0 = 0
            tipoBoss_1 = 21 

    return [tipoNemici_0,tipoNemici_1,tipoBoss_0,tipoBoss_1]

def divideNumber(numeroTarget:int, quantiNumeri:int) -> list:
    divided_numbers = []

    for _ in range(quantiNumeri - 1):
        random_number = randint(0, numeroTarget)
        divided_numbers.append(random_number)
        numeroTarget -= random_number
    divided_numbers.append(numeroTarget)
    shuffle(divided_numbers)
    
    return divided_numbers

def summonEnemies(numeroStage:int, quanti:int, boss:bool) -> list:
    nomi = {}
    nemici = []
    i = dungeon(numeroStage)

    quante_classi = i[3]
    
    subclasses_mob = EnemyMob.__subclasses__()[i[0]: i[1]]
    subclasses_boss = EnemyBoss.__subclasses__()[i[2]: i[3]][0]
    if boss:
        quanti -= 1
        nomi[subclasses_boss]=1
    numeri = divideNumber(quanti, quante_classi)
    shuffle(subclasses_mob)

    for ind in range(len(subclasses_mob)):
        nomi[subclasses_mob[ind]]=numeri[ind]

    for k in nomi:
        lettera = 65

        for _ in range(nomi[k]):
            e = k()
            e.name = k.__name__

            if nomi[k] > 1:
                e.name += " "+chr(lettera)
                lettera += 1

            # possibile passiva ultimo boss
            if numeroStage == 7:  
                e.stats["HP"][0] *= 10
                e.stats["HP"][1] *= 10

            nemici.append(e)

    agi = "AGI"
    nemici.sort(key=lambda character: character.stats[agi], reverse=True)
    for n in nemici:
        for item in n.inventory:
            if isinstance(item, Equipment):
                n.equip(item)
        print(f"{n.name} appears!")
    return nemici