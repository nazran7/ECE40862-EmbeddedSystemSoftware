import esp32
import machine
from machine import Pin
import network
import socket

# Global variables
temp = 0 # measure temperature sensor data
hall = 0 # measure hall sensor data
red_led_state = '' # string, check state of red led, ON or OFF

red_led = Pin(13, Pin.OUT)

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

def web_page():
    """Function to build the HTML webpage which should be displayed
    in client (web browser on PC or phone) when the client sends a request
    the ESP32 server.
    
    The server should send necessary header information to the client
    (YOU HAVE TO FIND OUT WHAT HEADER YOUR SERVER NEEDS TO SEND)
    and then only send the HTML webpage to the client.
    
    Global variables:
    temp, hall, red_led_state
    """
    temp = str(esp32.raw_temperature())
    hall = str(esp32.hall_sensor())
    if red_led.value() == 1:
        red_led_state="ON"
    else:
        red_led_state="OFF"
        
    html_webpage = """<!DOCTYPE HTML><html>
    <head>
    <title>ESP32 Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
    html {
     font-family: Arial;
     display: inline-block;
     margin: 0px auto;
     text-align: center;
    }
    h1 { font-size: 3.0rem; }
    p { font-size: 3.0rem; }
    .units { font-size: 1.5rem; }
    .sensor-labels{
      font-size: 1.5rem;
      vertical-align:middle;
      padding-bottom: 15px;
    }
    .button {
        display: inline-block; background-color: #e7bd3b; border: none; 
        border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none;
        font-size: 30px; margin: 2px; cursor: pointer;
    }
    .button2 {
        background-color: #4286f4;
    }
    </style>
    </head>
    <body>
    <h1>ESP32 WEB Server</h1>
    <p>
    <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="sensor-labels">Temperature</span> 
    <span>"""+str(temp)+"""</span>
    <sup class="units">&deg;F</sup>
    </p>
    <p>
    <i class="fas fa-bolt" style="color:#00add6;"></i>
    <span class="sensor-labels">Hall</span>
    <span>"""+str(hall)+"""</span>
    <sup class="units">V</sup>
    </p>
    <p>
    RED LED Current State: <strong>""" + red_led_state + """</strong>
    </p>
    <p>
    <a href="/?red_led=on"><button class="button">RED ON</button></a>
    </p>
    <p>
    <a href="/?red_led=off"><button class="button button2">RED OFF</button></a>
    </p>
    </body>
    </html>"""
    return html_webpage

do_connect()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  cnct, addr = s.accept()
  req = cnct.recv(1024)
  req = str(req)
  led_on = req.find('/?red_led=on')
  led_off = req.find('/?red_led=off')
  if led_on == 6:
    red_led.value(1)
  if led_off == 6:
    red_led.value(0)
  response = web_page()
  cnct.send('HTTP/1.1 200 OK\n')
  cnct.send('Content-Type: text/html\n')
  cnct.send('Connection: close\n\n')
  cnct.sendall(response)
  cnct.close()

# used resources from https://randomnerdtutorials.com/esp32-esp8266-micropython-web-server/


