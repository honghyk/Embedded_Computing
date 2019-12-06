from flask import Flask, render_template
from flask_mqtt import Mqtt
import json

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = "52.79.58.10"
app.config['MQTT_BROKER_PORT'] = 1883
mqtt = Mqtt(app)

@app.route("/")
def index():
  return "Hello Embedded"

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register/lullaby")
def pub_lullaby():
    print('pub lullaby')
    payload = {
        'action' : 'lullaby',
        'url' : ""
    }
    json_payload = json.dumps(payload)
    print(json_payload)
    mqtt.publish('action', json_payload)

    return "registered"

@app.route("/register/youtube/<url>")
def pub_youtube(url):
    video_tag = request.query_string.decode('ascii')
    payload = {
        'action' : 'youtube',
        'url' : url + '?' + video_tag
    }
    json_payload = json.dumps(payload)
    print(json_payload)
    mqtt.publish('action', json_payload)

    return "registered"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
