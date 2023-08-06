from pymusement.parks.universal.UniversalStudiosFlorida import UniversalStudiosFlorida
from pymusement.parks.universal.IslandsOfAdventure import IslandsOfAdventure
from pymusement.parks.universal.UniversalHollywood import UniversalHollywood
from pymusement.parks.universal.UniversalVolcano import UniversalVolcano
from pymusement.parks.HersheyPark import HersheyPark


PARKS = {
    'universal-florida' : UniversalStudiosFlorida(),
    'islands-adventure' : IslandsOfAdventure(),
    'universal-hollywood' : UniversalHollywood(),
    'volcano-bay' : UniversalVolcano(),
    'hersheypark' : HersheyPark()
}
