import threading
import os, json
import paho.mqtt.client as mqtt
from downloadYoutube import downloadVideo
setting_path = '{}/../settings/settings.json'.format(os.path.dirname(os.path.abspath(__file__)))

def on_connect(client, userdata, flags, rc): 
    print("Connected with result code "+str(rc)) 
    client.subscribe("action")

def on_message(client, userdata, msg): 
    #string 형태의 payload -> dict
    reg_settings = json.loads(msg.payload)
    
    with open(setting_path, 'w', encoding='UTF-8') as setting_file:
        json.dump(reg_settings, setting_file, indent='\t')
    
    with open(setting_path) as json_file:
        settings = json.load(json_file)
        action = settings['action']
        url = settings['url']
        if action == 'youtube':
            yt = 'https://www.youtube.com/' + url
            downloadVideo(yt)



class mqttThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        client = mqtt.Client()
        client.on_connect = on_connect 
        client.on_message = on_message 
        client.connect("52.79.58.10", 1883, 60) 
        client.loop_forever()
