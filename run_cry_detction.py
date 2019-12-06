import os
import json
import paho.mqtt.client as mqtt
from make_prediction import predict_sound

setting_path = '{}/../settings/settings.json'.format(os.path.dirname(os.path.abspath(__file__)))

def on_connect(client, userdata, flags, rc): 
    print("Connected with result code "+str(rc)) 
    client.subscribe("action")

def on_message(client, userdata, msg): 
    #string 형태의 payload -> dict
    reg_settings = json.loads(msg.payload)
    
    with open(setting_path, 'w', encoding='UTF-8') as setting_file:
        json.dump(reg_settings, setting_file, indent='\t')

def clean_up():
    #재생 되고 있는 사운드가 있으면 stop
    pass

def recording():
    os.system('arecord -D plughw:1,0 -d 9 -f S16_LE -c1 -r44100 -t wav ..recording/signal_9s.wav')
    pass

def predict():
    print('predict...')
    return predict_sound()

def stop_playing(playing):
    if(playing == True):
        playing = False
    
def load_settings():
    with open(setting_path) as json_file:
        settings = json.load(json_file)
    action = settings['action']
    url = settings['url']
    print('in setting json... action : {}, url : {}'.format(action, url))

    return (action, url)


def start_playing(playing):
    if(playing == True):    #이미 자장가 또는 유튜브가 재생 중인 경우
        return
    else:
        print('start playing...')
        action, url = load_settings()
        if action == 'lullaby':
            #play lullaby
            print('play lullaby...')
            os.system('aplay -D plughw:0,0 ../lullaby/lullaby_classic.wav')
        elif action == "youtube":
            youtube_url = "youtube.com" + url
            #play youtube
        playing = True


if __name__ == "__main__":
    playing = False
    try:
        while True:
            #어떤 행동을 취할 지에 대한 setting 정보를 mqtt 데이터로 전달 받음
            client = mqtt.Client()
            client.on_connect = on_connect 
            client.on_message = on_message 
            client.connect("52.79.58.10", 1883, 60) 
            client.loop_forever()
            
            #recording을 멀티 쓰레드로 처리하면 prediction할 때 .wav파일이 없어서 오류 날 수 있음
            #recording - prediction은 sequential 한 과정
            #멀티 쓰레드로 한다면 predict()를 콜백으로??
            recording()
            prediction = predict()
            #아기가 울지 않는 경우
            if(prediction == 0):
                stop_playing(playing)
            #아기가 울고 있는 경우
            elif(prediction == 1):
                start_playing(playing)
    
    except KeyboardInterrupt:
        clean_up()
        exit()