"""
simulator.py — Sends fake sensor data to the server (no ESP32 needed)
Run this alongside server.py for testing.
"""
import requests
import random
import time
import math

SERVER = "http://localhost:5000/api/data"

def fake_reading(t: float) -> dict:
    return {
        "temperature": round(25 + 5 * math.sin(t / 30) + random.uniform(-0.5, 0.5), 1),
        "humidity":    round(60 + 10 * math.cos(t / 45) + random.uniform(-1, 1), 1),
        "light":       round(max(0, 400 + 300 * math.sin(t / 60) + random.uniform(-20, 20))),
        "motion":      random.random() < 0.15,
        "air_quality": round(max(0, 50 + 30 * abs(math.sin(t / 90)) + random.uniform(-5, 5))),
        "sound":       round(30 + random.uniform(0, 50)),
        "timestamp":   time.time(),
    }

if __name__ == "__main__":
    print(f"Sending fake sensor data to {SERVER} every 2s...")
    t = 0
    while True:
        reading = fake_reading(t)
        try:
            resp = requests.post(SERVER, json=reading, timeout=3)
            print(f"[{t:4d}s] Sent → {resp.json()}")
        except Exception as e:
            print(f"Error: {e}")
        t += 2
        time.sleep(2)
