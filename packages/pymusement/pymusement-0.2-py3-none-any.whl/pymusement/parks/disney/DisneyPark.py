#!/usr/bin/env python
import requests
import json
import datetime
from pymusement.park import Park
from pymusement.ride import Ride

URL_TEMPLATE = 'https://api.wdpro.disney.go.com/facility-service/theme-parks/%s'

class DisneyPark(Park):

    def __init__(self):
        self._id = self.getId()
        self._url = URL_TEMPLATE % self._id
        self.name = self.getName()
        super(DisneyPark, self).__init__()

    def getId(self):
        raise('This must be implemented in a subclass')

    def getName(self):
        raise('This must be implemented in a subclass')

    def _buildPark(self):
        self._auth_token = self._authorize()
        page = self._get_page()
        for attraction in page['entries']:
            if attraction['type'] != 'Attraction':
                continue
            self._build_attraction(attraction)

    def _build_attraction(self, attraction):
        attraction_obj = Ride()

        attraction_obj.setName(attraction['name'])
        self._waitTime(attraction_obj, attraction)

        self.addRide(attraction_obj)
    
    
    
    def _get_page(self):
        # Make page request, return dictionary of a park's waittimes.
        
        coach_headers = header = {"Authorization":"Basic RFBFQ1AtTU9CSUxFLldEVy5BTkRST0lELVBST0Q6RGhyeHMyZHVReGdiVjZ5Mg==","User-Agent":"CouchbaseLite/1.3 (1.4.1/8a21c5927a273a038fb3b66ec29c86425e871b11)","Content-Type":"application/json","Accept":"multipart/related"}
        headers = {
            'Accept-Language' : 'en_US',
            'User-Agent': 'UIEPlayer/2.1 iPhone OS 6.0.1',
            'Accept' : 'application/json;apiversion=1',
            'Connection' : 'keep-alive',
            'Proxy-Connection' : 'keep-alive',
            'Accept-Encoding' :'compress, gzip',
            'Authorization' :'BEARER ' + self._authorize(),
            'X-Conversation-Id' : 'WDPRO-MOBILE.MDX.CLIENT-PROD',
            'X-Correlation-ID' : str(datetime.datetime.now().timestamp())
        }
        
        channel = 'wdw.facilities.1_0.en_us'
        
        payload = {
            "channels": channel,
            "style": 'all_docs',
            "filter": 'sync_gateway/bychannel',
            "feed": 'normal',
            "heartbeat": 30000
        }
        
        r = requests.post("https://realtime-sync-gw.wdprapps.disney.com/park-platform-pub/_changes?feed=normal&heartbeat=30000&style=all_docs&filter=sync_gateway%2Fbychannel", data=json.dumps(payload), headers = coach_headers)
        s = json.loads(r.text)
        docs = []
        for i in s['results']:
            try:
                i['deleted']
                continue
            except:
                this = {}
                this['id'] = i['id']

                docs.append(this)

                split_id = i['id'].split(":")
                if len(split_id) > 1:
                    this = {}
                    this['id'] = split_id[0]
                    docs.append(this)
        payload = {"docs": docs, "json":True}
        requests.post("https://realtime-sync-gw.wdprapps.disney.com/park-platform-pub/_bulk_get?revs=true&attachments=true", data=json.dumps(payload), headers=coach_headers())
        s = r.text

        cont_reg = re.compile("\w+-\w+:\s\w+\/\w+")
        s = re.sub(cont_reg, "", s)
        s = s.splitlines()
        for x in s:
            if x != '' and x[0] != '-':
                try:
                    x = json.loads(x)
                    c.execute("INSERT INTO sync (id, rev, body, channel) VALUES (?, ?, ?, ?)", (x['_id'], x['_rev'], json.dumps(x), channel,))

                    split_id = x['_id'].split(':')
                    this['id'] = split_id[-1].split(';')[0].split('.')[-1]


                    this['name'] = x['name']
                    this['entityType'] = x['type']

                    try:
                        this['sub'] = x['subType']
                    except:
                        this['sub'] = None

                    this['cb_id'] = x['_id']
                    this['dest_code'] = x['_id'].split('.')[0]

                    try:
                        this['park_id'] = x['ancestorThemeParkId'].split(';')[0]
                    except:
                        try:
                            this['park_id'] = x['ancestorWaterParkId'].split(';')[0]
                        except:
                            this['park_id'] = None

                    try:
                        this['land_id'] = x['ancestorLandId'].split(';')[0]
                    except:
                        this['land_id'] = None

                    try:
                        this['resort_id'] = x['ancestorResortId'].split(';')[0]
                    except:
                        this['resort_id'] = None

                    try:
                        this['ra_id'] = x['ancestorResortAreaId'].split(';')[0]
                    except:
                        this['ra_id'] = None

                    try:
                        this['ev_id'] = x['ancestorEntertainmentVenueId'].split(';')[0]
                    except:
                        this['ev_id'] = None
                except Exception as e:
                    # print(x)
                    # print(e)
                    continue
        ride_link = self._url + '/wait-times'
        page = requests.get(self._url, headers=headers)
        response = requests.get(ride_link, headers=headers)
        print(response)
        
        return page

    def _waitTime(self,attraction_doc, attraction):
        if 'waitTime' in attraction:
            attraction_doc.setOpen()
            attraction_doc.setTime(0)
            if 'status' in attraction['waitTime'] and attraction['waitTime']['status'] == 'Closed':
                attraction_doc.setClosed()
            if 'actualWaitMinutes' in attraction['waitTime']:
                attraction_doc.setTime(attraction['waitTime']['actualWaitMinutes'])
            elif 'postedWaitMinutes' in attraction['waitTime']:
                attraction_doc.setTime(attraction['waitTime']['postedWaitMinutes'])
        else:
            attraction_doc.setClosed()
        

    def _fastPass(self,attraction_doc, attraction):
        if 'waitTime' in attraction:
            if 'fastpass' in attraction['waitTime']:
                attraction_doc.setFastPass(attraction['waitTime']['fastpass'])

    def _singleRider(self,attraction_doc, attraction):
        if 'singleRider' in attraction:
            attraction_doc.setSingleRider(attraction['singleRider'])
        

    def _authorize(self):
        # Returns authorization token

        r = requests.get("https://disneyworld.disney.go.com/authentication/get-client-token")
        response = json.loads(r.content)
        auth_token = response['access_token']
        return auth_token
