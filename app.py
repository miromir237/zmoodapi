from flask import Flask, jsonify, abort, make_response, request
app = Flask(__name__)

app.config.from_object('config.DevConfig')

lights = [ 
    {"id": 1, "state": 0, "name": "bouncy_pixel_service.service", "description": "Lights are flowing through the HAT and bouncing from it's margins."},
    {"id": 2, "state": 0, "name": "matrix_service.service", "description": "Lights are flowing through the HAT in Matrix fasion."},
    {"id": 3, "state": 0, "name": "rainbow_service.service", "description": "Lights are flowing through the HAT in rainbow patterns."} 
]

## Systemctl
from pydbus import SystemBus

bus = SystemBus()

systemd = bus.get(".systemd1")
#systemd = bus.get("org.freedesktop.systemd1")

manager = systemd[".Manager"]
#manager = systemd["org.freedesktop.systemd1.Manager"]
#manager = systemd # works but may break if systemd adds another interface

import sys

def systemctl(cmd, *name):
    try:
        command = cmd
        command = "".join(x.capitalize() for x in command.split("-"))
        result = getattr(manager, command)(*name)
    except Exception as e:
        print(e)

## Routes

@app.route("/")
@app.route("/api")
def hello():
    response = {"message":"This is simple jira API."}
    return jsonify(response)

@app.route("/api/lights")
@app.route("/api/lights/all")
def get_lights():
    return jsonify(lights)

@app.route("/api/lights/on/<int:light_id>", methods=['GET'])
def set_light_on(light_id):
    # Check if other light is ON and switch it off first
    for l in lights:
        if l["state"] == 1:
            set_light_off(l["id"])
    # Switch ON the light we want
    systemctl("start-unit", lights[light_id-1]["name"], "replace")
    lights[light_id-1]["state"] = 1
    response = {"message":"Light " + lights[light_id-1]["name"] + " on."}
    return jsonify(response)

@app.route("/api/lights/off/<int:light_id>", methods=['GET'])
def set_light_off(light_id):
    lights[light_id-1]["state"] = 0
    systemctl("stop-unit", lights[light_id-1]["name"], "replace")
    response = {"message":"Light " + lights[light_id-1]["name"] + " off."}
    return jsonify(response)

@app.route("/api/lights/off")
def set_lights_off():
    for l in lights:
        set_light_off(l["id"])
    response = {"message":"Lights turned off."}
    return jsonify(response)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': '404 - Not found'}), 404)

@app.errorhandler(503)
def not_found(error):
    return make_response(jsonify({'error': '503 - There was an error.'}), 503)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
