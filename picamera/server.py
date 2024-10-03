from flask import Flask, jsonify, render_template
from flask_cors import CORS
import kill
import cameras
import os
import json

# read state.json file
dir_path = os.path.dirname(os.path.realpath(__file__))

statepath = str(os.path.join(dir_path, "state.json"))
print(statepath)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/")
def main():
    return render_template("index.html")

# get State of cameras in json
@app.route("/state", methods=["POST", "GET"])
def get_state():
    with open(statepath) as f:
        data = json.load(f)
        print(data)
        return jsonify(data)

@app.route("/getProcesses", methods=["POST", "GET"])
def getProcesses():
    return jsonify(kill.getProcesses())

@app.route("/killCameras", methods=["POST"])
def killCameras():
    state = kill.killCameras()
    return jsonify({"status": state})

@app.route("/startup", methods=["POST"])
def startup():
    kill.killCameras()
    cameras.startup()
    return jsonify({"status": "done"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
