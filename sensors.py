# sensors.py — read all connected sensors on ESP32

import machine
import dht
import time

# --- Pin configuration (adjust for your wiring) ---
PIN_DHT22   = 4    # Temperature + Humidity
PIN_LDR     = 34   # Light (analog)
PIN_PIR     = 5    # Motion (digital)
PIN_MQ135   = 35   # Air quality (analog)
PIN_KY038   = 36   # Sound (analog)

dht_sensor = dht.DHT22(machine.Pin(PIN_DHT22))
pir_pin    = machine.Pin(PIN_PIR, machine.Pin.IN)
adc_light  = machine.ADC(machine.Pin(PIN_LDR))
adc_air    = machine.ADC(machine.Pin(PIN_MQ135))
adc_sound  = machine.ADC(machine.Pin(PIN_KY038))

# ESP32 ADC: 0-4095 → 0-3.3V
adc_light.atten(machine.ADC.ATTN_11DB)
adc_air.atten(machine.ADC.ATTN_11DB)
adc_sound.atten(machine.ADC.ATTN_11DB)

def read_dht():
    try:
        dht_sensor.measure()
        return dht_sensor.temperature(), dht_sensor.humidity()
    except Exception:
        return None, None

def adc_to_lux(raw):
    # Simple linear mapping 0-4095 → 0-1000 lux (calibrate for your LDR)
    return round(raw / 4095 * 1000, 1)

def adc_to_aqi(raw):
    # Rough mapping — calibrate for your MQ-135
    return round(raw / 4095 * 200)

def adc_to_db(raw):
    # Rough mapping — calibrate for your KY-038
    return round(20 + raw / 4095 * 80)

def read_all_sensors():
    temp, hum = read_dht()
    return {
        "temperature": temp,
        "humidity":    hum,
        "light":       adc_to_lux(adc_light.read()),
        "motion":      pir_pin.value() == 1,
        "air_quality": adc_to_aqi(adc_air.read()),
        "sound":       adc_to_db(adc_sound.read()),
        "timestamp":   time.time(),
    }
