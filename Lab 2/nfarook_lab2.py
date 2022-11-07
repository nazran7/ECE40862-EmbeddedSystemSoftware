from machine import RTC
from machine import Timer
from machine import ADC
from machine import Pin, PWM

pin_adc = Pin(39, Pin.IN) #adc1 pin
adc = ADC(pin_adc) #Pin A3
button = Pin(38, Pin.IN) # SW38 push button
val = 0
switchpress = 0 #counter for switch presses
adc_timer = Timer(2)
debounce_timer = Timer(3)

year = int(input('Year? '))
month = int(input('Month? '))
day = int(input('Day? '))
weekday = int(input('Weekday? '))
hour = int(input('Hour? '))
minute = int(input('Minute? '))
second = int(input('Second? '))
microsecond = int(input('Microsecond? '))

rtc = RTC()
rtc.datetime((year,month,day,weekday,hour,minute,second,microsecond))

def date_time(date_and_time):
    print('Date -> '+ "{:02d}".format(date_and_time[1]) + '/' + "{:02d}".format(date_and_time[2]) + '/' + "{:02d}".format(date_and_time[0]) + '.' +' Weekday value is ' +"{:01d}".format(date_and_time[3]) + '.')
    print('Time -> ' + "{:02d}".format(date_and_time[4]) + ':' + "{:02d}".format(date_and_time[5]) + ':' + "{:02d}".format(date_and_time[6]))
    
rtc_timer = Timer(1)
rtc_timer.init(mode=Timer.PERIODIC, period=30000, callback = lambda t:date_time(rtc.datetime()))

pwm0 = PWM(Pin(13), freq=10, duty=512)

def adc_in(x):
    global val
    global switchpress
    
    val = adc.read_u16()
    if (switchpress % 2) == 1  and   switchpress >0:
        pwm0.freq(int((val*400/65535)+1))
        #print(switchpress,int(val*400/65535)+1)
        
    elif (switchpress % 2) == 0 and switchpress >0:
        pwm0.duty(int(val/100))
        #print(switchpress,val)
    else:
        pass
        
def switch_pressed(y):
    global switchpress
    global debounce_val
    debounce_timer.init(mode=Timer.ONE_SHOT, period=20, callback=debounce)
    switchpress = switchpress + 1
    
button.irq(handler = switch_pressed, trigger = Pin.IRQ_FALLING) #detect switch press
adc_timer.init(mode=Timer.PERIODIC, period=100, callback=adc_in)

def debounce(z):
    curr_value = button.value()
    if curr_value == button.value():
        return
    else:
        debounce()
        

