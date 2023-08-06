from pymusement.parks.universal.UniversalPark import UniversalPark

class IslandsOfAdventure(UniversalPark):
    def __init__(self):
        super(IslandsOfAdventure, self).__init__()

    def getId(self):
        return 10000

    def getCity(self):
        return 'Orlando'

    def getName(self):
        return 'Islands of Adventure'
