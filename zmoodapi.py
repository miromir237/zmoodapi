import os
from flask import Flask, jsonify, abort, make_response, request, render_template

app = Flask(__name__)

lights = [ 
    {"id": 1, "state": 0, "name": "bouncy_pixel", "service_name": "bouncy_pixel_service.service", "description": "Lights are flowing through the HAT and bouncing from it's margins."},
    {"id": 2, "state": 0, "name": "matrix", "service_name": "matrix_service.service", "description": "Lights are flowing through the HAT in Matrix fasion."},
    {"id": 3, "state": 0, "name": "rainbow", "service_name": "rainbow_service.service", "description": "Lights are flowing through the HAT in rainbow patterns."} 
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

## Check if any of the lights are already running and update lights status accordingly
for unit in systemd.ListUnits():
        found_value = [dictionary for dictionary in lights if dictionary["service_name"] == unit[0]]
        if found_value:
            lights[found_value[0]["id"]-1]["state"] = 1
            
## Routes

@app.route("/")
@app.route("/home")
def home():
    return render_template("zmoodwebui.html", title="Zmood WebUI v0.1");

@app.route("/api")
def hello():
    response = {"message":"This is simple API to controll pimonroni HAT."}
    return jsonify(response)

@app.route("/api/lights")
def get_lights():
    return jsonify(lights)

@app.route("/api/lights/on/<int:light_id>", methods=['GET'])
def set_light_on(light_id):
    # Check if other light is ON and switch it off first
    for l in lights:
        if l["state"] == 1:
            set_light_off(l["id"])
    # Switch ON the light we want
    systemctl("start-unit", lights[light_id-1]["service_name"], "replace")
    lights[light_id-1]["state"] = 1
    response = {"message":"Light " + lights[light_id-1]["name"] + " on."}
    return jsonify(response)

@app.route("/api/lights/off/<int:light_id>", methods=['GET'])
def set_light_off(light_id):
    lights[light_id-1]["state"] = 0
    systemctl("stop-unit", lights[light_id-1]["service_name"], "replace")
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
    app.run()
