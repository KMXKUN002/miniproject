#!/usr/bin/python3
"""
Python Practical Template
Keegan Crankshaw
Readjust this Docstring as follows:
Names: Aluwani Malalamabi, Chris Kim
Student Number: MLLALU001, KMXKUN002
Prac: Mini-project
Date: <15/10/2019>
"""

# import Relevant Librares
import RPi.GPIO as GPIO
import smbus
import spidev
import time


#variable initialisations
systemStart = time.time()
timeSinceAlarm = 0
monitoring = True
monitorFrequency = 0
freqArray = [1, 2, 5]
alarmPlaying = False

# Logic that you write



def reset():
    global systemStart

    systemStart = time.time()
    
def freqInc():
    global monitorFrequency

    monitorFrequency = (monitorFrequency+1)%3   

def rtcTime():
    
    #now = datetime.now()
    
    #write_byte_data(addr, 0x02, now.hour)
    #write_byte_data(addr, 0x01, now.minute)
    #write_byte_data(addr, 0x00, now.second)

    #HH = REMEMBER.read_byte_data(addr,0x02)
    #MM = REMEMBER.read_byte_data(addr,0x01)
    #SS = REMEMBER.read_byte_data(addr,0x00)
    
    
    r = time.gmtime()
    print("RTC time | {}:{}:{}".format (r.tm_hour, r.tm_min, r.tm_sec))

def timer():
    """
    global systemHours
    global systemMins
    global systemSecs

    systemSecs +=1
    if (systemSecs==60):
        systemSecs=0
        systemMins+=1
        if (systemMins==60):
            systemMins=0
            systemHours+=1
    
    print("Sys Timer| {}:{}:{}".format(systemHours,systemMins,systemSecs))
    """
    
    global systemStart
    
    t = time.localtime(time.time() - systemStart)
    print ("Sys Timer| {}:{}:{}".format (t.tm_hour, t.tm_min, t.tm_sec))


def alarm():
    global timeSinceAlarm, alarmPlaying, systemStart
    if (alarmPlaying):
        print ("!!!!!! Alarm on !!!!!!")

    age = time.time() - systemStart
    
    dacReading = dacOut()
    if (dacReading > 2.65 or dacReading < 0.65):
        if (age - timeSinceAlarm > 180 or timeSinceAlarm == 0 or age < timeSinceAlarm):
            GPIO.output (6, True)
            alarmPlaying = True


def dismissAlarm():
    global timeSinceAlarm, alarmPlaying, systemStart
    GPIO.output (6, False)
    alarmPlaying = False
    timeSinceAlarm = time.time() - systemStart



def startStop():
    global monitoring
    if monitoring:
        monitoring = False
    else:
        monitoring = True
    
def initGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    #setup of pins
    GPIO.setup(6,GPIO.OUT)
    GPIO.output(6,False)
    GPIO.setup(17,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(27,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(22,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(5, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

    
    #button interrupts
    GPIO.add_event_detect(17,GPIO.FALLING,callback=reset,bouncetime = 200)
    GPIO.add_event_detect(27,GPIO.FALLING,callback=freqInc,bouncetime = 200)
    GPIO.add_event_detect(22,GPIO.FALLING,callback=dismissAlarm,bouncetime = 200)
    GPIO.add_event_detect(5 ,GPIO.FALLING,callback=startStop,bouncetime = 200)


def main():
    global systemStart
    global monitoring
    global monitorFrequency, freqArray
    
    initGPIO()
 
    while monitoring: 
        print("______________________")
        alarm()
        rtcTime()
        timer()
        time.sleep (freqArray[monitorFrequency])
if __name__ == "__main__":
    # Make sure the GPIO is stopped correctly
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print("Exiting gracefully")
        # Turn off your GPIOs here
        GPIO.cleanup()
    except Exception as e:
        GPIO.cleanup()
        print("Some other error occurred")


