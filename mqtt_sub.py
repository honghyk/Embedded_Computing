import paho.mqtt.client as mqtt
import json

def getSettings():
    with open('settings.json') as json_file:
        settings = json.load(json_file)
    
    action = settings['action']
    link = settings['link']
    print(action, link)

def on_connect(client, userdata, flags, rc): 
    print("Connected with result code "+str(rc)) 
    client.subscribe("action")

def on_message(client, userdata, msg): 
    #payload string -> dict
    reg_settings = json.loads(msg.payload)
    
    with open('settings.json', 'w', encoding='UTF-8') as setting_file:
        json.dump(reg_settings, setting_file, indent='\t')


if __name__ == '__main__': 
    try:
        while True:
            client = mqtt.Client()
            client.on_connect = on_connect 
            client.on_message = on_message 
            client.connect("52.79.58.10", 1883, 60) 
            client.loop_forever()
    except KeyboardInterrupt: 
        exit()