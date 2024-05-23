from buildUI import *

def main():
    print("-"*60)
    print("PLAY THE GAME".center(60))
    print("-"*60)
    eroe = Hero()
    eroe.name = input("Who are you: ").capitalize()
    sword = [HeroSword()]
    print(f"-{eroe.name} picks up the {sword[0].name}")
    potions = [HealthPotion(),HealthPotion(),HealthPotion(),
               ManaPotion(),ManaPotion(),ManaPotion(),
               HarmPotion(),HarmPotion()]
    object_counts = Counter(obj.name for obj in potions)
    for name, count in object_counts.items():
        print(f"-{eroe.name} picks up {count} {name}")
    eroe.inventory += sword + potions
    eroe.gold = 100
    print(f"-{eroe.name} picks up {eroe.gold} Gold")
    # eroe.equip(sword[0])
    begin(eroe)
    print("-"*60)

main()
