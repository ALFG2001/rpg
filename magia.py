class Spell():
    def __init__(self) -> None:
        self.name = ""
        self.cost = 0
        self.damage = 0

class Smite(Spell):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Smite"
        self.cost = 10
        self.damage = 2

class PoisonBall(Spell):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Poison Ball"
        self.cost = 5
        self.damage = 3

class FireBolt(Spell):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Fire Bolt"
        self.cost = 10
        self.damage = 2

class LightingStrike(Spell):
    def __init__(self) -> None:
        super().__init__()
        self.name = "lighting Strike"
        self.cost = 15
        self.damage = 3

class HealingLight(Spell):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Healing Light"
        self.cost = 8
        self.damage = -4  # Negative damage indicates healing

class HealingWave(Spell):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Healing Wave"
        self.cost = 15
        self.damage = -8  # Negative damage indicates healing
