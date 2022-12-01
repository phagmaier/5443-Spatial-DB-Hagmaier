from Lib.Game import Game

from pick import pick
import json

BattleShip = Game()

title = 'SELECT OPTION (ENTER to continue): '
options = []

with open('Config/menu.json') as f:
    dics = json.load(f)
    
    for dic in dics:
        options.append(dic['item'])

options.append('Exit')

while(True):
    selected = pick(options, title, '->' , 0, False, 1)

    secondOptions = ['Exit']
    secondTitle = 'Response: '

    match selected[0]:
        case 'Start':
            secondTitle += BattleShip.Start()

        case 'Generate Fleet':
            secondTitle += BattleShip.GenFleet()

        case 'Get Battle Location':
            secondTitle += BattleShip.GetLocation()

        case 'Position Fleet':
            secondTitle += BattleShip.PosFleet()

        case 'Ships Speed':
            secondTitle += BattleShip.ShipSpeed()

        case 'Move Ships':
            secondTitle += BattleShip.MoveShip()

        case 'Turn Ships':
            shipList = []
            bearingList = []

            numShips = ['All']

            for i in range(1,26): numShips.append(i)
            
            selected = pick(numShips, 'Select all ships you want to turn (SPACE to select ENTER to continue)', '->' , 0, True, 1)

            for option in selected:
                shipList.append(option[0])

            
            if 'All' in shipList:
                selected = pick(list(range(0,361,5)), 'Select degree to turn all ships (SPACE to select ENTER to continue)', '->' , 0, False, 1)
                bearingList.append(selected[0])
                shipList = []

            for ship in shipList:
                selected = pick(list(range(0,361,5)), 'Select degree to turn ship: ' + str(ship) + ' (SPACE to select ENTER to continue)', '->' , 0, False, 1)
                bearingList.append(selected[0])

            secondTitle += BattleShip.TurnShip(shipList, bearingList)

        case 'Move Guns':
            bearingList = []
            elevationList = []
            
            selected = pick(list(range(1,26)), "Select the ship who's gun to move (ENTER to continue)", '->' , 0, False, 1)

            shipID = selected[0]
            
            for i in range(1,6):
                selected = pick([-1, 0, 90, 180, 270], "Select the bearing for gun (-1 to stay the same): " + str(i) + " (ENTER to continue)", '->' , 0, False, 1)
                bearingList.append(selected[0])

            for i in range(1,6):
                selected = pick(list(range(-1,46)), "Select the elevation for gun (-1 to stay the same): " + str(i) + " (ENTER to continue)", '->' , 0, False, 1)
                elevationList.append(selected[0])

            secondTitle += BattleShip.MoveGun(shipID, bearingList, elevationList)

        case 'Fire Guns':
            velocityList = []
            elevationList = []
            gunsList = []
            
            selected = pick(list(range(1,26)), "Select the ship who's gun(s) to fire (ENTER to continue)", '->' , 0, False, 1)

            shipID = selected[0]

            selected = pick(list(range(1,6)), "Select the guns from ship " + str(shipID) + " to fire: (SPACE to select ENTER to continue)", '->' , 0, True, 1)
            
            for item in selected:
                gunsList.append(item[0])

            for gun in gunsList:
                selected = pick(list(range(0,46)), "Select the elevation for gun: " + str(gun) + " (ENTER to continue)", '->' , 0, False, 1)
                elevationList.append(selected[0])

                selected = pick([100, 200], "Select the velocity for the shot from gun: " + str(gun) + " (ENTER to continue)", '->' , 0, False, 1)
                velocityList.append(selected[0])
            
            print(gunsList, elevationList, velocityList)

            secondTitle += BattleShip.FireGun(shipID, gunsList, elevationList, velocityList)

        case 'Exit':
            exit()

    pick(secondOptions, secondTitle, '->' , 0, False, 1)