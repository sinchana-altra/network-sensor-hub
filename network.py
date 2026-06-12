# network.py — WiFi connection + HTTP POST for ESP32 MicroPython

import network as net
import urequests
import ujson
import time

wlan = net.WLAN(net.STA_IF)

def connect_wifi(ssid: str, password: str, timeout: int = 15):
    wlan.active(True)
    if wlan.isconnected():
        print("Already connected:", wlan.ifconfig())
        return

    print(f"Connecting to {ssid}...")
    wlan.connect(ssid, password)

    t = 0
    while not wlan.isconnected() and t < timeout:
        time.sleep(1)
        t += 1
        print(".", end="")

    if wlan.isconnected():
        print("\nConnected! IP:", wlan.ifconfig()[0])
    else:
        print("\nFailed to connect.")

def post_data(url: str, data: dict):
    headers = {"Content-Type": "application/json"}
    body    = ujson.dumps(data)
    resp    = urequests.post(url, data=body, headers=headers)
    resp.close()
