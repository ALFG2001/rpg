from personaggi import *
from magia import *
from inventario import *
from functions import *

def begin(hero:Hero):
    END = False
    while not hero.dead and not END:        
        # livelli da 1 a 7
        for livello in range(1,3):
            # ultimo encounter dello stage = boss fight
            boss = False
            print(f"STAGE {livello}".center(60, "-"))
            # diversi encounter nello stesso stage
            for encounter in range(1,livello+2):
                hero.printStats()
                print("-"*60)
                _ = input("Press Enter to continue".center(60))
                # controlla quando c'è bossfight
                if encounter == livello+1:
                    boss = True
                print(f"ENCOUNTER {encounter}".center(60, "-"))
                # crea lista di nemici
                nem = summonEnemies(livello,encounter, boss)
                print("-"*60)
                agi = "AGI"
                # aggiunge eroe e ordina per agilità
                orderOfAction = sorted([hero]+nem, key=lambda character: character.stats[agi], reverse=True)
                while nem:
                    for persona in orderOfAction:
                        # turno eroe
                        if checkHero(persona) and not persona.dead:
                            # turno eroe
                            turnoEroe(hero, nem, orderOfAction)
                        else:
                            # turno nemici
                            turnoNemico(hero, persona)
                
                print("DROPS")
                # i morti droppano e aggiungi all'inventario
                for persona in orderOfAction:
                    if not isinstance(persona, Hero):
                        if persona.dead:
                            print(f"1 - {persona.gold} Gold")
                            dropped = persona.dropItems()
                            hero.inventory += dropped
                            hero.gold += persona.gold

                print("-"*60)
                hero.levelUp()
            if livello < 2: # dovrà essere 7
                if livello > 1:
                    shop = createShop(livello, shop)
                else:
                    shop = createShop(livello)
                print("ENTERING SHOP".center(60,"-"))
                print("1 - buy")
                print("2 - sell")
                print("3 - check gold")
                bs = input("0 to quit: ")
                while bs != "0":
                    openShop(hero, shop, bs)
                    print("1 - buy")
                    print("2 - sell")
                    print("3 - check gold")
                    bs = input("0 to quit: ")
                input("NEW STAGE - ENTER TO CONTINUE".center(60,"-"))
        if not END:
            hero.printStats()
        print("-"*60)
        if livello > 1: # deve diventare 6
            END = True
    if not hero.dead:
        print("YOU WIN!".center(60))
        print("-"*60)
    else:
        print("YOU LOSE!".center(60))
        print("-"*60)
    again = input("PLAY AGAIN? [Y/N]")
    return again

