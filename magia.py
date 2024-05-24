class Spell():
    def __init__(self) -> None:
        self.name = ""
        self.cost = 0
        

class Damaging(Spell):
    def __init__(self) -> None:
        super().__init__()
        self.damage = 0

class Healing(Spell):
    def __init__(self) -> None:
        super().__init__()
        self.heal = 0

class Smite(Damaging):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Smite"
        self.cost = 10
        self.damage = 2

class PoisonBall(Damaging):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Poison Ball"
        self.cost = 5
        self.damage = 3

class FireBolt(Damaging):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Fire Bolt"
        self.cost = 10
        self.damage = 2

class LightingStrike(Damaging):
    def __init__(self) -> None:
        super().__init__()
        self.name = "lighting Strike"
        self.cost = 15
        self.damage = 3

class HealingLight(Healing):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Healing Light"
        self.cost = 8
        self.heal = 4  # Negative damage indicates healing

class HealingWave(Healing):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Healing Wave"
        self.cost = 15
        self.heal = 8  # Negative damage indicates healing
