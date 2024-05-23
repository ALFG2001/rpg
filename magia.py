class Spell():
    def __init__(self) -> None:
        self.name = ""
        self.cost = 0
        self.damage = 0

class Smite(Spell):
    def __init__(self) -> None:
        self.name = "Smite"
        self.cost = 10
        self.damage = 2

class PoisonBall(Spell):
    def __init__(self) -> None:
        self.name = "Poison Ball"
        self.cost = 5
        self.damage = 3

class FireBolt(Spell):
    def __init__(self) -> None:
        self.name = "Fire Bolt"
        self.cost = 10
        self.damage = 2

class LightingStrike(Spell):
    def __init__(self) -> None:
        self.name = "lighting Strike"
        self.cost = 15
        self.damage = 3