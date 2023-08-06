#!/usr/bin/env python
from pymusement.parks.disney.DisneyPark import DisneyPark
class CaliforniaAdventure(DisneyPark):

    def __init__(self):
        super(CaliforniaAdventure, self).__init__()

    def getId(self):
        return '336894'

    def getName(self):
        return "Disney California Adventure"
