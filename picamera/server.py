from flask import Flask, jsonify, render_template,request
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

@app.route('/update-camera/<int:id>', methods=['PATCH'])
def update_camera(id):
    
    try:
        
        with open(statepath, 'r') as file:
            state = json.load(file)

        
        if id < 0 or id >= len(state['cameras']):
            return jsonify({"error": "Camera ID not found"}), 404

        # Get the camera to be updated
        camera = state['cameras'][id]

        # Get the JSON body with updated fields
        updates = request.json

        # Apply updates to the camera
        for key, value in updates.items():
            if key in camera:
                camera[key] = value
            else:
                return jsonify({"error": f"Invalid property: {key}"}), 400

        # Save the updated data back to the JSON file
        with open(statepath, 'w') as file:
            json.dump(state, file, indent=4)

        return jsonify({"message": "Camera updated successfully", "camera": camera}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
