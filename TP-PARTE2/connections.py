import machine
import time

from network import WLAN, LTE, Bluetooth

def wifi_connection():
    wlan = WLAN(mode=WLAN.STA)
    wlan.antenna(WLAN.EXT_ANT)
    try:
        nets = wlan.scan()
        for net in nets:
            if net.ssid == "prueba":
                print('Network found0!')
                wlan.connect('prueba', auth=(WLAN.WPA2, 'prueba123'), timeout=5000)
                while not wlan.isconnected():
                    machine.idle()
                print('conection to prueba!')
                break
            # elif net.ssid == "LCD":
            #     print('Network found!')
            #     wlan.connect('LCD', auth=(WLAN.WPA2, '1cdunc0rd0ba'))
            #     while not wlan.isconnected():
            #         machine.idle()
            #     print('conection to LCD!')
            #     break
            elif net.ssid == "Auditorium PLM":
                print('Network found1!')
                wlan.connect('Auditorium PLM', auth=None, timeout=5000)
                while not wlan.isconnected():
                    machine.idle()
                print('conection to Auditorium PLM!')
                break
            elif net.ssid == "FCEFyN":
                print('Network found2!')
                wlan.connect('FCEFyN', auth=None, timeout=5000)
                while not wlan.isconnected():
                    machine.idle()
                print('conection to FCEFyN!')
                break
            elif net.ssid == "RAYADOS 2.4":
                print('Network found3!')
                wlan.connect('RAYADOS 2.4', auth=(WLAN.WPA2, 'Rayaplasencia1996'), timeout=10000)
                while not wlan.isconnected():
                    machine.idle()
                print('conection to RAYADOS 2.4!')
                break
    except Exception as e:
        print('Connection failed!')
        print(e)
        wifi_connection()
        
def check_wifi():
    wlan = WLAN(mode=WLAN.STA)
    wlan.antenna(WLAN.EXT_ANT)
    if not wlan.isconnected():
        print('wifi not connected')
        wlan.disconnect()
        return True
    else:
        print('wifi connected')
        return False

def lte_connection():
    lte = LTE()
    # lte.attach(band=28, apn="datos.personal.com")
    lte.attach(band=28, apn="igprs.claro.com.ar")
    while not lte.isattached():
        time.sleep(0.25)
    lte.connect()
    while not lte.isconnected():
        time.sleep(0.25)
    print('LTE connection succeeded!')

def bluetooth_connection():
    bt = Bluetooth()
    bt.init(antenna=bt.EXT_ANT)
    bt.start_scan(-1)
    aux=bt.get_adv()
    return aux

def headers():
    header_dict = {
        'Content-Type': 'application/json',
        'Authorization': 'dfc25f9c-e417-422d-a7b6-b15f860cd8a9'
    }
    return 'headers: {}'.format(header_dict)
