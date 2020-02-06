#!/usr/bin/env python
import time
import numpy
from marvelmind import MarvelmindHedge
from time import sleep
import sys
import math
# from MDD10A import direction, speed


# global DIR
# DIR = direction()
global pos
# SPD = speed()

STATE_LEFT = 0
STATE_BACK = 1
STATE_RIGHT = 2
STATE_FORWARD = 3

X_MAX = 10.9
Y_MAX = 5.8

MIN_SPEED = 10
MAX_SPEED = 100

RIGHT_ANGLE_TURN_SECS = 2

def turn_left_90():
	##DIR.set_left(-20)
	# # DIR.set_right(20)
	time.sleep(RIGHT_ANGLE_TURN_SECS)
	# DIR.set_both(0)
	print("turn_left_90")



def main(X, Y):
	global HEDGE
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
		old_state = state
		x = pos[1]
		y = pos[2]
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
		# SPD.set_both(speed)
		if X-.5 <= pos[1] <= X+.5 and Y-.5 <= pos[2] <= Y+.5:
			state = STATE_LEFT
			print("turn_left_90")
			break
		# elif x < 0 and y > 0:
		# 	state = STATE_BACK
		# 	print("STATE_BACK")
		# elif x < 0 and y < 0:
		# 	state = STATE_RIGHT
		# 	print("STATE_RIGHT")
		else:
			state = STATE_FORWARD
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
		main(5.2, -4.1)
	except KeyboardInterrupt:
		HEDGE.stop()
		sys.exit()
