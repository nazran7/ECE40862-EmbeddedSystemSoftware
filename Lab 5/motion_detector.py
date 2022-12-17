import neopixel
import time
from machine import RTC
from machine import Timer
import urequests
from machine import Pin
import network

neo_led = Pin(0, Pin.OUT) # neopixel led
neo_power = Pin(2, Pin.OUT) # NEOPIXEL_I2C_POWER
neo_power.value(1)
red_led = Pin(13, Pin.OUT)
red_led.value(0)

#Credits: Andrew Lynn (former ECE40862 student) and Vijay R.
class MPU:
    # Static MPU memory addresses
    ACC_X = 0x3B
    ACC_Y = 0x3D
    ACC_Z = 0x3F
    TEMP = 0x41
    GYRO_X = 0x43
    GYRO_Y = 0x45
    GYRO_Z = 0x47

    def acceleration(self):
        self.i2c.start()
        acc_x = self.i2c.readfrom_mem(self.addr, MPU.ACC_X, 2)
        acc_y = self.i2c.readfrom_mem(self.addr, MPU.ACC_Y, 2)
        acc_z = self.i2c.readfrom_mem(self.addr, MPU.ACC_Z, 2)
        self.i2c.stop()

        # Accelerometer by default is set to 2g sensitivity setting
        # 1g = 9.81 m/s^2 = 16384 according to mpu datasheet
        acc_x = self.__bytes_to_int(acc_x) / 16384 * 9.81
        acc_y = self.__bytes_to_int(acc_y) / 16384 * 9.81
        acc_z = self.__bytes_to_int(acc_z) / 16384 * 9.81

        return acc_x, acc_y, acc_z

    def temperature(self):
        self.i2c.start()
        temp = self.i2c.readfrom_mem(self.addr, self.TEMP, 2)
        self.i2c.stop()

        temp = self.__bytes_to_int(temp)
        return self.__celsius_to_fahrenheit(temp / 340 + 36.53)

    def gyro(self):
        return self.pitch, self.roll, self.yaw

    def __init_gyro(self):
        # MPU must be stationary
        gyro_offsets = self.__read_gyro()
        self.pitch_offset = gyro_offsets[1]
        self.roll_offset = gyro_offsets[0]
        self.yaw_offset = gyro_offsets[2]

    def __read_gyro(self):
        self.i2c.start()
        gyro_x = self.i2c.readfrom_mem(self.addr, MPU.GYRO_X, 2)
        gyro_y = self.i2c.readfrom_mem(self.addr, MPU.GYRO_Y, 2)
        gyro_z = self.i2c.readfrom_mem(self.addr, MPU.GYRO_Z, 2)
        self.i2c.stop()

        # Gyro by default is set to 250 deg/sec sensitivity
        # Gyro register values return angular velocity
        # We must first scale and integrate these angular velocities over time before updating current pitch/roll/yaw
        # This method will be called every 100ms...
        gyro_x = self.__bytes_to_int(gyro_x) / 131 * 0.1
        gyro_y = self.__bytes_to_int(gyro_y) / 131 * 0.1
        gyro_z = self.__bytes_to_int(gyro_z) / 131 * 0.1

        return gyro_x, gyro_y, gyro_z

    def __update_gyro(self, timer):
        gyro_val = self.__read_gyro()
        self.pitch += gyro_val[1] - self.pitch_offset
        self.roll += gyro_val[0] - self.roll_offset
        self.yaw += gyro_val[2] - self.yaw_offset

    @staticmethod
    def __celsius_to_fahrenheit(temp):
        return temp * 9 / 5 + 32

    @staticmethod
    def __bytes_to_int(data):
        # Int range of any register: [-32768, +32767]
        # Must determine signing of int
        if not data[0] & 0x80:
            return data[0] << 8 | data[1]
        return -(((data[0] ^ 0xFF) << 8) | (data[1] ^ 0xFF) + 1)

    def __init__(self, i2c):
        # Init MPU
        self.i2c = i2c
        self.addr = i2c.scan()[0]
        self.i2c.start()
        self.i2c.writeto(0x68, bytearray([107,0]))
        self.i2c.stop()
        print('Initialized MPU6050.')

    # Gyro values will be updated every 100ms after creation of MPU object
        self.pitch = 0
        self.roll = 0
        self.yaw = 0
        self.pitch_offset = 0
        self.roll_offset = 0
        self.yaw_offset = 0
        self.__init_gyro()
        gyro_timer = Timer(3)
        gyro_timer.init(mode=Timer.PERIODIC, callback=self.__update_gyro, period=100)

from machine import SoftI2C, Pin
i2c = SoftI2C(scl=Pin(14), sda=Pin(22))
mpu = MPU(i2c)

print(mpu.acceleration())

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
    
def ifttt_upload_data():
    send_data = {'value1': str(mpu.acceleration()[0] + x_offset), 'value2': str(mpu.acceleration()[1] + y_offset), 'value3': str(mpu.acceleration()[2] + z_offset)}
    req_headers = {'Content-Type': 'application/json'}
    req = urequests.post('https://maker.ifttt.com/trigger/motion_sensor_notification/with/key/bDq-PGLNc56f1X-voe8LXRnC-G01Jj7Sqj6FRgmhP1e', json=send_data, headers=req_headers)
    req.close()


def alarm_state():
    global timer_status
    ts_get = urequests.get('https://api.thingspeak.com/channels/1980469/feeds.json?api_key=QQD318FU5S82ND61&results=2').json()
    ts_data = ts_get['feeds'][1]['field1']
    if ts_data == "1":
        n[0] = (0, 255, 0)
        n.write()
        if timer_status == 1:
            pass
        else:
            tim2.init(period=100,mode=Timer.PERIODIC,callback=lambda t:mpu_read())
            timer_status = 1
    elif ts_data == "0":
        n[0] = (0, 0, 0)
        n.write()
        red_led.value(0)

def mpu_read():
    if ((mpu.acceleration()[0] + x_offset) > 10) or ((mpu.acceleration()[0] + x_offset) < -10) or ((mpu.acceleration()[1] + y_offset) > 10) or ((mpu.acceleration()[1] + y_offset) < -10) or ((mpu.acceleration()[2] + z_offset) > 15) or ((mpu.acceleration()[2] + z_offset) < -15):
        red_led.value(1)
        ifttt_upload_data()
    else:
        red_led.value(0)
         
n = neopixel.NeoPixel(neo_led, 1)

x_offset = -0.7232959
y_offset = 0.2993774
z_offset = 0.706111

final_x = mpu.acceleration()[0] + x_offset
final_y = mpu.acceleration()[1] + y_offset
final_z = mpu.acceleration()[2] + z_offset

print('Calibrated Values: ', '(', final_x, ', ', final_y, ', ', final_z, ')')
print('Calibration Complete.')
timer_status = 0
do_connect()
tim1=Timer(1)
tim2=Timer(2)
tim0=Timer(0)
alarm_state()
tim1.init(period=3000,mode=Timer.PERIODIC,callback=lambda t:alarm_state())

