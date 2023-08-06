from pymusement.parks.universal.UniversalPark import UniversalPark

class UniversalStudiosFlorida(UniversalPark):
    def __init__(self):
        super(UniversalStudiosFlorida, self).__init__()

    def getId(self):
        return 10010
    def getCity(self):
        return 'Orlando'
    def getName(self):
        return 'Universal Studios Florida'
