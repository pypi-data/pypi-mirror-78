from pymusement.attraction import Attraction
class Show(Attraction):

    _added_keys = ['showtimes', 'endtimes']

    def __init__(self):
        self._addKeys(self._added_keys)
        super(Show, self).__init__()

    def addTime(self, time):
        if self['showtimes'] is None:
            self['showtimes'] = [time]

        else:
            self['showtimes'].append(time)
    def addEnd(self, time):
        if self['endtimes'] is None:
            self['endtimes'] = [time]

        else:
            self['endtimes'].append(time)
    def getTimes(self):
        return self['showtimes'], self['endtimes']
