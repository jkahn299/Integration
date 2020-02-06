#!/usr/bin/env python
import time
import numpy
from marvelmind import MarvelmindHedge
from time import sleep
import sys
import math
# from MDD10A import direction, speed

global HEDGE
HEDGE = MarvelmindHedge(tty= "/dev/ttyACM0", adr=10, debug=False)
HEDGE.start()
# global DIR
# DIR = direction()
# global POS
# SPD = speed()

STATE_LEFT = 0
STATE_BACK = 1
STATE_RIGHT = 2
STATE_FORWARD = 3

X_MAX = 10.9
Y_MAX = 5.8

MIN_SPEED = 10

RIGHT_ANGLE_TURN_SECS = 2

def turn_left_90():
	# # DIR.set_left(-20)
	# # DIR.set_right(20)
	time.sleep(RIGHT_ANGLE_TURN_SECS)
	# DIR.set_both(0)
	print("turn_left_90")


def main():
	run = True
	state = None
	while run:
		old_state = state
		pos = HEDGE.position()
		x = pos[1]
		y = pos[2]
		print("Current position: ({}, {})".format(x, y))
		speed = math.fabs((x * y) / (X_MAX * Y_MAX))
		if speed < MIN_SPEED:
			speed = MIN_SPEED
		print("speed magnitude: {}".format(speed))
		# SPD.set_both(speed)
		if x > 0 and y > 0:
			state = STATE_LEFT
			print("STATE_LEFT")
		elif x < 0 and y > 0:
			state = STATE_BACK
			print("STATE_BACK")
		elif x < 0 and y < 0:
			state = STATE_RIGHT
			print("STATE_RIGHT")
		else:
			state = STATE_FORWARD
			print("STATE_FORWARD")
			# run = False # End loop after driving
		# drive_in_direction(state) # <---- Uncomment me when you have a driving function
		if state != old_state:
			turn_left_90()
		time.sleep(1)


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		HEDGE.stop()
		sys.exit()
