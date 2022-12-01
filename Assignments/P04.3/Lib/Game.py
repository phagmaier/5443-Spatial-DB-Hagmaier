import requests
import json
import pprint

class Game:
    def __init__(self):
        with open('./login.json', 'r') as f:
            info = json.load(f)
            self.__key = info['key']

        self.__teamName = 'hydra'
        
        self.__data = None
        self.__game_id = None
        self.__fleet_id = None
        self.__bbox = None
        self.__cardinalLocation = None

    def Start(self):
        #needs to set game_id
        #needs to set fleet_id
        return 'Start'

    def GenFleet(self):
        res = requests.get("https://battleshipgame.fun:1234/generate_fleet/?fleetName="
                           + self.__teamName + "&hash=" + self.__key)
        
        if res.status_code == requests.codes.ok:
            self.__data = res.json()

            return 'Success'
        else:
            return 'Error'
    
    def GetLocation(self):
        res = requests.get("https://battleshipgame.fun:1234/get_battle_location/?hash="
                           + self.__key + "&game_id=" + self.__game_id)

        if res.status_code == requests.codes.ok:
            data = res.json()
            
            self.__bbox = data['bbox']
            self.__cardinalLocation = data['CardinalLocation']

            return 'Success'
        else:
            return 'Error'

    def PosFleet(self):
        return 'PosFleet'

    def ShipSpeed(self):
        return 'ShipSpeed'
    
    def MoveShip(self):
        return 'MoveShip'
    
    def TurnShip(self, shipList, bearingList):
        url = "https://battleshipgame.fun:1234/turn_ship/?hash=" + self.__key

        payload = json.dumps({
            "fleet_id": self.__fleet_id,
            "ship_id": shipList, #ie. [3,4,8] or []
            "bearing": bearingList #ie. [200,300,180]
        })

        headers = {
            'Content-Type': 'application/json'
        }

        res = requests.request("GET", url, headers=headers, data=payload)

        if res.status_code == requests.codes.ok:
            return 'Success'
        else:
            return 'Error'

    def MoveGun(self, shipID, bearingList, elevationList):
        #!!!NEED DOCUMENTATION TO CONTINUE MOVE GUN

        # url = "https://battleshipgame.fun:1234/moveGuns/?hash=" + self.__key

        # payload = json.dumps({
        #     "fleet_id": self.__fleet_id,
        #     "ship_id": shipList, #ie. [0, 1, 2]
        #     "gun_id": gunList, #ie. [[3, 6], [5, 6]] list of ships, list of guns
        #     "gun_position": ???
        # })

        # headers = {
        #     'Content-Type': 'application/json'
        # }

        # res = requests.request("GET", url, headers=headers, data=payload)

        # if res.status_code == requests.codes.ok:
        #     return 'Success'
        # else:
        #     return 'Error'
        
        #------------------------------------
        #changing this to orient gun for now
        #------------------------------------

        url = "https://battleshipgame.fun:1234/orient_guns/?hash=" + self.__key

        payload = json.dumps({
            "fleet_id": self.__fleet_id,
            "ship_id": shipID, #ie. 5
            "bearing": bearingList, #ie. [90,0,270,180,0]
            "elevation": elevationList #ie. [0, 10, 15, 30, 45]
        })

        headers = {
            'Content-Type': 'application/json'
        }

        res = requests.request("GET", url, headers=headers, data=payload)

        if res.status_code == requests.codes.ok:
            return 'Success'
        else:
            return 'Error'

    def FireGun(self, shipID, gunList, elevationList, velocityList):
        url = "https://battleshipgame.fun:1234/fireGuns/?hash=" + self.__key + "&fleet_id=" + self.__fleet_id + "&ship_id=" + str(shipID)

        payload = json.dumps({
            "elevation": elevationList, #ie. [0, 10, 15, 30, 45]
            "velocity": velocityList,
            "gun_id": gunList
        })

        headers = {
            'Content-Type': 'application/json'
        }

        res = requests.request("GET", url, headers=headers, data=payload)

        if res.status_code == requests.codes.ok:
            return pprint.pformat(res.json(), indent = 4)
        else:
            return 'Error'