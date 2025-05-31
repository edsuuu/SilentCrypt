from core.core import Core

class SilentCrypt:
    def __init__(self):
        self.start()
        
    def start(self):
        Core().main()
        print(1)        

if __name__ == "__main__":
    SilentCrypt()