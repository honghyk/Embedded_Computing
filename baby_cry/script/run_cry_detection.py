import os, time
import json
import paho.mqtt.client as mqtt
import sounddevice as sd
from scipy.io.wavfile import write
from mqttThread import mqttThread
from make_prediction import predict_sound
from omxplayer import OMXPlayer
import paho.mqtt.publish as publish
from youtube_util import download_audio 

setting_path = '{}/../settings/settings.json'.format(os.path.dirname(os.path.abspath(__file__)))
recording_path = '{}/../recording/signal_9s.wav'.format(os.path.dirname(os.path.abspath(__file__)))
lullaby_path = '{}/../lullaby/lullaby_classic.wav'.format(os.path.dirname(os.path.abspath(__file__)))
yt_path = '{}/../lullaby/from_youtube.mp4'.format(os.path.dirname(os.path.abspath(__file__)))

player = None
playing = False

def clean_up():
    #재생 되고 있는 사운드가 있으면 stop
    stop_playing()


def recording():
    duration = 9    #9초간 녹음
    fs = 44100
    #blocking모드로 rec 함수 실행. 녹음을 완료한 다음에 prediction을 하기 위함
    recording = sd.rec((int(duration * fs)), samplerate=fs, channels=1, blocking=True)
    write(recording_path, fs, recording)

idx = -1
def predict(simulate=False):
    global idx
    print('predict...')
    #시연용 시뮬레이션 하는 경우, 0~9번 파일을 순차적으로 predict
    if simulate:
        idx = idx + 1
        if idx == 6:
            idx = 0
    return predict_sound(idx)


def stop_playing():
    global player
    global playing
    #생성한 omxplayer가 있고, 재생 중이라면 stop
    if playing == True:
        if player is not None:
            player.quit()
            playing = False


def playing_done(player, exit_status=15):
    global playing
    if playing == True:
        playing = False


def load_settings():
    #설정을 저장하고 있는 json 파일로부터 내용을 읽어옴
    with open(setting_path) as json_file:
        settings = json.load(json_file)
    action = settings['action']
    url = settings['url']
    print('in setting json... action : {}, url : {}'.format(action, url))

    return (action, url)


def start_playing():
    global playing
    global player

    if(playing == True):    #이미 자장가 또는 유튜브가 재생 중인 경우
        print('already playing....')
        return
    else:
        print('start playing...')
        action, url = load_settings()
        if action == 'lullaby':
            #play lullaby
            print('play lullaby...')
            player = OMXPlayer(lullaby_path)
            
        elif action == "youtube":
            #play youtube
            print('play youtube sound...')
            player = OMXPlayer(yt_path)
            
        #player가 재생을 끝나면 playing 변수를 False로 바꿔주는 함수를 등록
        player.exitEvent = playing_done
        playing = True
    
def on_connect(client, userdata, flags, rc): 
    #사용자가 detection을 시작하는지 subscribe
    print("start MQTT Connected with result code "+str(rc)) 
    client.subscribe("start_detection")

def on_message(client, userdata, msg): 
    #detction을 시작하면 설정을 바꾸는지 subscribe 하는 mqtt client가 있는 쓰레드를 생성
    connectMqtt = mqttThread()
    connectMqtt.start()
 
    #등록되어 있는 설정을 json 파일로부터 읽어옴
    reg_settings = json.loads(msg.payload)
    
    with open(setting_path, 'w', encoding='UTF-8') as setting_file:
        json.dump(reg_settings, setting_file, indent='\t')        
    
    with open(setting_path) as json_file:
        settings = json.load(json_file)
        action = settings['action']
        url = settings['url']
        if action == 'youtube':
            yt = 'https://www.youtube.com/' + url
            download_audio(yt)

    try:
        while True:
            #recording()
            prediction = predict(simulate=True)
            print('predicted ... {}'.format(prediction))
            #아기가 울지 않는 경우
            if(prediction == 0):
                publish.single("detection", payload=False, hostname="52.79.58.10")
                stop_playing()
            #아기가 울고 있는 경우
            elif(prediction == 1):
                publish.single("detection", payload=True, hostname="52.79.58.10")
                start_playing()
    
    except KeyboardInterrupt:
        clean_up()
        exit()

if __name__ == "__main__":
    try:
        client = mqtt.Client()
        client.on_connect = on_connect 
        client.on_message = on_message 
        client.connect("52.79.58.10", 1883, 60) 
        client.loop_forever()
    
    except KeyboardInterrupt:
        exit()