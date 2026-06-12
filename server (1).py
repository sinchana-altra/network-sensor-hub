"""
server.py — Receives sensor data from ESP32, stores it, broadcasts via WebSocket
"""
from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO
from database import Database
import time

app = Flask(__name__, template_folder="../dashboard")
sio = SocketIO(app, cors_allowed_origins="*")
db  = Database("sensors.db")

ALERT_RULES = {
    "temperature": {"min": 0,   "max": 35,  "unit": "°C"},
    "humidity":    {"min": 20,  "max": 80,  "unit": "%"},
    "air_quality": {"min": 0,   "max": 100, "unit": "AQI"},
    "sound":       {"min": 0,   "max": 75,  "unit": "dB"},
}

def check_alerts(data: dict) -> list:
    alerts = []
    for field, rule in ALERT_RULES.items():
        val = data.get(field)
        if val is None:
            continue
        if val > rule["max"]:
            alerts.append(f"{field} HIGH: {val}{rule['unit']}")
        elif val < rule["min"]:
            alerts.append(f"{field} LOW: {val}{rule['unit']}")
    if data.get("motion"):
        alerts.append("Motion detected!")
    return alerts

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/data", methods=["POST"])
def receive_data():
    payload = request.json
    if not payload:
        return jsonify({"error": "No data"}), 400

    payload["server_time"] = time.time()
    db.insert(payload)

    alerts = check_alerts(payload)
    payload["alerts"] = alerts
    sio.emit("sensor_update", payload)
    return jsonify({"ok": True, "alerts": alerts})

@app.route("/api/history")
def history():
    limit = int(request.args.get("limit", 50))
    rows  = db.get_recent(limit)
    return jsonify(rows)

@app.route("/api/latest")
def latest():
    row = db.get_latest()
    return jsonify(row or {})

if __name__ == "__main__":
    db.init()
    print("Sensor Hub server → http://localhost:5000")
    sio.run(app, host="0.0.0.0", port=5000, debug=False)
