from omxplayer import OMXPlayer 

def play(path):
    player = OMXPlayer('fromYoutube.mp4') 
    player.play()
    while player.is_playing:
        pass 
    player.quit()

class player(threading.Thread):
    def __init__(self, path):
        threading.Thread.__init__(self)
        self.path = path
    
    def run(self):
        play(self.path)
