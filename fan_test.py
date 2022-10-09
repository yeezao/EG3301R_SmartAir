import time
import RPi.GPIO as GPIO
import program_constants as pc


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pc.RELAY_1_PIN, GPIO.OUT)
GPIO.setup(pc.RELAY_2_PIN, GPIO.OUT)
GPIO.setup(pc.RELAY_3_PIN, GPIO.OUT)

while True:

    GPIO.output(pc.RELAY_1_PIN, GPIO.HIGH)
    GPIO.output(pc.RELAY_2_PIN, GPIO.HIGH)
    GPIO.output(pc.RELAY_3_PIN, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(pc.RELAY_1_PIN, GPIO.LOW)
    GPIO.output(pc.RELAY_2_PIN, GPIO.LOW)
    GPIO.output(pc.RELAY_3_PIN, GPIO.LOW) 
    time.sleep(2)

