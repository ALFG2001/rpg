from personaggi import *
from magia import *
from inventario import *
from collections import Counter

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

def checkBoss(nemico:Character) -> bool:
    if isinstance(nemico, EnemyBoss):
        return True
    return False

def kindOfBoss(boss:EnemyBoss) -> int:
    if isinstance(boss, SlimeKing):
        return 1
    if isinstance(boss, GoblinLord):
        return 2
    """
    if isinstance(boss, KoboldHighShaman):
        return 3
    if isinstance(boss, OrcWarlord):
        return 4
    if isinstance(boss, DemonPrince):
        return 5
    if isinstance(boss, DragonTyrant):
        return 6
    if isinstance(boss, DarkLord):
        return 7
    """

def bossPassive(i:int, boss:EnemyBoss, args:list):
    match i:    #PASSIVE BOSS
        case 1:
            list = args
            if boss.dead:
                print()
                print("THE SLIME KING IS DIVIDING ITSELF".center(60))
                print("-"*60)
                ind = list.index(boss)
                boss.divideSlime(list, ind)
            checkDead(list)
        case 2:
            list = args
            if boss.dead:
                print()
                print("THE GOBLIN LORD IS GOING BERSERKER".center(60))
                print("-"*60)
                boss.berserker()
            checkDead(list)
            
def checkHero(eroe:Character) -> bool:
    if isinstance(eroe, Hero):
        return True
    return False   

def printInventario(lista:list):
    listaItem = [(item.name, item.cost) for item in lista if not isinstance(item, Equipment)]
    listaEquipment = [(item.name, item.stats, item.equipped) for item in lista if isinstance(item, Equipment)]

    dictUsato = {}

    for item in listaItem:
        if item not in dictUsato:
            dictUsato[item] = 1
        else:
            dictUsato[item] += 1 
        
    for k in dictUsato:
        print(f"{dictUsato[k]} {k[0]} - ({k[1]*dictUsato[k]} Gold)")

    for item in listaEquipment:
        s = ["->"]
        for k in item[1]:
            stat = item[1][k]
            if not isinstance(stat, int):
                stat = stat[0]
            if stat > 0:
                s.append("+"+str(stat))
                s.append(k)
        if item[2]:
            s.append("- Equipped")
        else:
            s.append("- Not Equipped")
        print(item[0],*s)

def sortUniqueList(listaOriginale:list) -> list:
    dict_listaOriginale = {it.name:it for it in listaOriginale}
    sorted_keys = sorted(dict_listaOriginale.keys(), key=lambda key: listaOriginale.index(dict_listaOriginale[key]))
    sorted_unique = []
    for k in sorted_keys:
        sorted_unique.append(dict_listaOriginale[k])
    return(sorted_unique)

def meleeAttack(hero:Hero, nem:list, numeri_bersaglio:list, order:list):
    print("POSSIBLE TARGETS")
    for n in range(len(nem)):
        nem[n].printStats(n+1, 1)
        print("-"*60)
    # scegli il bersagli + check
    bersaglio = input(f"Which enemy will you attack {[int(x) for x in numeri_bersaglio[:-1]]}\n0 to go back: ")
    while bersaglio not in numeri_bersaglio:
        print("Target out of range")
        bersaglio = input(f"Which enemy will you attack {[int(x) for x in numeri_bersaglio[:-1]]}\n0 to go back: ")
    if bersaglio != "0":
        bersaglio = int(bersaglio)
        print("-"*60)
        hero.attack(nem[bersaglio-1])
        if checkBoss(nem[bersaglio-1]):
            boss = nem[bersaglio-1]
            b = kindOfBoss(boss)
            bossPassive(b, boss, nem)
            for nemici in nem:
                if nemici not in order:
                    order.append(nemici)
            agi = "AGI"
            order = sorted(order, key=lambda character: character.stats[agi], reverse=True)
        elif nem[bersaglio-1].dead:
            checkDead(nem)
        hero.hasAttacked = True
    else:
        print("-"*60)
        print("GOING BACK".center(60))

def spellAttack(hero:Hero, nem:list, numeri_bersaglio:list, order:list):
    if hero.spells:
        # prendi spells disponibili + numeri per selezione
        listaSpell = hero.spells
        numeri_spell = [str(x) for x in range(1,len(listaSpell)+1)] + ["0"]
        mana = "MANA"
        print(f"You have {hero.stats[mana][0]} Mana left")
        print("Which spell do you want to use:")
        # select spell che vuoi + check
        for indS in range(len(listaSpell)):
            print(f"{indS+1} - {listaSpell[indS].name} - cost: {listaSpell[indS].cost} Mana")
        select_spell = input("0 - to go back: ")
        while select_spell not in numeri_spell:
            print("Target out of range")
            print("Which spell do you want to use:")
            for indS in range(len(listaSpell)):
                print(f"{indS+1} - {listaSpell[indS].name} - cost: {listaSpell[indS].cost} Mana")
            select_spell = input(": ")
        select_spell = int(select_spell)
        if select_spell != 0:
            print("-"*60)
            print(f"Selected {listaSpell[select_spell-1].name}")
            print("-"*60)
            # controlla mana disponibile
            if hero.stats["MANA"][0] >= listaSpell[select_spell-1].cost:
                print("POSSIBLE TARGETS")
                # stampa bersaglio + selezione
                for n in range(len(nem)):
                    nem[n].printStats(n+1, 1)
                    print("-"*60)
                bersaglio = input(f"Which enemy will you cast {listaSpell[select_spell-1].name} on {[int(x) for x in numeri_bersaglio[:-1]]}\n0 to go back: ")
                while bersaglio not in numeri_bersaglio:
                    print("Target out of range")
                    bersaglio = input(f"Which enemy will you cast {listaSpell[select_spell-1].name} on {[int(x) for x in numeri_bersaglio[:-1]]}\n0 to go back: ")
                if bersaglio != "0":
                    bersaglio = int(bersaglio)
                    print("-"*60)
                    # cast spell
                    hero.castSpell(listaSpell[select_spell-1], nem[bersaglio-1])
                    # attiva passiva boss
                    if checkBoss(nem[bersaglio-1]):
                        boss = nem[bersaglio-1]
                        b = kindOfBoss(boss)
                        bossPassive(b, boss, nem)
                        for nemici in nem:
                            if nemici not in order:
                                order.append(nemici)
                        agi = "AGI"
                        order = sorted(order, key=lambda character: character.stats[agi], reverse=True)
                    elif nem[bersaglio-1].dead:
                        checkDead(nem)
                    hero.hasAttacked = True
                else:
                    print("-"*60)
                    print("GOING BACK".center(60))
            else:
                print("NOT ENOUGH MANA".center(60))
                print("-"*60)
        else:
            print("-"*60)
            print("GOING BACK".center(60))
    else:
        print("NO SPELL UNLOCKED".center(60))

def useItem(hero: Hero, nem: list, numeri_bersaglio: list, order: list):
    i = 1
    d_uti = {}
    d_harm = {}

    for item in hero.inventory:
        # Take only utility items
        if isinstance(item, Utility):
            if item.name not in d_uti:
                d_uti[item.name] = [1, [*item.stats], list(item.stats.values())]
            else:
                d_uti[item.name][0] += 1
 
        if isinstance(item, Harmful):
            if item.name not in d_harm:
                d_harm[item.name] = [1, item.damage]
            else:
                d_harm[item.name][0] += 1

    for k in d_uti:
        s = ""
        for stat in d_uti[k][1]:
            s += f"+{d_uti[k][2][0]} {d_uti[k][1][0]}"
        print(f"{i} - {k} -> {s} - {d_uti[k][0]} left")
        i += 1

    for k in d_harm:
        print(f"{i} - {k} -> {d_harm[k][1]} damage - {d_harm[k][0]} left")
        i += 1

    for item in hero.inventory:
        if isinstance(item, Equipment):
            listaStats = []
            for k, stat in item.stats.items():
                if isinstance(stat, list):
                    stat = stat[0]
                if stat > 0:
                    listaStats.append(f"+{stat} {k}")
            if item.equipped:
                print(f"{i} - {item.name} ->", *listaStats, "- Equipped")
            else:
                print(f"{i} - {item.name} ->", *listaStats, "- Not equipped")
            i += 1
    
    selection = [str(x) for x in range(1, i)] + ["0"]
    selection_str = ", ".join(selection[:-1])
    print("-"*60)
    stringa = f"Select item to equip/unequip [{selection_str}]\n0 to go back: "
    select = input(stringa)
    
    while select not in selection:
        print("Target out of range")
        select = input(stringa)
    
    if select != "0":
        itemSelectPot = [it for it in hero.inventory if isinstance(it, Utility)]
        sorted_unique_list_U = sortUniqueList(itemSelectPot)

        itemSelectHarm = [it for it in hero.inventory if isinstance(it, Harmful)]
        sorted_unique_list_H = sortUniqueList(itemSelectHarm)

        itemSelectEquip = [it for it in hero.inventory if isinstance(it, Equipment)]
        itemSelect = sorted_unique_list_U + sorted_unique_list_H + itemSelectEquip

        itemSelect = itemSelect[int(select) - 1]
        
        if isinstance(itemSelect, Equipment):
            if not itemSelect.equipped:
                print(f"Equipped {itemSelect.name}")
            else:
                print(f"Put {itemSelect.name} back in the inventory")
            hero.equip(itemSelect)
        
        elif isinstance(itemSelect, Utility):
            print(f"{hero.name} drank 1 {itemSelect.name}")
            if not itemSelect.one_time:
                print(f"{itemSelect.name} will last until the end of the encounter")
            hero.healPotion(itemSelect)
            hero.hasAttacked = True
        
        elif isinstance(itemSelect, Harmful):
            print("-" * 60)
            for n in range(len(nem)):
                nem[n].printStats(n + 1, 1)
                print("-" * 60)
            bersaglio = input(f"Which enemy will you use {itemSelect.name} on {[int(x) for x in numeri_bersaglio[:-1]]}\n0 to go back: ")
            while bersaglio not in numeri_bersaglio:
                print("Target out of range")
                bersaglio = input(f"Which enemy will you use {itemSelect.name} on {[int(x) for x in numeri_bersaglio[:-1]]}\n0 to go back: ")
            if bersaglio != "0":
                bersaglio = int(bersaglio)
                print("-" * 60)
                hero.harmPotion(itemSelect, nem[bersaglio - 1])
                if checkBoss(nem[bersaglio - 1]):
                    boss = nem[bersaglio - 1]
                    b = kindOfBoss(boss)
                    bossPassive(b, boss, nem)
                    for nemici in nem:
                        if nemici not in order:
                            order.append(nemici)
                    order = sorted(order, key=lambda character: character.stats["AGI"], reverse=True)
                elif nem[bersaglio - 1].dead:
                    checkDead(nem)
                hero.hasAttacked = True
            else:
                print("-" * 60)
                print("GOING BACK".center(60))
    else:
        print("-" * 60)
        print("GOING BACK".center(60))

def turnoEroe(hero:Hero, nem:list, order:list):
    hero.hasAttacked = False
    while not hero.hasAttacked:
        numeri_bersaglio = [str(x) for x in range(1,len(nem)+1)] + ["0"]
        
        what_now = input("What do you want to do now?\n1 - Melee attack\n2 - Cast a spell\n3 - Use an item\n4 - Check enemies\n5 - Check self\n6 - Check spell\n7 - Check inventory\n: ")
        while what_now not in ("1","2","3","4","5","6","7"):
            print("Error")
            print("Try again")
            what_now = input(": ")
        print("-"*60)

        match what_now:
            case "1": # attacco melee
                meleeAttack(hero, nem, numeri_bersaglio, order)
            case "2": # attacco magico
                spellAttack(hero, nem, numeri_bersaglio, order)
            case "3": # equip item
                useItem(hero, nem, numeri_bersaglio, order)
            case "4": # check enemies
                for n in range(len(nem)):
                    nem[n].printStats(0,1)
            case "5": # check self
                hero.printStats()      
                if hero.spells:
                    print("-"*60)
                    print("AVAILABLE SPELLS")
                    for spell in hero.spells:
                        print(f"{spell.name}: {spell.cost} Mana")
            case "6": # check spells
                if hero.spells:
                    for spell in hero.spells:
                        checkSpell(spell, hero)
                else:
                    print("NO SPELLS UNLOCKED".center(60))
            case "7": # check inventory
                print(f"{hero.gold} Gold Pieces")
                if hero.inventory:
                    printInventario(hero.inventory)
                else:
                    print("NO ITEMS IN INVENTORY".center(60))
        
        print("-"*60)
        _ = input("Press Enter to continue".center(60))
        print("-"*60)

def turnoNemico(hero:Hero, persona:Character):
    if not persona.dead:
        if not hero.dead:
            if persona.spells:
                # gets all enemy spells sorted by damage
                availableSpells = sorted(persona.spells, key=lambda sp: sp.damage, reverse=True)
                availableMana = persona.stats["MANA"][0]
                i = 0
                casted = False
                # casta prima spell con costo abbastanza basso disponibile
                while not casted and i < len(availableSpells):
                    if availableMana >= availableSpells[i].cost:
                        persona.castSpell(availableSpells[i], hero)
                        casted = True
                    else:
                        i += 1
                # se non casta spell attacca
                if not casted:
                    persona.attack(hero)
            else:
                #se non ha spell attacca
                persona.attack(hero)
        if not hero.dead:
            print("-"*60)
            _ = input("Press Enter to continue".center(60))
            print("-"*60)

def buy(hero:Hero,shop:list, shopOG:list ,item_class, quanti:int):
    # takes item from the shop and adds it to the inventory while removing the price from the hero
    for i in range(quanti):
        new_object = item_class()
        hero.inventory.append(new_object)
        hero.gold -= new_object.cost
        for i, item in enumerate(shop):
            if type(item) == type(new_object):
                for oggetto in shopOG:
                    if type(oggetto) == type(shop[i]):
                        shopOG.remove(oggetto)
                        break
                del shop[i]
                break
            
def sell(hero:Hero, shop:list, item:Item, quanti:int):
    # takes item from the inventory and adds it to the shop while adding the price to the hero
    for _ in range(quanti):
        for i in hero.inventory:
            if type(item) == type(i):
                if isinstance(i, Equipment) and i.equipped:
                    hero.equip(i)
                hero.inventory.remove(i)
                shop.append(i)
                hero.gold += item.cost
                shop.sort(key=lambda x : x.name)
                break

def hasBought(hero:Hero, store:list, storeOG:list, quanti:int):
    # takes all classes from store
    store_set = set(type(obj) for obj in store)
    used_subclasses_list = []
    
    # takes every item subclass
    lista_classi = []
    lista_classi += [classe for classe in Drop.__subclasses__()]
    lista_classi += [classe for classe in Equipment.__subclasses__()]
    lista_classi += [classe for classe in Utility.__subclasses__()]
    lista_classi += [classe for classe in Harmful.__subclasses__()]

    # Iterate over all subclasses and append the ones in the store to the list
    for subclass in lista_classi:
        if subclass in store_set:
            used_subclasses_list.append(subclass)

    # checks name and if you can buy
    for name in used_subclasses_list:
        a = len(hero.inventory)
        buy(hero, store, storeOG, name, quanti)
        b = len(hero.inventory)
        print("-"*60)
    if a != b:
        print(f"{hero.name} bought {quanti} {name().name}")
    else:
        print(f"{hero.name} could not buy {quanti} {name().name}")

def hasSold(hero:Hero, shop:list, item:Item, quanti:int):
    # takes all classes from inventory
    inventory_set = set(type(obj) for obj in hero.inventory)
    used_subclasses_list = []

    # takes every item subclass
    lista_classi = []
    lista_classi += [classe for classe in Drop.__subclasses__()]
    lista_classi += [classe for classe in Equipment.__subclasses__()]
    lista_classi += [classe for classe in Utility.__subclasses__()]
    lista_classi += [classe for classe in Harmful.__subclasses__()]

    # Iterate over all subclasses and append the ones in the inventory to the list
    for subclass in lista_classi:
        if subclass in inventory_set:
            used_subclasses_list.append(subclass)

    # checks name and if you can sell
    for name in used_subclasses_list:
        if type(item) == name:
            a = len(shop)
            sell(hero, shop,item, quanti)
            b = len(shop)
            print("-"*60)
            if a != b:
                print(f"{hero.name} sold {quanti} {name().name}")
            else:
                print(f"{hero.name} could not sell {quanti} {name().name}")

def selectItemBuy(hero:Hero, store:list):
    # takes and formats a set of the store
    store_set = dict(enumerate(set((obj.name, globals()[obj.__class__.__name__]) for obj in store),1))
    stampa = [(x,store_set[x][0],sum(1 for item in store if isinstance(item,store_set[x][1])),store_set[x][1].__name__) for x in store_set]
    selectNumbers = []

    print("THE SHOP".center(60, "-"))
    # prints the formatted store
    for it in stampa:
        selectNumbers.append(str(it[0]))
        print(f"{it[0]} - {it[1]} - {globals()[it[3]]().cost} Gold each - {it[2]} available")
    print("-"*60)

    # select item you want to buy
    if len(selectNumbers)-1 < 1:
        step = 1
    else:
        step = len(selectNumbers)-1
    select = input(f"select item {list(range(1, int(selectNumbers[-1])+1, step))}\n0 to quit: ")
    while select not in selectNumbers + ["0"]:
        print("error")
        select = input(f"select item {list(range(1, int(selectNumbers[-1])+1, step))}\n0 to quit: ")
    
    #select how many of the item you want to buy
    if select != "0":
        select = int(select)
        classSelect = [store_set[x][1]() for x in store_set if x == select][0]
        storeSelect = [item for item in store if isinstance(item, globals()[classSelect.__class__.__name__])]

        print("-"*60)
        if len(storeSelect)-1 < 1:
            step = 1
        else:
            step = len(storeSelect)-1

        quanti = input(f"how many {storeSelect[0].name} do you want to buy {list(range(1, 1+len(storeSelect), step))}\n0 to quit: ")
        while not quanti.isnumeric():
            print("Error")
            quanti = input(f"how many {storeSelect[0].name} do you want to buy {list(range(1, 1+len(storeSelect), step))}\n0 to quit: ")
        quanti = int(quanti)
        while quanti not in list(range(1, 1+len(storeSelect)))+[0]:
            print("Error")
            quanti = int(input(f"how many {storeSelect[0].name} do you want to buy {list(range(1, 1+len(storeSelect), step))}\n0 to quit: "))

        # buys the item selected in the desired quantity
        if quanti != 0:
            hasBought(hero, storeSelect, store, quanti)
            print(f"{hero.name} has {hero.gold} Gold left!")
        else:
            print("-"*60)
            print("quit")
    else:
        print("-"*60)
        print("quit")

def selectItemSell(hero:Hero, store:list):
    inventario = hero.inventory
    inventario_set = dict(enumerate(set((obj.name, globals()[obj.__class__.__name__]) for obj in inventario),1))
    stampa = [(x,inventario_set[x][0],sum(1 for item in inventario if isinstance(item,inventario_set[x][1])),inventario_set[x][1].__name__) for x in inventario_set]
    selectNumbers = []

    print("INVENTORY".center(60, "-"))
    for it in stampa:
        selectNumbers.append(str(it[0]))
        print(f"{it[0]} - {it[1]} - {globals()[it[3]]().cost} Gold each - You have {it[2]}")
    print("-"*60)

    if len(selectNumbers)-1 < 1:
        step = 1
    else:
        step = len(selectNumbers)-1
    select = input(f"select item {list(range(1, int(selectNumbers[-1])+1, step))}\n0 to quit: ")
    while select not in selectNumbers + ["0"]:
        print("error")
        select = input(f"select item {list(range(1, int(selectNumbers[-1])+1, step))}\n0 to quit: ")
    print("-"*60)

    if select != "0":
        select = int(select)
        classSelect = [inventario_set[x][1]() for x in inventario_set if x == select][0]
        inventarioSelect = [item for item in inventario if isinstance(item, globals()[classSelect.__class__.__name__])]

        if len(inventarioSelect)-1 < 1:
            step = 1
        else:
            step = len(inventarioSelect)-1

        quanti = input(f"how many {inventarioSelect[0].name} do you want to sell {list(range(1, 1+len(inventarioSelect), step))}\n0 to quit: ")
        while not quanti.isnumeric():
            print("Error")
            quanti = input(f"how many {inventarioSelect[0].name} do you want to sell {list(range(1, 1+len(inventarioSelect), step))}\n0 to quit: ")
        quanti = int(quanti)
        while quanti not in list(range(1, 1+len(inventarioSelect)))+[0]:
            print("Error")
            quanti = int(input(f"how many {inventarioSelect[0].name} do you want to sell {list(range(1, 1+len(inventarioSelect), step))}\n0 to quit: "))  
        
        if quanti != 0:
            hasSold(hero, store, inventarioSelect[0], quanti)
            print(f"{hero.name} has now {hero.gold} Gold!")
        else:
            print("-"*60)
            print("quit")
    else:
        print("quit")

def openShop(hero:Hero, store:list, compra:str):
    store.sort(key=lambda x : x.name)
    match compra:
        case "1":
            if store:
                selectItemBuy(hero, store)
                print("-"*60)
            else:
                print("-"*60)
                print("nothing for sale")
                print("-"*60)
        case "2":
            if hero.inventory:
                print("-"*60)
                selectItemSell(hero, store)
                print("-"*60)
            else:
                print("nothing to sell")
                print("-"*60)
        case "3":
            print("-"*60)
            print(f"{hero.name} has {hero.gold} Gold Pieces")
            print("-"*60)
        case "0":
            print("-"*60)
            print("quit")

def createShop(stage:int, shop=[]) -> list:
    match stage:
        case 1:
            for _ in range(3):
                shop.append(HealthPotion())
            for _ in range(3):
                shop.append(ManaPotion())
            for _ in range(3):
                shop.append(HarmPotion())
            shop.append(StrengthPotion())
            shop.append(ConstitutionPotion())
            shop.append(IntelligencePotion())
    return shop
