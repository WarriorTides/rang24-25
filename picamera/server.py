from flask import Flask, jsonify
import kill
import cameras

# impot state.json file
import json

# read state.json file
with open("state.json") as f:
    data = json.load(f)
    print(data)


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# get State of cameras in json
@app.route("/state", methods=["POST", "GET"])
def get_state():
    with open("state.json") as f:
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
    cameras.startup()
    return jsonify({"status": "done"})

    # return jsonify({"status": "done"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
