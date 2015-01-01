#!/usr/bin/python
import time
import RPi.GPIO as GPIO

# Common Anode RGB-LED ( Anode = Active High )
RGB_ENABLE = 1
RGB_DISABLE = 0
 
# RGB LED Configuration - Set GPIO Ports
RGB_RED = 11   # GPIO 17
RGB_GREEN = 13 # GPIO 27 Rev2
RGB_BLUE = 15  # GPIO 22
RGB = [RGB_RED,RGB_GREEN,RGB_BLUE]
 
def setup():
    GPIO.setwarnings(False)  
    GPIO.setmode(GPIO.BOARD)
    for GPIO_num in RGB:
        GPIO.setup(GPIO_num, GPIO.OUT)
 
def activate(colour):
    GPIO.output(colour, RGB_ENABLE)
 
def deactivate(colour):
    GPIO.output(colour,RGB_DISABLE)
 
def clear():
    for GPIO_num in RGB:
        GPIO.output(GPIO_num, RGB_DISABLE)

def cleanup():
    GPIO.cleanup()

def test():
    setup()
    clear()
    activate(RGB_RED)
    time.sleep(5)
    deactivate(RGB_RED)
    activate(RGB_GREEN)
    time.sleep(5)
    deactivate(RGB_GREEN)
    activate(RGB_BLUE)
    time.sleep(5)
    deactivate(RGB_BLUE)
    clear()
    GPIO.cleanup()
 
#main()
