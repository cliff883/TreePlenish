from cv2 import *
import time
import serial
import requests

import RPi.GPIO as GPIO
import time
import pigpio

GPIO.setmode(GPIO.BCM)

trigger = 14
echo = 15

pwm = pigpio.pi()

servol1 = 19
servol2 = 13
servou1 = 18
servou2 = 12

pwm.set_mode(servol1, pigpio.OUTPUT)
pwm.set_PWM_frequency(servol1, 50)
pwm.set_mode(servol2, pigpio.OUTPUT)
pwm.set_PWM_frequency(servol2, 50)
pwm.set_mode(servou1, pigpio.OUTPUT)
pwm.set_PWM_frequency(servou1, 50)
pwm.set_mode(servou2, pigpio.OUTPUT)
pwm.set_PWM_frequency(servou2, 50)


DISTANCE_THRESHOLD = 25

#CV and ML
url = "http://143.215.91.126:8000/predict"
cam_port = -1

#ultrasonic setup
GPIO.setup(trigger, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

GPIO.output(trigger, 0)
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

def capture_and_save():
	cam = VideoCapture(cam_port)
	result, image = cam.read()

	if result:
		imwrite("/home/raspberry/recycle/image.jpg", image)
	else:
		print("nothing detected")
		exit(0)
	
	return image
	
def send_to_model():
	with open("image.jpg", 'rb') as image_file:
		response = requests.post(url, files={'image': image_file})

	result = response.json()
	
	return result

def set_lower_position(pos):
	if pos == 0: #closed
		pwm.set_servo_pulsewidth(servol1, 950)
		pwm.set_servo_pulsewidth(servol2, 2100)
	elif pos == 1: #45deg
		pwm.set_servo_pulsewidth(servol1, 1200)
		pwm.set_servo_pulsewidth(servol2, 1800)
	else: #open
		pwm.set_servo_pulsewidth(servol1, 1900)
		pwm.set_servo_pulsewidth(servol2, 1100)
		
def set_upper_position(pos):
	if pos == 0: #closed
		pwm.set_servo_pulsewidth(servou1, 2150)
		pwm.set_servo_pulsewidth(servou2, 1000)
	elif pos == 1: #45deg
		pwm.set_servo_pulsewidth(servou1, 1800)
		pwm.set_servo_pulsewidth(servou2, 1350)
	else: #open
		pwm.set_servo_pulsewidth(servou1, 1100)
		pwm.set_servo_pulsewidth(servou2, 1900)

def set_chute_position(pos):
	if pos == 0: #holding for scan
		set_upper_position(0)
		set_lower_position(0)
	elif pos == 1: #first chute
		set_upper_position(1)
		set_lower_position(0)
	elif pos == 2: #second chute
		set_lower_position(1)
		time.sleep(0.25)
		set_upper_position(2)
	else: #bottom chute
		set_lower_position(2)
		time.sleep(0.25)
		set_upper_position(2)



try:
	while True:
		
		#resetting
		set_chute_position(0)
		
		#wait for distance
		dist = 100
		debounce = 0
		while True:
			dist = distance()
			print(dist)
			if dist < 25:
				debounce += 1
			else:
				debounce = 0
			
			if debounce > 1:
				break
			
			time.sleep(0.5)
		
		#let settle
		time.sleep(2)
		
		#caught in 480p
		print("taking picture")
		image = capture_and_save()
		
		#send to model
		print("sending to web")
		res = send_to_model()
		print(res)
			
		#determine result
		category = "trash"
		for key in res.keys():
			category = key
	
		#send to the correct bin
		print(category)
		if category == "bottle":
			set_chute_position(1)
		elif category == "can":
			set_chute_position(2)
		else: 
			set_chute_position(3)
			
		time.sleep(2)
			
				
except KeyboardInterrupt:		
	GPIO.cleanup()
	pwm.set_PWM_dutycycle(servol1, 0)
	pwm.set_PWM_frequency(servol1, 0)
	pwm.set_PWM_dutycycle(servol2, 0)
	pwm.set_PWM_frequency(servol2, 0)
	pwm.set_PWM_dutycycle(servou1, 0)
	pwm.set_PWM_frequency(servou1, 0)
	pwm.set_PWM_dutycycle(servou2, 0)
	pwm.set_PWM_frequency(servou2, 0)









#print("taking picture")
#image = capture_and_save()

#imshow("abcd", image)
#waitKey(0)
#destroyWindow("abcd")

#print("sending to web")
#res = send_to_model()

#print(res)

#time.sleep(5)

