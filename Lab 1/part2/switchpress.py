from machine import Pin
import neopixel

p0 = Pin(0, Pin.OUT) # neopixel led
p1 = Pin(2, Pin.OUT) # NEOPIXEL_I2C_POWER
button = Pin(38, Pin.IN) # SW38 push button

# NEOPIXEL_I2C_POWER (GPIO 2) pin that must be set HIGH for
# the NeoPixel LED to work.
p1.value(1)

n = neopixel.NeoPixel(p0, 1)

count = 0

prev_val=0
val=0

while True:
    prev_val = val
    val = button.value()
    
    if(prev_val == 0 and val == 1):
        count = count + 1
        if count > 5:
            break
    if button.value() == 0:
        n[0] = (0, 255, 0)
        n.write()    
    elif button.value()==1:
        n[0] = (255, 0, 0)
        n.write()    

n[0] = (0, 0, 0)
n.write()
print("You have successfully implemented LAB1!")

        


