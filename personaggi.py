from magia import *
from inventario import *
from random import randint, shuffle, choice

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
        print(f"{n.name} appears!")
    return nemici

def checkDead(lista:list) -> list:
    for p in lista:
        if p.dead:
            lista.pop(lista.index(p))
    return lista

def checkItem(item:Item):
    print(f"{item.name}:")
    print(f"COSTO: {item.cost}")
    if isinstance(item, Equipment):
        for stat in item.stats:
            if item.stats[stat]:
                print(f"{stat}: +{item.stats[stat]}")

def checkSpell(spell:Spell, caster):
    print(f"{spell.name}:")
    print(f"COST: {spell.cost}")
    int = "INT"
    print(f"DAMAGE: {spell.damage*caster.stats[int]}")

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
            it.append(item)
        return it

    def reset(self):
        self.stats = self.stats_base

    def attack(self, target):
        dannoMax = self.stats["STR"]
        resist = target.stats["CON"]
        danno = dannoMax - round(resist**0.5) # forse
        nomeS, nomeT = self.name, target.name
        print(f"{nomeS} attacks {nomeT} for {danno} damage")
        target.stats["HP"][0] -= danno
        if target.stats["HP"][0] <= 0:
            target.stats["HP"][0] = 0
            target.dead = True
            print("-"*60)
            print(f"{nomeT} is dead!".center(60))

    def castSpell(self, spell:Spell, target):
            self.stats["MANA"][0] -= spell.cost
            dannoMax = spell.damage * self.stats["INT"]
            resist = target.stats["CON"]
            danno = dannoMax - round(resist**0.3) #forse
            nomeS, nomeT = self.name, target.name
            print(f"{nomeS} casts {spell.name} on {nomeT} for {danno} damage")
            target.stats["HP"][0] -= danno
            if target.stats["HP"][0] <= 0:
                target.stats["HP"][0] = 0
                target.dead = True
                print("-"*60)
                print(f"{nomeT} is dead!".center(60))
    
    def healPotion(self, item:Utility):
        for key in item.stats:
            diff = 0, ""
            if isinstance(self.stats[key], int):
                self.stats[key] += item.stats[key]
                diff = item.stats[key], key
            else:
                if self.stats[key][0] + item.stats[key] > self.stats[key][1]:
                     diff = (self.stats[key][1] + item.stats[key]) - (self.stats[key][0] + item.stats[key]), key
                     self.stats[key][0] =  self.stats[key][1]
                else:
                    diff = item.stats[key], key
                    self.stats[key][0] += item.stats[key]
                
            print(f"{self.name} gained {diff[0]} {diff[1]}")
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

class Hero(Character):
    def __init__(self) -> None:
        super().__init__()
        self.level = 1
        self.name = "Hero"
        self.stats = {"LEVEL":self.level,
                      "HP":[10,10],
                      "MANA":[5,5], 
                      "STR":10,
                      "CON":10, 
                      "AGI":10,
                      "INT":10}
        self.stats_base = {"LEVEL":self.level,
                            "HP":[10,10],
                            "MANA":[5,5], 
                            "STR":10,
                            "CON":10, 
                            "AGI":10, 
                            "INT":10}
        self.spells = []
        self.inventory = []
        self.hasAttacked = False
        self.dead = False

    def levelUp(self):
        stat_increase = 1.265
        self.level += 1
        i = []
        for item in self.inventory:
            if isinstance(item, Equipment):
                if item.equipped:
                    i.append(item)
                    self.equip(item)
        self.stats = {"LEVEL":self.level,
                    "HP":[10+10*(self.level-1),10+10*(self.level-1)],
                    "MANA":[5+5*(self.level-1),5+5*(self.level-1)], 
                    "STR":10+round((self.level-1)**stat_increase), 
                    "CON":10+round((self.level-1)**stat_increase), 
                    "AGI":10+round((self.level-1)**stat_increase), 
                    "INT":10+round((self.level-1)**stat_increase)   }
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
        
    def equip(self, item:Equipment):
        if not item.equipped:
            item.equipped = True
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
                    
class EnemyMob(Character): # enemy non boss
    
    def __init__(self) -> None:
        super().__init__()
    
    def __lt__(self, other): 
          return self.__class__ < other.__class__
    
class Slime(EnemyMob):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Slime"
        self.stats = {"HP":[8,8], "MANA":[0,0], "STR":5, "CON":5, "AGI":2, "INT":2}
        self.inventory = [SlimeGoo()]
        self.gold = 20

class GoblinHunter(EnemyMob):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Goblin Hunter"
        self.stats = {"HP":[20,20], "MANA":[0,0], "STR":15, "CON":10, "AGI":10, "INT":2}
        self.inventory = [GoblinEar()]
        self.gold = 30

class GoblinShaman(EnemyMob):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Goblin Shaman"
        self.stats = {"HP":[15,15], "MANA":[25,25], "STR":5, "CON":5, "AGI":5, "INT":5}
        self.inventory = [GoblinEar()]
        self.spells = [FireBolt(), LightingStrike()]
        self.gold = 30

"""
class Kobold1(EnemyMob):
    def __init__(self) -> None:
        super().__init__()

class Kobold2(EnemyMob):
    def __init__(self) -> None:
        super().__init__()

class Kobold3(EnemyMob):
    def __init__(self) -> None:
        super().__init__()

class Orc1(EnemyMob):
    def __init__(self) -> None:
        super().__init__()

class Orc2(EnemyMob):
    def __init__(self) -> None:
        super().__init__()

class Orc3(EnemyMob):
    def __init__(self) -> None:
        super().__init__()

class Orc4(EnemyMob):
    def __init__(self) -> None:
        super().__init__()

class Demon1(EnemyMob):
    def __init__(self) -> None:
        super().__init__()

class Demon2(EnemyMob):
    def __init__(self) -> None:
        super().__init__()

class Demon3(EnemyMob):
    def __init__(self) -> None:
        super().__init__()

class Demon4(EnemyMob):
    def __init__(self) -> None:
        super().__init__()

class Demon5(EnemyMob):
    def __init__(self) -> None:
        super().__init__()

class Dragon1(EnemyMob):
    def __init__(self) -> None:
        super().__init__()

class Dragon2(EnemyMob):
    def __init__(self) -> None:
        super().__init__()

class Dragon3(EnemyMob):
    def __init__(self) -> None:
        super().__init__()

class Dragon4(EnemyMob):
    def __init__(self) -> None:
        super().__init__()

class Dragon5(EnemyMob):
    def __init__(self) -> None:
        super().__init__()

class Dragon6(EnemyMob):
    def __init__(self) -> None:
        super().__init__()
"""

class EnemyBoss(Character): # enemy boss
    def __init__(self) -> None:
        super().__init__()

class SlimeKing(EnemyBoss):
    def __init__(self) -> None:
        super().__init__()
        self.stats = {"NAME":"Slime King","HP":[25,25], "MANA":[5,5], "STR":10, "CON":10, "AGI":5, "INT":2}
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
        self.stats = {"NAME":"Slime King","HP":[30,30], "MANA":[0,0], "STR":20, "CON":20, "AGI":15, "INT":2}
        self.inventory = [GoblinEar(), GoblinEar(), GoblinGem()]
        self.bers = False
        self.gold = 100

    def berserker(self):
        if self.dead and not self.bers:
            self.dead = False
            self.bers = True
            self.stats["HP"] = [50,50]
            self.stats["STR"] += 15
            self.stats["CON"] += 15
"""
class KoboldHighShaman(EnemyBoss):
    def __init__(self) -> None:
        super().__init__()
        self.stats = {"NAME":"Slime King","HP":[30,30], "MANA":[0,0], "STR":15, "CON":15, "AGI":5, "INT":2}

class OrcWarlord(EnemyBoss):
    def __init__(self) -> None:
        super().__init__()
        self.stats = {"NAME":"Slime King","HP":[30,30], "MANA":[0,0], "STR":15, "CON":15, "AGI":5, "INT":2}

class DemonPrince(EnemyBoss):
    def __init__(self) -> None:
        super().__init__()
        self.stats = {"NAME":"Slime King","HP":[30,30], "MANA":[0,0], "STR":15, "CON":15, "AGI":5, "INT":2}

class DragonTyrant(EnemyBoss):
    def __init__(self) -> None:
        super().__init__()
        self.stats = {"NAME":"Slime King","HP":[30,30], "MANA":[0,0], "STR":15, "CON":15, "AGI":5, "INT":2}

class DarkLord(EnemyBoss):
    def __init__(self) -> None:
        super().__init__()
"""