import vlc, pafy

def play(link):
    url = link
    video = pafy.new(url)
    best = video.getbest()
    media = vlc.MediaPlayer(best.url)
    media.play()
    print('play start...')
    try:
        while True:
            if media.get_state() == 6:
                exit()
    except KeyboardInterrupt:
        exit()        
