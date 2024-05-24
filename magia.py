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

class Buffing(Spell):
    def __init__(self) -> None:
        super().__init__()
        self.stat = {"":0}

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

class LightningStrike(Damaging):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Lightning Strike"
        self.cost = 15
        self.damage = 3

class ShadowBolt(Damaging):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Shadow Bolt"
        self.cost = 10
        self.damage = 8

class DarkFlame(Damaging):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Dark Flame"
        self.cost = 15
        self.damage = 10

class FireBreath(Damaging):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Fire Breath"
        self.cost = 25
        self.damage = 20

class DeathCurse(Damaging):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Death Curse"
        self.cost = 40
        self.damage = 30

class SoulDrain(Damaging):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Soul Drain"
        self.cost = 20
        self.damage = 20

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

