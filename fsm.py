#!/usr/bin/env python
import time

STATE_LEFT = 0
STATE_BACK = 1
STATE_RIGHT = 2
STATE_FORWARD = 3


def main():
	run = True
	state = None
	while run:
		pos = HEDGE.position()
		x = pos[1], y = pos[2]
		if x > 0 && y > 0:
			state = STATE_LEFT
			print("STATE_LEFT")
		else if x < 0 && y > 0:
			state = STATE_BACK
			print("STATE_BACK")
		else if x < 0 && y < 0:
			state = STATE_RIGHT
			print("STATE_RIGHT")
		else:
			state = STATE_FORWARD
			print("STATE_FORWARD")
			run = False # End loop after driving
		# drive_in_direction(state) # <---- Uncomment me when you have a driving function
		time.sleep(1)

