import RPi.GPIO as GPIO
import time, threading, multiprocessing

buzzer_pin = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT) 
GPIO.setwarnings(False)

buzzer_on_flag = False

def init():
    threading.Thread(target=buzzer_thread_func, args=()).start()
    return

def turn_on():
    global buzzer_on_flag
    buzzer_on_flag = True
    return

def turn_off():
    global buzzer_on_flag
    buzzer_on_flag = False
    return

def buzzer_thread_func():
    global buzzer_on_flag
    while 1:
        while buzzer_on_flag:
            GPIO.output(buzzer_pin,GPIO.HIGH)
            time.sleep(0.05) # Delay in seconds
            GPIO.output(buzzer_pin,GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(buzzer_pin,GPIO.HIGH)
            time.sleep(0.05) # Delay in seconds
            GPIO.output(buzzer_pin,GPIO.LOW)
            time.sleep(1)
        time.sleep(0.1)
    return
