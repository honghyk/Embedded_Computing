from omxplayer import OMXPlayer
from time import sleep
 
# This will start an `omxplayer` process, this might 
# fail the first time you run it, currently in the 
# process of fixing this though.
player = OMXPlayer('fromYoutube.mp4')
 
# The player will initially be paused
 
player.play()
while player.is_playing:
    pass 
# Kill the `omxplayer` process gracefully.
player.quit()