import requests
import datetime
import hmac
import base64
import re
import hashlib
import json
from pymusement.park import Park
from pymusement.ride import Ride
from pymusement.show import Show
SHARED_HEADERS = {
    'Accept'                          : 'application/json',
    'Accept-Language'                 : 'en-US',
    'X-UNIWebService-AppVersion'      : '1.2.1',
    'X-UNIWebService-Platform'        : 'Android',
    'X-UNIWebService-PlatformVersion' : '4.4.2',
    'X-UNIWebService-Device'          : 'samsung SM-N9005',
    'X-UNIWebService-ServiceVersion'  : '1',
    'User-Agent'                      : 'Dalvik/1.6.0 (Linux; U; Android 4.4.2; SM-N9005 Build/KOT49H)',
    'Connection'                      : 'keep-alive',
    'Accept-Encoding'                 : 'gzip'
  }

RIDE_URL = 'https://services.universalorlando.com/api/pointsofinterest/rides'
SHOW_URL = 'https://services.universalorlando.com/api/pointsofinterest/Shows'
HOUR_URL = 'https://services.universalorlando.com/api/venues/{0}/hours'

class UniversalPark(Park):
    def __init__(self):
        super(UniversalPark, self).__init__()

    def _buildPark(self):
        token = self._get_token()
        ride_page = self._get_request(token, RIDE_URL)
        show_page = self._get_request(token, SHOW_URL)
        hour_page = self._get_request(token, HOUR_URL.format(self.getId()))
        
        for date in hour_page:
            if datetime.date.fromisoformat(date['Date']) == datetime.date.today():
                open_time, close_time = datetime.datetime.fromisoformat(date['OpenTimeString']), datetime.datetime.fromisoformat(date['CloseTimeString'])
                if open_time < datetime.datetime.now().astimezone() < close_time:
                    self.set_open()
                else:self.set_closed()
        
        for ride in ride_page['Results']:
            if ride['VenueId'] == self.getId():
                self._make_attraction(ride)

        
        for show in show_page['Results']:
            if show['VenueId'] == self.getId():
                self._make_show(show)
        

    def _make_attraction(self, ride):
        attraction = Ride()
        attraction.setName(ride['MblDisplayName'])
        
        if ride['WaitTime'] is None:
            attraction.setClosed()
        else:
            attraction.setOpen()

        if ride['WaitTime'] == -50:
            attraction.setTime(-1)
            attraction.setStatus('Unknown')
            attraction.setClosed()
        if ride['WaitTime'] == -9:
            attraction.setOpen()
            attraction.setTime(0)
            attraction.setStatus('VLO')
        elif ride['WaitTime'] == -8:
            attraction.setClosed()
            attraction.setTime(-1)
            attraction.setStatus('Not Open Yet')
        elif ride['WaitTime'] == -7:
            attraction.setTime(0)
            attraction.setOpen()
        elif ride['WaitTime'] == -5:
            attraction.setClosed()
            attraction.setTime(-1)
            attraction.setStatus('Capacity')
        elif ride['WaitTime'] == -4:
            attraction.setClosed()
            attraction.setStatus('Weather')
        elif ride['WaitTime'] < 0:
            attraction.setClosed()
            attraction.setTime(-1)
            attraction.setStatus('Closed')
            

        else:
            attraction.setTime(ride['WaitTime'])
        
        attraction.setVirtualLine(ride['VirtualLine'])
        
        
        
        self.addRide(attraction)

    def _make_show(self, show):
        show_obj = Show()
        show_obj.setName(show['MblDisplayName'])
        for time in show['StartTimes']:
            show_obj.addTime(time)
        if show['EndTimes']:
            for time in show['EndTimes']:
                show_obj.addEnd(time)
        self.addShow(show_obj)


    def _get_request(self, token, url):
        headers = {
            'X-UNIWebService-ApiKey' : 'AndroidMobileApp',
            'X-UNIWebService-Token' : token 
        }
        headers.update(SHARED_HEADERS)
        params = {'city':self.getCity(),'pageSize':'all'}
        r = requests.get(url, headers=headers, params=params)
        return r.json()

    def _get_token(self):
        # Thanks to lloydpick for the Key / Secret
        KEY    = 'AndroidMobileApp'
        SECRET = b'AndroidMobileAppSecretKey182014'

        date = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        secret_test = "{KEY}\n{date}\n".format(KEY=KEY, date=date)
        digest = hmac.new(SECRET, secret_test.encode('ascii'), hashlib.sha256)
        signature = base64.b64encode(digest.digest()).strip()
        signature = re.sub('/=$/', "\u003d", signature.decode('ascii'))
        
        
        params = { 
                'apikey': 'AndroidMobileApp', 
                'signature': signature 
        }
        headers = {
            'Date' :date,
            'Content-Type' : 'application/json; charset=UTF-8'
        }

        headers.update(SHARED_HEADERS)

        r = requests.post('https://services.universalorlando.com/api', headers=headers, data=json.dumps(params, ensure_ascii=False))
        return r.json()['Token']
