import pycom
import time
import ubinascii
import ujson
import urequests
import math
import airq
import connections

from sensors import Sensors
from machine import Timer
from pycoproc_1 import Pycoproc
from network import Bluetooth

# Bluetooth connecton
bt = Bluetooth()
bt.init(antenna=bt.EXT_ANT)
bt.start_scan(-1)

# Global variable
mac = "-airq"
rssi = 0

MAC1 = 212805600649701
MAC2 = 232505064286148
MAC3 = 150771113716701
MAC4 = 189296944373700
MAC5 = 241490362886364
MAC6 = 46048858581962
MAC7 = 259207203091946
MAC8 = 240453264680149

# Colors indicator led
RED = 0x7f0000
GREEN = 0x007f00
BLUE = 0x00007f
YELLOW = 0x7f7f00
WHITE = 0x7f7f7f
PINK = 0x7f007f
CIAN = 0x007f7f
NO_COLOUR = 0x000000

# Disable hearbeat led
pycom.heartbeat(False)

# Led blink to indicate start
pycom.rgbled(GREEN)
time.sleep(1)
pycom.rgbled(NO_COLOUR)

# Server address and headers
SERVER_ADDRESS = "https://api.tago.io/data"
headers={'Content-Type':'application/json','Authorization':'dfc25f9c-e417-422d-a7b6-b15f860cd8a9'}

print("headers: ", headers)

# Wifi connection
connections.wifi_connection()

# Pycom credentials
py = Pycoproc(Pycoproc.PYSENSE)
pySensor = Sensors(py)

# Sensor data
data_sensor = [
    {
        "variable" : "rssi{}".format(mac),
        "value" : rssi
    },
]

# Sensor rate
rate = {
    'transmission_rate' : 12,
    'sensor' : 6,
    'wifi_rate': 9
}

# Start timer
chrono = Timer.Chrono()

def transmission_handler(alarm):
    print("transmission")
    alarm.cancel()
    alarm = Timer.Alarm(transmission_handler, rate['transmission_rate'], periodic=True)
    chrono.stop()
    send_data()
    chrono.start()

def sensor_handler(alarm):
    print("sensor")
    alarm.cancel()
    alarm = Timer.Alarm(sensor_handler, rate['sensor'], periodic=True)
    chrono.stop()
    data_bt()
    macChange = macSelect(mac)
    print("mac: ", mac)
    data_sensor[0]["variable"] = 'rssi{}'.format(macChange)
    data_sensor[0]["value"] = rssi
    
    print("data_sensor: ", data_sensor)

    chrono.start()

def macSelect(mac):
    if mac == MAC1:
        return 'airq1'
    elif mac == MAC2:
        return 'airq2'
    elif mac == MAC3:
        return 'airq3'
    elif mac == MAC4:
        return 'airq4'
    elif mac == MAC5:
        return 'airq5'
    elif mac == MAC6:
        return 'airq6'
    elif mac == MAC7:
        return 'airq7'
    elif mac == MAC8:
        return 'airq8'
    
def wifi_handler(alarm):
    chrono.stop()
    print("wifi")
    if(connections.check_wifi()):
        alarm.cancel()
        alarm = Timer.Alarm(wifi_handler, rate['wifi_rate'], periodic=True)
        connections.wifi_connection()
        pycom.rgbled(WHITE)
        time.sleep(1)
        pycom.rgbled(NO_COLOUR)
    else:
        pycom.rgbled(PINK)
        time.sleep(1)
        pycom.rgbled(NO_COLOUR)
    chrono.start()

chrono.start()

transmission_alarm = Timer.Alarm(transmission_handler, rate['transmission_rate'], periodic=True)
sensor_rate = Timer.Alarm(sensor_handler, rate['sensor'], periodic=True)
wifi_rate = Timer.Alarm(wifi_handler, rate['wifi_rate'], periodic=True)

alarm_sets = []

alarm_sets.append([transmission_alarm, transmission_handler, 'transmission_rate'])
alarm_sets.append([sensor_rate, sensor_handler, 'sensor'])
alarm_sets.append([wifi_rate, wifi_handler, 'wifi_rate'])

def data_bt():
    global rssi, mac, gas_resistance, pressure, temperature, humidity, voc
    while True:
        adv = bt.get_adv()
        if adv:
            read_adv = bt.resolve_adv_data(adv.data, Bluetooth.ADV_MANUFACTURER_DATA)
            if read_adv == None:
                pass
            else:
                manuf_data = ubinascii.hexlify(read_adv[0:4])
                if(manuf_data == b'4c000215'):
                    rssi = adv.rssi
                    mac = int.from_bytes(adv.mac, "little")
                    uuid_raw = read_adv[4:20]
                    name, gas_resistance, pressure  = airq.byte_to_info(uuid=uuid_raw)
                    if name == "PyN":
                        major = ubinascii.hexlify(read_adv[20:22])
                        minor = ubinascii.hexlify(read_adv[22:24])
                        major_int = int(major, 16)
                        major_f = major_int/100
                        minor_int = int(minor,16)
                        minor_f = minor_int/100
                        temperature = major_f
                        humidity = minor_f
                        voc = airq.air_quality_score(minor_f, gas_resistance)
                        break
        else:
            time.sleep(0.050)

def stored_data():
    store_data = {}
    store_data = data_sensor
    json_store_data = ujson.dumps(store_data)
    return json_store_data

def post_data(address, raw_data):
    print("posting data")
    chrono.stop()
    if(connections.check_wifi()):
        connections.wifi_connection()
        pycom.rgbled(WHITE)
        time.sleep(1)
        pycom.rgbled(NO_COLOUR)
    else:
        pycom.rgbled(PINK)
        time.sleep(1)
        pycom.rgbled(NO_COLOUR)
    response = urequests.post(address, headers=headers, data=raw_data)
    print("response.text: ", response.text)
    chrono.start()
    return response

def get_data(address):
    response = urequests.get(address, headers=headers)
    aux = response.json()
    return aux

def send_data():
    print("sending data")
    try:
        print("mac:", mac)
        if ((mac == MAC1) or (mac == MAC2) or (mac == MAC3) or (mac == MAC4) or (mac == MAC5) or (mac == MAC6) or (mac == MAC7) or (mac == MAC8)):
            print("mac correct")
            response = post_data(SERVER_ADDRESS, stored_data())
            print("Se envio {}".format(mac))
            pycom.rgbled(CIAN)
            time.sleep(1)
            pycom.rgbled(NO_COLOUR)
        else:
            print("mac incorrect")
            pycom.rgbled(BLUE)
            time.sleep(1)
            pycom.rgbled(NO_COLOUR)
    except Exception as e:
        print(e)
        print("POST attempet failed.")
        pycom.rgbled(RED)
        time.sleep(1)
        pycom.rgbled(NO_COLOUR)
    