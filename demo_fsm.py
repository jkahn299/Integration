#!/usr/bin/env python
import time
import numpy
from marvelmind import MarvelmindHedge
from time import sleep
import sys
import math
# from MDD10A import direction, speed
# import math
import RPi.GPIO as GPIO
# from time import sleep
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
PWM1=11
PWM2=12
DIR1=13
DIR2=15
GPIO.setup(PWM1,GPIO.OUT)
GPIO.setup(PWM2,GPIO.OUT)
GPIO.setup(DIR1,GPIO.OUT)
GPIO.setup(DIR2,GPIO.OUT)
p1=GPIO.PWM(PWM1, 1000)
p2=GPIO.PWM(PWM2, 1000)
p1.start(0)
p2.start(0)

global pos

class direction():
	def __init__(self, motor):
		self.m=motor
	def change_direction(self, direction):
		self.d=direction
		if(self.m=="ONE"):
			if self.d=="forward":
				GPIO.output(DIR1, GPIO.HIGH)
			elif self.d=="reverse":
				GPIO.output(DIR1,GPIO.LOW)
		elif self.m=="TWO":
			if self.d=="forward":
				GPIO.output(DIR2,GPIO.LOW)
			elif self.d=="reverse":
				GPIO.output(DIR2,GPIO.HIGH)

class speed():
	def __init__(self):
		self.s=0.0
	def set_motor(self, speed, motor):
		print(self.s)
		if(self.s < speed):	
			self.s=self.s+5
			motor.ChangeDutyCycle(int(self.s))
		elif (self.s > speed):
			self.s=self.s-5
			motor.ChangeDutyCycle(int(self.s))

	def get(self):
		return float(self.s)

def motor_off():
	GPIO.output(DIR1,GPIO.LOW)
	GPIO.output(DIR2,GPIO.LOW)
	p1.ChangeDutyCycle(0)
	p2.ChangeDutyCycle(0)


STATE_LEFT = 0
STATE_BACK = 1
STATE_RIGHT = 2
STATE_FORWARD = 3


MIN_SPEED = 10
MAX_SPEED = 100

RIGHT_ANGLE_TURN_SECS = 3

m1=direction("ONE")
m2=direction("TWO")
s1=speed()
s2=speed()


def turn_left_90():
	m1.change_direction("forward")
	m2.change_direction("reverse")
	s1.set_motor(25, p1)
	s2.set_motor(25, p2)
	time.sleep(RIGHT_ANGLE_TURN_SECS)
	print("turn_left_90")



def main(X, Y):
	run = True
	state = None
	HEDGE = MarvelmindHedge(tty= "/dev/ttyACM0", adr=10, debug=False)
	HEDGE.start()
	pos = HEDGE.position()
	x = pos[1]
	y = pos[2]
	xdiff=X-x
	ydiff=Y-y
	m_i = numpy.sqrt(xdiff*xdiff + ydiff*ydiff)
	print(m_i)

	while True:
		pos = HEDGE.position()
		old_state = state
		x = pos[1]
		y = pos[2]
		print(x)
		print(y)
		xdiff=X-x
		ydiff=Y-y
		m_c = numpy.sqrt(xdiff*xdiff + ydiff*ydiff)
		print(m_c)
		print("Current position: ({}, {})".format(x, y))
		speed = (m_c / m_i) *100
		print("speed magnitude: {}".format(speed))
		s1.set_motor(speed, p1)
		s2.set_motor(speed, p2)
		if X-.5 <= pos[1] <= X+.5 and Y-.5 <= pos[2] <= Y+.5:
			motor_off()
			time.sleep(1.5)
			turn_left_90()
			motor_off()
			break
		
		else:
			print("STATE_FORWARD")
			m1.change_direction("forward")
			m2.change_direction("forward")
			

		time.sleep(1)


if __name__ == '__main__':
	try:
		main(5.7, -3.9)
		print("broken")
		main(8.9, -1.54)
		print("broken2")
		main(4.9, 2.95)
		print("broken3")
		main(1.4, -.5)
		print("fineto")
	except KeyboardInterrupt:
		motor_off()
		HEDGE.stop()
		sys.exit()
