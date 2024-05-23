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
        
class HealthPotion(Utility):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Health Potion"
        self.cost = 10
        self.stats = {"HP":10}
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
        self.stats = {"STR":10}

class ConstitutionPotion(Utility):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Constitution Potion"
        self.cost = 10
        self.stats = {"CON":10}

class IntelligencePotion(Utility):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Intelligence Potion"
        self.cost = 10
        self.stats = {"INT":10}

class HarmPotion(Harmful):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Harm Potion"
        self.cost = 10
        self.damage = 10

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

class SlimeCrown(Equipment):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Slime Crown"
        self.cost = 10
        self.stats = {"HP":[0,0],
                      "MANA":[0,0],
                      "STR":0,
                      "CON":10, 
                      "AGI":0, 
                      "INT":5}
        
class GoblinGem(Equipment):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Goblin Gem"
        self.cost = 10
        self.stats = {"HP":[10,10],
                      "MANA":[0,0],
                      "STR":10,
                      "CON":10, 
                      "AGI":0, 
                      "INT":0}
        
class HeroSword(Equipment):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Hero Sword"
        self.cost = 100
        self.stats = {"HP":[10,10],
                      "MANA":[10,10],
                      "STR":10,
                      "CON":10, 
                      "AGI":10, 
                      "INT":10}
        
