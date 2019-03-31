#Joshua Frenia
#Multiplayer text-based game
#2019 Hackathon
#03/30/19 - 03/31/19
import random
class room(object):
    def __init__(self, description, paths = [],interactions = None, monsters = None):
        self.description = description
        self.paths = paths
        self.interactions = interactions

introRoom = room("The area is full of trees with a small clearing with debris from some sort of accident.\nThere is a path to the south in the forest and a small shed to the east ", [{"s":"forest"},{"e":"shed"}])

class player(object):
    def __init__(self, name, health, inventory=[]):
        self.name = name
        self.health = health
        self.inventory = inventory

class npc(object):
    def __init__(self, name, health):
        self.name = name
        self.health = health

class monster(object):
    def __init__(self, name, health, damage, loot):
        self.name = name
        self.health = health
        self.damage = damage
        self.loot = loot

class items(object):
    def __init__(self, name, description, weight, position):
        self.name = name
        self.description = description
        self.weight = weight
        self.position = position

class weapons(object):
    def __init__(self, name, description, damage, handAmount):
        self.name = name
        self.description = description
        self.damage = damage
        self.handAmount = handAmount

def moves(room, move):
    if ((room == introRoom)and(move == "s")):
        return forest
    elif((room == introRoom)and(move == "e")):
        return shed
    elif((room == shed)and(move == "s")):
        return interiorShed
    elif((room == shed)and(move == "w")):
        return introRoom
    elif((room == forest)and(move == "s")):
        return forest
    elif((room == forest)and(move == "n")):
        return introRoom
    elif((room == interiorShed)and(move == "p")):
        return None
    elif((room == interiorShed)and(move == "e")):
        return shedInsideDoor
    elif((room == interiorShed)and (move == "n")):
        return shed
    elif((room == shedInsideDoor)and(move == "w")):
        return interiorShed
    elif((room == shedInsideDoor)and(move == "d")):
        return trapDoorUnderTroll
    elif((room == trickTunnel)and (move == "d")):
        return deathFromTrap
    elif((room == trickTunnel)and (move == "e")):
        return shed
    else:
        return room
        
greatSword = weapons("Great Sword", "Slices things", 10, 2)
shortSword = weapons("Short Sword", "Slices Things", random.randrange(6,8), 1)
greatAxe = weapons("Great Axe", "Chops Things", random.randrange(12,14), 2)
handAxe = weapons("Hand Axe", "Chops Things", 8, 1)
troll = monster("troll",random.randrange(20,40),random.randrange(3,5),greatAxe)
demon = monster("demon",random.randrange(40,60),random.randrange(6,9),None)
forest = room("You are in a forest with a dead end to the south and a path to a clearing to the north. ", [{"s":"forest"},{"n","introRoom"}])
shed = room("The shed is huge with a door slightly ajar to the south and a clearing to the west. ", [{"s":"interiorShed"},{"w","introRoom"}])
interiorShed = room("There is a dark room with swords on the floor, a door to the east and a door to the north.\n('p' to pick up for all players) ",[{"e":"shedInsideDoor"}], ["p"])
shedInsideDoor = room("In this very eary room, the only way out is back to the west. ",[{"w":"interiorShed"}],["a"])
trapDoorUnderTroll = room("In the corner of the room, you find a phone.('i' to interact)\nThere is also a tunnel heading south underground.\nThere is also a ladder up.\n",[{"u":"stepInsideDoor"}])
trickTunnel = room("There is a path that leads to the east and a ladder that leads down('d'). ")
deathFromTrap = room("Your team has been slain by an acid trap.\n")
def game(playerNumb, players):
    troll.health *= playerNumb
    troll.damage *= playerNumb
    print("You wake up and everyone around you seems fine, despite there being rubble all along the ground.\n('n','s','e','w' to move)")
    newRoom = introRoom
    numb=0
    while players != []:
        if newRoom != shedInsideDoor:
            move = input(newRoom.description)
            newRoom = moves(newRoom, move)
            if newRoom == None:
                for i in players:
                    i.inventory.append(shortSword)
                interiorShed.description = "There is a door to the east and a door to the north.\n"
                newRoom = interiorShed
        elif newRoom == shedInsideDoor:
            print(newRoom.description)
            if troll.health > 0:
                print("A troll attacks you!\n")
            while troll.health > 0 and players != []:            
                for j in players:
                    if random.randrange(1,6)>=4:
                        j.health -= troll.damage
                        print(j.name+" takes "+ str(troll.damage) + " points of damage and now has " + str(j.health) + " health left.\n")
                    if j.health > 0:      
                        move = input(j.name + ", how would you like to attack ('s' to attack with sword,'a' to attack without)? ")
                        n = 0
                        for k in j.inventory:
                            if n == 0:
                                n+=1
                                if ((move == "s")and(k == shortSword)):
                                    troll.health -= shortSword.damage
                                    print("The troll takes " + str(shortSword.damage) + " points of damage.\n")
                                elif move == "a":
                                    troll.health -= 3
                                    print("The troll takes " + str(3) + " points of damage.\n")
                    else:
                        print(j.name + " is dead.\n")
                        players.remove(j)
                        if players == []:
                            break

            if players != []:
                if numb == 0:
                    numb+=1
                    print("After the battle the whole team rests and heals to full health.\n")
                    for i in players:
                        i.health = 60
                
                    loot = input("You've slain the troll, you can loot the body('l').\n")
                else:
                    loot = "n"
                if loot == "l":
                    for i in players:
                        i.inventory.append(greatAxe)
                        print("You have obtained " + greatAxe.name)
                    print("As you are looting the body, you barely see a trap door under the body.\n")
                    shedInsideDoor.description = "There is a door to the west and a trap door below('d')"
                    newRoom = shedInsideDoor
                    move = input(shedInsideDoor.description)
                    newRoom = moves(newRoom, move)
                else:
                    newRoom = shedInsideDoor
                    move = input(shedInsideDoor.description)
                    newRoom = moves(newRoom, move)
                if newRoom == trapDoorUnderTroll:
                    demon.health *= playerNumb
                    demon.damage *= playerNumb
                    print("Demon:\nWell,look who came to die!\nI'm going to crush your bones into dust!\nI thought I'd killed you when I smashed you out of the sky!\nNow that you've killed my troll, I will enjoy this!\n")
                    while demon.health > 0 and players != []:            
                        for j in players:
                            if random.randrange(1,10)>=7:
                                j.health -= demon.damage
                                print(j.name+" takes "+ str(demon.damage) + " points of damage and now has " + str(j.health) + " health left.\n")
                            if j.health > 0:      
                                move = input(j.name + ", how would you like to attack ('s' to attack with sword,'a' to attack with axe)? ")
                                n = 0
                                for k in j.inventory:
                                    if n == 0:
                                        n+=1
                                        if ((move == "s")and(k == shortSword)):
                                            demon.health -= shortSword.damage
                                            print("The demon takes " + str(shortSword.damage) + " points of damage.\n")
                                        elif(move == "a"):
                                            demon.health -= greatAxe.damage
                                            print("The demon takes " + str(greatAxe.damage) + " points of damage.\n")
                            else:
                                print(j.name + " is dead.\n")
                                players.remove(j)
                                if players == []:
                                    break

                    if players != []:
                        print("You've slain the demon!\n")
                        move = input(trapDoorUnderTroll.description)
                        if move == "i":
                            print("The phone rings twice and then is picked up.\n")
                            print("The operator is surprised to hear from you.\n")
                            print("A rescue team arrives minutes later.\n")
                            break
                        elif move == "u":
                            newRoom = shedInsideDoor
                            move = input(newRoom.description)
                            newRoom = moves(newRoom, move)
                        elif move == "s":
                            newRoom = trickTunnel
                            move = input(newRoom.description)
                            newRoom = moves(newRoom, move)
                        else:
                            newRoom = trapDoorUnderTroll
                            move = input(newRoom.description)
                            newRoom = moves(newRoom, move)
                    else:
                        break

                if newRoom == deathFromTrap:
                    print(newRoom.description)
                    players = []
                    break
            else:
                break
    if players != []:
        print("Congratulations, you got rescued and completed the demo!")
    else:
        print("All players have died, you have failed.")
    
def main():
    gameStart = input("Would you like to play a game?('y' or 'n') ")
    if gameStart == "y":
        print("Hello adventurer(s)!")
        playerNumb = int(input("How many players are there?(1-4) "))
        if playerNumb>=1 and playerNumb<=4: 
            players = []
            number = 1
            while number <= playerNumb:
                name = input("What is the name of player " + str(number) + "? ")
                players.append(player(name,45))
                number += 1
            for i in players:
                print("Welcome " + i.name + "!")
            game(playerNumb,players)
        else:
            main()
    else:
        main()

if __name__ == "__main__":
    main()