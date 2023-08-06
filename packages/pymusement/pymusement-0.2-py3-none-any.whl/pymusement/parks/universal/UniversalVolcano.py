from pymusement.parks.universal.UniversalPark import UniversalPark

class UniversalVolcano(UniversalPark):
    def __init__(self):
        super(UniversalVolcano, self).__init__()

    def getId(self):
        return 13801
    def getCity(self):
        return 'Orlando'
    def getName(self):
        return 'Universal Volcano Bay'
