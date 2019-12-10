import threading
import time
from omxplayer import OMXPlayer 

def play(self):
    player = OMXPlayer('./fromYoutube.mp4') 
    player.play()
    #time.sleep(3)
    print('play fromYoutube4')
    while True:
        print(player.is_playing())
        if self.stop == True:
            break
    print('quit')
    player.quit()

class player(threading.Thread):
    def __init__(self, path, stop):
        threading.Thread.__init__(self)
        self.path = path
        self.stop = stop
    
    def run(self):
        play(self)
