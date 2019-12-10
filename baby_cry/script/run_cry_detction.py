import os, time
import json
import paho.mqtt.client as mqtt
import sounddevice as sd
from scipy.io.wavfile import write
from mqttThread import mqttThread
from make_prediction import predict_sound
from omxplayer import OMXPlayer

setting_path = '{}/../settings/settings.json'.format(os.path.dirname(os.path.abspath(__file__)))
recording_path = '{}/../recording/signal_9s.wav'.format(os.path.dirname(os.path.abspath(__file__)))

player = None
playing = False

def clean_up():
    #재생 되고 있는 사운드가 있으면 stop
    stop_playing()


def recording():
    duration = 9
    fs = 44100
    recording = sd.rec((int(duration * fs)), samplerate=fs, channels=1, blocking=True)
    write(recording_path, fs, recording)


def predict():
    print('predict...')
    return predict_sound()


def stop_playing():
    global player
    global playing
    if (player is not None) and (player.is_playing()):
        player.quit()
        playing = False


def playing_done(player, exit_status=15):
    global playing
    if(playing == True):
        playing = False


def load_settings():
    with open(setting_path) as json_file:
        settings = json.load(json_file)
    action = settings['action']
    url = settings['url']
    print('in setting json... action : {}, url : {}'.format(action, url))

    return (action, url)


def start_playing():
    global playing
    if(playing == True):    #이미 자장가 또는 유튜브가 재생 중인 경우
        print('already playing....')
        return
    else:
        print('start playing...')
        action, url = load_settings()
        if action == 'lullaby':
            #play lullaby
            print('play lullaby...')
            player = OMXPlayer('../lullaby/lullaby_classic.wav')
            
        elif action == "youtube":
            #play youtube
            print('play youtube sound...')
            if os.path.exists('./fromYoutube.mp4'):
                player = OMXPlayer('./fromYoutube.mp4')
            else:
                print('downloaded not yet')
                player = OMXPlayer('./fromYoutube.mp4')
            
        player.exitEvent = playing_done
        playing = True
    


if __name__ == "__main__":
    
    connectMqtt = mqttThread()
    connectMqtt.start()
    try:
        while True:
            #recording()
            time.sleep(5)
            prediction = predict()
            print('predicted ... {}'.format(prediction))
            #아기가 울지 않는 경우
            if(prediction == 0):
                stop_playing()
            #아기가 울고 있는 경우
            elif(prediction == 1):
                start_playing()
    
    except KeyboardInterrupt:
        clean_up()
        exit()
