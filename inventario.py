# templates
class Item():
    def __init__(self) -> None:
        self.name = ""
        self.cost = 0

class Drop(Item):
    def __init__(self) -> None:
        super().__init__()

class Equipment(Drop):
    def __init__(self) -> None:
        super().__init__()
        self.stats = {"HP":[0,0],
                      "MANA":[0,0],
                      "STR":0,
                      "CON":0, 
                      "AGI":0, 
                      "INT":0}
        self.equipped = False

class Sword(Equipment):
    def __init__(self) -> None:
        super().__init__()

class Shield(Equipment):
    def __init__(self) -> None:
        super().__init__()

class Armor(Equipment):
    def __init__(self) -> None:
        super().__init__()

class Helmet(Equipment):
    def __init__(self) -> None:
        super().__init__()

class Ring(Equipment):
    def __init__(self) -> None:
        super().__init__()

class Necklace(Equipment):
    def __init__(self) -> None:
        super().__init__()

class Utility(Item):
    def __init__(self) -> None:
        super().__init__()
        self.used = False
        self.one_time = False
        self.stats = {}
    
class Harmful(Item):
    def __init__(self) -> None:
        super().__init__()
        self.used = False
        self.damage = 0

# utility        
class HealthPotion(Utility):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Health Potion"
        self.cost = 10
        self.stats = {"HP":15}
        self.one_time = True

class ManaPotion(Utility):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Mana Potion"
        self.cost = 10
        self.stats = {"MANA":10}
        self.one_time = True
    
class StrengthPotion(Utility):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Strength Potion"
        self.cost = 10
        self.stats = {"STR":5}

class ConstitutionPotion(Utility):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Constitution Potion"
        self.cost = 10
        self.stats = {"CON":5}

class IntelligencePotion(Utility):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Intelligence Potion"
        self.cost = 10
        self.stats = {"INT":5}

class HealingHerb(Utility):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Healing Herb"
        self.cost = 5
        self.stats = {"HP":10}
        self.one_time = True

class MagicScroll(Utility):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Magic Scroll"
        self.cost = 50
        self.stats = {"MANA":20}
        self.one_time = True

# harmful
class HarmPotion(Harmful):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Harm Potion"
        self.cost = 10
        self.damage = 10

# drop
class SlimeGoo(Drop):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Slime Goo"
        self.cost = 5

class GoblinEar(Drop):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Goblin Ear"
        self.cost = 10

class KoboldEar(Drop):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Kobold Ear"
        self.cost = 8

# equipments
class SlimeCrown(Helmet):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Slime Crown"
        self.cost = 10
        self.stats = {"HP":[0,0],
                      "MANA":[0,0],
                      "STR":0,
                      "CON":5, 
                      "AGI":0, 
                      "INT":2}
        
class GoblinRing(Ring):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Goblin Gem"
        self.cost = 10
        self.stats = {"HP":[10,10],
                      "MANA":[0,0],
                      "STR":5,
                      "CON":5, 
                      "AGI":0, 
                      "INT":0}
        
class KoboldAmulet(Necklace):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Kobold Amulet"
        self.cost = 20
        self.stats = {"HP":[5,5],
                      "MANA":[5,5],
                      "STR":2,
                      "CON":2, 
                      "AGI":2, 
                      "INT":2}

class HeroSword(Sword):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Hero Sword"
        self.cost = 100
        self.stats = {"HP":[0,0],
                      "MANA":[0,0],
                      "STR":5,
                      "CON":0, 
                      "AGI":5, 
                      "INT":0}
        
class SmallShield(Shield):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Small Shield"
        self.cost = 15
        self.stats = {"HP":[5,5],
                      "MANA":[0,0],
                      "STR":0,
                      "CON":3, 
                      "AGI":0, 
                      "INT":0}

class LegendaryShield(Shield):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Legendary Shield"
        self.cost = 15000
        self.stats = {"HP":[500,500],
                      "MANA":[0,0],
                      "STR":0,
                      "CON":300, 
                      "AGI":0, 
                      "INT":0}
