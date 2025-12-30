import network
import urequests
import time
import ntptime
from machine import Pin, ADC
import dht

# =========== WiFi Setup ===========
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("Citech_boyHostel - 3/4Th Floor ", "CitHostel_2024")

while not wifi.isconnected():
    print("Connecting to WiFi...")
    time.sleep(1)
print("Connected! IP:", wifi.ifconfig()[0])

# Sync ESP32 time from Internet (UTC base)
try:
    ntptime.settime()
    print("Time synchronized!")
except:
    print("Time sync failed!")

# =========== Sensors ===========
dht_sensor = dht.DHT11(Pin(4))

rain_analog = ADC(Pin(34))
rain_analog.atten(ADC.ATTN_11DB)
rain_analog.width(ADC.WIDTH_12BIT)

API_KEY = "LEKTAFZ35HTSQ85I"
THINGSPEAK_URL = "https://api.thingspeak.com/update"

# Display time in IST (UTC +5:30)
def get_timestamp():
    t = time.localtime(time.time() + 19800)
    return "{:02d}/{:02d}/{} {:02d}:{:02d}:{:02d}".format(
        t[2], t[1], t[0], t[3], t[4], t[5]
    )

# =========== MAIN LOOP ===========
while True:
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        rain = rain_analog.read()
        timestamp = get_timestamp()

        print("\n============================")
        print("Time       :", timestamp)
        print("Temp       :", temp, "°C")
        print("Humidity   :", hum, "%")
        print("Rain ADC   :", rain)

        # Upload only numeric data
        url = (
            THINGSPEAK_URL +
            "?api_key=" + API_KEY +
            "&field1=" + str(temp) +
            "&field2=" + str(hum) +w
            "&field3=" + str(rain)
        )
        response = urequests.get(url)
        print("Uploaded:", response.text)
        response.close()

    except Exception as e:
        print("Error:", e)

    time.sleep(20)  # 1 upload every 20 seconds
