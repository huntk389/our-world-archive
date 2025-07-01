from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load the manifest (master index)
with open("ourworld_manifest.json", "r") as f:
    manifest = json.load(f)

@app.route("/")
def home():
    return "🌍 Our World is live."

@app.route("/manifest", methods=["GET"])
def get_manifest():
    return jsonify(manifest)

@app.route("/file/<path:filename>", methods=["GET"])
def get_file(filename):
    try:
        with open(filename, "r") as f:
            content = f.read()
        return jsonify({"filename": filename, "content": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)