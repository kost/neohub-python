import requests
import json
from pprint import pprint

class Neohub:

    def __init__(self, **params):
        self.url = self.getkey(params,"url") #"http://localhost:8009"
        self.devkey = self.getkey(params,"devkey")
        self.vendorid = self.getkey(params,"vendorid")
        self.devicetypeid = self.getkey(params,"devicetypeid")
        self.debug = self.getkey(params,"debug")

        if self.url == None:
            #self.url="http://localhost:8009"
            self.url="https://neohub.co.uk"

        self.token=None


    def pretty_print_POST(self,req):
        print('{}\n{}\n{}\n\n{}'.format(
            '-----------START-----------',
            req.method + ' ' + req.url,
            '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            req.body,
        ))

    def getkey(self, dict, key):
        if key in dict:
            return dict[key]
        return None

    def login(self, username, password):
        params = {
            "USERNAME":username,
            "PASSWORD":password,
            "devkey":self.devkey,
            "vendorid":self.vendorid,
            "devicetypeid":self.devicetypeid
        }
        resp=self.httpreq("/hm_user_login",params)
        #pprint(resp.content)
        if self.debug:
          pprint(resp.content)
        #import code; code.interact(local=dict(globals(), **locals()))
        js=resp.json()
        if "STATUS" in js:
            if js["STATUS"]==1:
                self.username=username
                self.password=password
                self.token=js["TOKEN"]
                self.devices=js["devices"]
                return js

        return resp

    def httppost(self,uri,headers,data):
        req = requests.Request('POST',uri,headers=headers,data=data)
        prepared = req.prepare()
        # del prepared.headers['User-Agent']
        if self.debug:
            self.pretty_print_POST(prepared)
        s = requests.Session()
        r=s.send(prepared)
        if self.debug:
            pprint(r)
        return r

    def httpreq(self, uri, json):
        try:
            r=self.httppost(self.url+uri, headers={}, data=json)
            return r
        except Exception as e:
            raise

    def httpauthreq(self, uri, json):
        params = {
            "token":self.token,
            "devkey":self.devkey,
            "vendorid":self.vendorid,
            "devicetypeid":self.devicetypeid
        }
        params.update(json)
        if self.debug:
          pprint(params)
        r=self.httpreq(uri, params)
        if self.debug:
          pprint(r.text)
        return r

    def jsonreq(self,uri,params):
        r=self.httpauthreq(uri,params)
        if r.status_code==401:
            login(self.username,self.password)
            r2=self.httpauthreq(uri,params)
            return r2.json()
        j=r.json()
        if self.debug:
          pprint(j)
#        if j["STATUS"]==401:
        return j

    def getdevices(self):
        params = {
            "USERNAME": self.username
        }
        return self.jsonreq("/hm_get_devices",params)

    def device_status(self, device_id):
        params = {
            "device_id": device_id
        }
        js=self.jsonreq("/hm_device_status",params)
        return js

    def sendsscommand(self, device_id, command):
        params = {
            "devices": device_id,
            "command": command
        }
        js=self.jsonreq("/hm_ss_multicommand",params)
        return js

    def sendaddcommand(self, devicestat_id,command):
        params = {
            'device_id': devicestat_id,
            'command': command
        }
        return self.jsonreq('/hm_add_command',params)

    def get_temp(self, device_id):
        j=self.device_status(device_id)
        # j['devices'][0]['CURRENT_TEMPERATURE']
        #dh=next(item for item in j["devices"] if item["deviceid"] == device_id)
        dh=j['devices'][0]
        return float(dh['CURRENT_TEMPERATURE'])

    def set_temp(self, devicestat_id,temp):
        tempstr='%.1f' % round(temp,0)
        cmdstr="{'SET_TEMP':["+tempstr+",'"+devicestat_id+"']}"
        return self.sendaddcommand(devicestat_id,cmdstr)

    def away_on(self, devstat_id):
        #cmdstr=json.dumps({'AWAY_ON':[devstat_id]})
        cmdstr="{'AWAY_ON': ['"+devstat_id+"']}"
        return self.sendaddcommand(devstat_id,cmdstr)

    def away_off(self, devstat_id):
        cmdstr="{'AWAY_OFF': ['"+devstat_id+"']}"
        return self.sendaddcommand(devstat_id,cmdstr)

    def frost_on(self, devstat_id):
        cmdstr="{'FROST_ON':['"+devstat_id+"']}"
        return self.sendaddcommand(devstat_id,cmdstr)

    def frost_off(self, devstat_id):
        cmdstr="{'FROST_OFF':['"+devstat_id+"']}"
        return self.sendaddcommand(devstat_id,cmdstr)
