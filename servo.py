import time
from gpiozero import Servo
import gpiozero

import pigpio


servo1 = 12

pwm = pigpio.pi()
pwm.set_mode(servo1, pigpio.OUTPUT)

pwm.set_PWM_frequency(servo1, 50)


try:
	while True:
		n = input("num")
		pwm.set_servo_pulsewidth(servo1, int(n))
except KeyboardInterrupt:
	pwm.set_PWM_dutycycle(servo1, 0)
	pwm.set_PWM_frequency(servo1, 0)
	
