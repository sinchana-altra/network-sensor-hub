# main.py — runs on ESP32 with MicroPython
# Flash MicroPython first: https://micropython.org/download/esp32/

import time
from sensors import read_all_sensors
from network import connect_wifi, post_data

WIFI_SSID     = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"
SERVER_URL    = "http://192.168.1.100:5000/api/data"  # your PC IP
INTERVAL_SEC  = 2

def main():
    print("Sensor Hub starting...")
    connect_wifi(WIFI_SSID, WIFI_PASSWORD)

    while True:
        readings = read_all_sensors()
        print("Readings:", readings)
        try:
            post_data(SERVER_URL, readings)
        except Exception as e:
            print("Send error:", e)
        time.sleep(INTERVAL_SEC)

main()
