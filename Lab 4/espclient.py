import esp32
import machine
from machine import Pin
import network
from machine import Timer
import socket

def do_connect():
    ssid_name = 'Nazran' #insert wifi name here
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid_name, 'bean1234')
        while not sta_if.isconnected():
            pass
    #print('network config:', sta_if.ifconfig())
    print('Connected to', ssid_name)
    print('IP Address: ', sta_if.ifconfig()[0])
    
def sensor_data(ctr):
    temp = str(esp32.raw_temperature())
    hall = str(esp32.hall_sensor())
    print('Temperature: ' + temp)
    print('Hall: ' + hall)
    s = socket.socket()
    s.connect(socket.getaddrinfo('api.thingspeak.com', 80)[0][-1])
    s.send('GET https://api.thingspeak.com/update?api_key=2X5IAEG5OJINB643&field1=' + temp +'&field2='+ hall+'\r\n')
    ctr += 1
    if ctr >= 9:
        sensor_timer.deinit()
        s.close()
        
ctr = 0
do_connect()
sensor_timer = Timer(1)
sensor_timer.init(mode=Timer.PERIODIC, period=30000, callback = lambda t:sensor_data(ctr))

# API key: 2X5IAEG5OJINB643


