from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

MAX_TIME = 85
DHT11PIN = 7

dht11_val = [0, 0, 0, 0, 0]

def dht11_read_val():
    lststate = "HIGH"
    counter = 0  
    j = 0
    i = 0
    farenheit = 0.0
    for i in range (5):
        dht11_val[i] = 0
    GPIO.setup(DHT11PIN, GPIO.OUT)
    GPIO.output(DHT11PIN, GPIO.LOW)
    # delay(18) milliseconds
    sleep(0.018)
    GPIO.output(DHT11PIN, GPIO.HIGH);
    # delayMicroseconds(40);
    sleep(0.00004)
    GPIO.setup(DHT11PIN, GPIO.IN)
    for i in range (MAX_TIME):
        counter = 0
        while GPIO.input(DHT11PIN) is lststate:
            counter = counter + 1
            # delayMicroseconds(1);
            sleep(0.000001)
            if counter==255:
                break
        lststate = GPIO.input(DHT11PIN)
        if counter == 255:
            break
        # top 3 transistions are ignored
        if (( i >= 4 ) and ( i%2 == 0 )):
            dht11_val[j/8] <<= 1
            if counter > 16:
                dht11_val[j/8] = dht11_val[j/8]  | 1
            j = j + 1
    # verify cheksum and print the verified data
    if(( j >= 40 ) and ( dht11_val[4] == (( dht11_val[0] + dht11_val[1] + dht11_val[2] + dht11_val[3] ) & 0xFF ))):
        farenheit=dht11_val[2]*9./5.+32
        print "Humidity = %d.%d %% Temperature = %d.%d *C (%.1f *F)\n" % (dht11_val[0],dht11_val[1],dht11_val[2],dht11_val[3],farenheit)
    else:
        print "Invalid Data!!\n"

def main():
    print "Interfacing Temperature and Humidity Sensor (DHT11) With Raspberry Pi\n"
    #if(wiringPiSetup()==-1)
        #exit(1)
    while 1:
        dht11_read_val()
        sleep(3)
    return

main()
