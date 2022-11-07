import esp32
import machine
from machine import TouchPad, Pin
import network
import ntptime
import neopixel
import time
from machine import RTC
from machine import Timer

neo_led = Pin(0, Pin.OUT) # neopixel led
neo_power = Pin(2, Pin.OUT) # NEOPIXEL_I2C_POWER
neo_power.value(1)
button = Pin(38, Pin.IN) # SW38 push button
t = TouchPad(Pin(15))
wake_switch = Pin(33, mode = Pin.IN)
red_led = Pin(13, Pin.OUT)
UTC_OFFSET = -4 * 60 * 60


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
    


def local_time():
    ntptime.host = 'pool.ntp.org'
    ntptime.settime()
    est_time = time.localtime(time.time()+UTC_OFFSET)
    rtc = RTC()
    rtc.datetime((est_time[0], est_time[1], est_time[2], est_time[6], est_time[3], est_time[4],est_time[5], est_time[7]))
    print_time(rtc.datetime())
    rtc_timer = Timer(1)
    rtc_timer.init(mode=Timer.PERIODIC, period=15000, callback = lambda t:print_time(rtc.datetime()))
    
    
def print_time(date_and_time):
    print("Date: ", "{:02d}".format(date_and_time[1]) + '/' + "{:02d}".format(date_and_time[2]) + '/' + "{:02d}".format(date_and_time[0]))
    print("Time：", "{:02d}".format(date_and_time[4]) + ':' + "{:02d}".format(date_and_time[5]) + ':' + "{:02d}".format(date_and_time[6]) + ' HRS')

def touch_input():
    t.read()
    if t.read() < 200: #touched
        n[0] = (0, 255, 0)
        n.write()
    else:
        n[0] = (0, 0, 0)
        n.write()
        
def sleeper():
    print('I am going to sleep for 1 minute.')
    red_led.value(0)
    machine.deepsleep(60000)
    
esp32.wake_on_ext0(pin = wake_switch, level = esp32.WAKEUP_ANY_HIGH)
if machine.wake_reason() == machine.PIN_WAKE:
    print('Woke up due to EXT0 wakeup.')
if machine.wake_reason() == machine.DEEPSLEEP:
    print("Timer Wakeup")

red_led.value(1)
do_connect()
local_time()

n = neopixel.NeoPixel(neo_led, 1)
touch_timer = Timer(2)
touch_timer.init(mode=Timer.PERIODIC, period=50, callback = lambda t:touch_input())


sleep_timer = Timer(3)
sleep_timer.init(mode=Timer.PERIODIC, period=30000, callback = lambda t:sleeper())




