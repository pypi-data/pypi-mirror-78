from pymusement.parks.universal.UniversalPark import UniversalPark

class UniversalHollywood(UniversalPark):
    def __init__(self):
        super(UniversalHollywood, self).__init__()

    def getId(self):
        return 13825
    def getCity(self):
        return 'Hollywood'
    def getName(self):
        return 'Universal Studios Hollywood'
