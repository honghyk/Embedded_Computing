import threading
import os, json
import paho.mqtt.client as mqtt
from youtube_util import download_audio 

#설정을 저장하고 있는 json 파일의 절대경로
setting_path = '{}/../settings/settings.json'.format(os.path.dirname(os.path.abspath(__file__)))

#설정을 바꾸는지에 대한 topic을 connect함과 동시에 subscribe
def on_connect(client, userdata, flags, rc): 
    print("setting MQTT Connected with result code "+str(rc)) 
    client.subscribe("action")

#setting을 바꾸는지에 대한 topic이 오면
#json 파일에 payload로 온 설정을 json파일에 write
def on_message(client, userdata, msg): 
    #string 형태의 payload -> dict
    reg_settings = json.loads(msg.payload)
    
    with open(setting_path, 'w', encoding='UTF-8') as setting_file:
        json.dump(reg_settings, setting_file, indent='\t')
    
    with open(setting_path) as json_file:
        settings = json.load(json_file)
        action = settings['action']
        url = settings['url']
        #설정이 유튜브 재생이면 url에 해당하는 오디오 다운로드
        if action == 'youtube':
            yt = 'https://www.youtube.com/' + url
            download_audio(yt)


class mqttThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        try:
            client = mqtt.Client()
            client.on_connect = on_connect 
            client.on_message = on_message 
            client.connect("52.79.58.10", 1883, 60) 
            client.loop_forever()
        
        except KeyboardInterrupt:
            exit()