from network import LTE
import time
import socket

# Se crea una instancia de la clase LTE
lte = LTE()

# Seteamos la banda en la que vamos a operar (la cual depende de la version de nuestra FiPy, las basicas son: 3, 4, 12, 13, 20, 28) y la apn del operador de nuestra SIM
# APN para android
# APN Personal: datos.personal.com
# APN Claro: igprs.claro.com.ar
# APN Movistar: wap.gprs.unifon.com.ar //// internet.gprs.unifon.com.ar //// mms.gprs.unifon.com.ar
# APN ios
# APN Personal: datos.personal.com
# APN Claro: igprs.claro.com.ar
# APN Movistar: gprs.unifon.com.ar
# Bandas de 4G LTE en Argentina: 2, 4, 5, 7, 8, 28, 66

# Hailitamos la funcionalidad de radio y conectarse a la red LTE autorizada por la tarjeta SIM
# Se inicializa el modem LTE
lte.init()

# Se conecta a la red LTE
lte.attach(band=28, apn="datos.personal.com")
# lte.attach(band=28, apn="igprs.claro.com.ar")

# Se consulta hasta que se conecte a la red
while not lte.isattached():
    # Se espera 0.25 segundos
    time.sleep(0.25)
    print('Conectando a la red LTE...')

# Se obtiene la calidad de la señal
response = lte.send_at_cmd('AT+CSQ')
# Se verifica que la respuesta no sea vacia
if response:
    # Se obtiene el RSSI y la calidad de la señal
    rssi, signal_quality = response.rstrip()[:-2].split(':')[1].split(',')
    # Se imprime el RSSI y la calidad de la señal
    print('RSSI: {} dBm'.format(rssi.strip()))
    print('Signal Quality: {}'.format(signal_quality.strip()))
else:
    # Se imprime un mensaje de error
    print('Error al obtener la calidad de la señal.')

# Se obtiene el IMEI
response = lte.send_at_cmd('AT+CGSN')
# Se verifica que la respuesta no sea vacia
if response:
    # Se imprime el IMEI
    imei = response.strip().rstrip()[:-2]
    print('IMEI: {}'.format(imei.strip()))
else:
    # Se imprime un mensaje de error
    print('Error al obtener el IMEI.')

# Se obtiene la IP
response = lte.send_at_cmd('AT+CGPADDR')
# Se verifica que la respuesta no sea vacia
if response:
    # Se imprime la IP
    response = response.strip().rstrip()[:-2].split(':')[1].split(',')[1].replace('"','').strip()
    print('IP: {}'.format(response))
else:
    # Se imprime un mensaje de error
    print('Error al obtener la IP.')

# Se obtiene el registro
response = lte.send_at_cmd('AT+CREG?')
# Se verifica que la respuesta no sea vacia
if response:
    # Se obtiene el estado del registro y el tipo de registro
    registration_status, registration_type = response.rstrip()[:-2].split(':')[1].split(',')
    # Se imprime el estado del registro y el tipo de registro
    print('Registration Status: {}'.format(registration_status))
    print('Registration Type: {}'.format(registration_type.strip()))
else:
    # Se imprime un mensaje de error
    print('Error al obtener el registro.')

# Se obtiene el nombre del operador
response = lte.send_at_cmd('AT+COPS=?')
# Se verifica que la respuesta no sea vacia
if response:
    # Se obtiene el nombre del operador
    operator_name = response.rstrip()[:-2].split(':')[1].split(',')[2].replace('"','').strip()
    # Se imprime el nombre del operador
    print('Operator Name: {}'.format(operator_name))
else:
    # Se imprime un mensaje de error
    print('Error al obtener el nombre del operador.')

# Se obtiene el numero de telefono
response = lte.send_at_cmd('AT+CNUM')
# Se verifica que la respuesta no sea vacia
if response:
    # Se obtiene el numero de telefono
    number = response.rstrip()[:-2].split(':')[1].replace(',','').strip()
    # Se imprime el numero de telefono
    print('Number: {}'.format(number))

# Se obtiene el estado de la conexion
response = lte.send_at_cmd('AT+CGATT?')
# Se verifica que la respuesta no sea vacia
if response:
    # Se obtiene el estado de la conexion
    connection_status = response.rstrip()[:-2].split(':')[1].strip()
    # Se imprime el estado de la conexion
    print('Connection Status: {}'.format(connection_status))
else:
    # Se imprime un mensaje de error
    print('Error al obtener el estado de la conexion.')

# Se obtiene el nombre del fabricante
response = lte.send_at_cmd('AT+CGMI')
# Se verifica que la respuesta no sea vacia
if response:
    # Se obtiene el nombre del fabricante
    manufacturer_name = response.rstrip()[:-2].strip()
    # Se imprime el nombre del fabricante
    print('Manufacturer Name: {}'.format(manufacturer_name))
else:
    # Se imprime un mensaje de error
    print('Error al obtener el nombre del fabricante.')

# Se obtiene el modelo del dispositivo
response = lte.send_at_cmd('AT+CGMM')
# Se verifica que la respuesta no sea vacia
if response:
    # Se obtiene el modelo del dispositivo
    model = response.rstrip()[:-2].strip()
    # Se imprime el modelo del dispositivo
    print('Model: {}'.format(model))
else:
    # Se imprime un mensaje de error
    print('Error al obtener el modelo del dispositivo.')

# Se obtiene la version del firmware
response = lte.send_at_cmd('AT+CGMR')
# Se verifica que la respuesta no sea vacia
if response:
    # Se obtiene la version del firmware
    firmware_version = response.rstrip()[:-2].strip()
    # Se imprime la version del firmware
    print('Firmware Version: {}'.format(firmware_version))
else:
    # Se imprime un mensaje de error
    print('Error al obtener la version del firmware.')

# Se desconecta de la red LTE
lte.dettach()
    
# Se apaga el modem LTE
lte.deinit()