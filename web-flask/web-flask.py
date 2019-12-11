from flask import Flask, request, redirect, render_template, url_for
from flask_mqtt import Mqtt
import json
from mqttThread import MqttThread

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = "52.79.58.10"
app.config['MQTT_BROKER_PORT'] = 1883
mqtt = Mqtt(app)

crying = False
payload = {}
status = {}

#라즈베리파이에서 detection 메세지를 보내면 호출되는 callback 함수
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    global crying
    detection = message.payload.decode('ascii')

    if detection == 'True':
        crying = True
    else:
        crying = False
    status['crying'] = crying
    

@app.route("/")
def index():
  return render_template("main.html")


@app.route("/start", methods=['POST', 'GET'])
def start_detection():
    global payload
    global status

    #라즈베리파이에서 울음 소리를 감지했는지에 대한 메세지를 subscribe
    mqtt.subscribe("detection")
    
    #사용자가 start detection버튼을 누르면 post메소드로 action, url 전송
    if request.method == 'POST':
        action = request.form.get('action')
        url = request.form.get('url', "")
        payload = {
            'action' : action,
            'url' : url
        }
        #payload의 내용을 status에 복사
        for k, v in payload.items():
            status[k] = v
        #dictionary를 json 형태의 string으로 변환
        json_payload = json.dumps(payload)
        print(json_payload)

        #라즈베리파이에 사용자가 detection을 시작했다는 메세지 전송
        mqtt.publish('start_detection', json_payload)
        
        return render_template("register.html", **status)

    else:
        for k, v in payload.items():
            status[k] = v
        return render_template("register.html", **status)


#사용자가 설정을 자장가로 변경
@app.route("/register/lullaby")
def pub_lullaby():
    global payload
    payload = {
        'action' : 'lullaby',
        'url' : ""
    }
    json_payload = json.dumps(payload)
    print(json_payload)
    #바뀐 설정을 라즈베리파이에 publish
    mqtt.publish('action', json_payload)
    
    #"ip:port/start" 로 페이지를 다시 이동
    return redirect(url_for('start_detection'))


#사용자가 설정을 유튜브로 변경
@app.route("/register/youtube/<url>")
def pub_youtube(url):
    global payload
    video_tag = request.query_string.decode('ascii')
    payload = {
        'action' : 'youtube',
        'url' : url + '?' + video_tag
    }
    json_payload = json.dumps(payload)
    print(json_payload)
    #바뀐 설정을 라즈베리파이에 publish
    mqtt.publish('action', json_payload)

    return redirect(url_for('start_detection'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
