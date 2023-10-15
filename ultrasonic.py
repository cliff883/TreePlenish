import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


trigger = 14
echo = 15

GPIO.setup(trigger, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

GPIO.output(trigger, 0)
time.sleep(2)
print("starting")

def delay_10us():
	a = 2+2
	return a
	
def distance():
	GPIO.output(trigger, 1)
	delay_10us()
	GPIO.output(trigger, 0)
	
	startTime = time.time()
	endTime = time.time()
	
	while GPIO.input(echo) == 0:
		startTime = time.time()
		
	while GPIO.input(echo) == 1:
		endTime = time.time()
		
	elapsed = endTime - startTime
	distance = (elapsed * 34300) / 2
	
	return distance

try:
	while True:
		dist = distance()
		print("Measured Distance = %.1f cm" % dist)
		time.sleep(1)
except KeyboardInterrupt:
	print("Stopped")
	GPIO.cleanup()
