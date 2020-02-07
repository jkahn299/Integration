#!/usr/bin/env python
import time
import numpy
from marvelmind import MarvelmindHedge
from time import sleep
import sys
import math
from MDD10A import direction, speed
import math
import RPi.GPIO as GPIO
from time import sleep
# GPIO.setmode(GPIO.BOARD)
# GPIO.setwarnings(False)
# PWM1=11
# PWM2=12
# DIR1=13
# DIR2=15
# GPIO.setup(PWM1,GPIO.OUT)
# GPIO.setup(PWM2,GPIO.OUT)
# GPIO.setup(DIR1,GPIO.OUT)
# GPIO.setup(DIR2,GPIO.OUT)
# p1=GPIO.PWM(PWM1, 1000)
# p2=GPIO.PWM(PWM2, 1000)

global DIR
DIR = direction()
global pos
SPD = speed()

STATE_LEFT = 0
STATE_BACK = 1
STATE_RIGHT = 2
STATE_FORWARD = 3

X_MAX = 10.9
Y_MAX = 5.8

MIN_SPEED = 10
MAX_SPEED = 100

RIGHT_ANGLE_TURN_SECS = 2

m1=motor("ONE")
m2=motor("TWO")
s1=speed()
s2=speed()
p1.start(0)
p2.start(0)

def turn_left_90():
	m1.DIR.change_direction("forward")
	m2.DIR.change_direction("reverse")
	DIR.set_right(20)
	time.sleep(RIGHT_ANGLE_TURN_SECS)
	DIR.set_both(0)
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

	while run:
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
		speed = math.fabs((x * y) / (X_MAX * Y_MAX)) * 100
		if speed < MIN_SPEED:
			speed = MIN_SPEED
		elif speed > MAX_SPEED:
			speed = MAX_SPEED
		print("speed magnitude: {}".format(speed))
		SPD.set_both(speed)
		if X-.5 <= pos[1] <= X+.5 and Y-.5 <= pos[2] <= Y+.5:
			state = STATE_LEFT
			turn_left_90()
			#print("turn_left_90")
			break
		# elif x < 0 and y > 0:
		# 	state = STATE_BACK
		# 	print("STATE_BACK")
		# elif x < 0 and y < 0:
		# 	state = STATE_RIGHT
		# 	print("STATE_RIGHT")
		else:
			state = STATE_FORWARD
			m1.DIR.change_direction("forward")
			m2.DIR.change_direction("forward")
			s1.set_both
			print("STATE_FORWARD")
			# run = False # End loop after driving
		# if state != old_state:
		# 	turn_left_90()
		# if state = done:
		# 	print("here")
		# 	print("Left")
		# 	break
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
		HEDGE.stop()
		sys.exit()
