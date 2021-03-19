from flask import Flask, jsonify, abort, make_response, request
app = Flask(__name__)

app.config.from_object('config.DevConfig')

lights = { 
    "bouncy_pixels_service" : "Lights are flowing through the HAT and bouncing from it's margins.",
    "matrix_service" : "Lights are flowing through the HAT in Matrix fasion.",
    "rainbow_service" : "Lights are flowing through the HAT in rainbow patterns." 
    }

#Routes

@app.route("/")
@app.route("/api")
def hello():
    response = {"message":"This is simple jira API."}
    return jsonify(response)

@app.route("/api/lights")
def list_lights():
    return jsonify(lights)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': '404 - Issue Not found'}), 404)

@app.errorhandler(503)
def not_found(error):
    return make_response(jsonify({'error': '503 - There was an error calling Jira.'}), 503)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
