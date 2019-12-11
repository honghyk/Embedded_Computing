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

    if request.method == 'POST':
        action = request.form.get('action')
        url = request.form.get('url', "")
        payload = {
            'action' : action,
            'url' : url
        }
        for k, v in payload.items():
            status[k] = v
        json_payload = json.dumps(payload)
        print(json_payload)

        mqtt.subscribe("detection")
        mqtt.publish('start_detection', json_payload)
        
        return render_template("register.html", **status)

    else:
        for k, v in payload.items():
            status[k] = v
        mqtt.subscribe("detection")
        return render_template("register.html", **status)


@app.route("/register/lullaby")
def pub_lullaby():
    global payload
    payload = {
        'action' : 'lullaby',
        'url' : ""
    }
    json_payload = json.dumps(payload)
    print(json_payload)
    mqtt.publish('action', json_payload)
    
    return redirect(url_for('start_detection'))


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
    mqtt.publish('action', json_payload)

    return redirect(url_for('start_detection'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
