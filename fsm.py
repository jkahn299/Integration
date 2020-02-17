#!/usr/bin/env python
import time
import numpy
from marvelmind import MarvelmindHedge
from time import sleep
import sys
import math
import pygame

# from MDD10A import direction, speed
# import math
import RPi.GPIO as GPIO
# from time import sleep
GPIO.setmode(GPIO.BCM)
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




# global DIR
# DIR = direction()



class Motor():
	def __init__(self, motor):
		self.m = motor
	def direction(self, direction):
		self.d = direction
		if(self.m == "ONE"):
			if(self.d == "forward"):
				GPIO.output(DIR1, GPIO.HIGH)
			elif(self.d == "reverse"):
				GPIO.output(DIR1, GPIO.LOW)
		elif(self.m == "TWO"):
			if(self.d == "forward"):
				GPIO.output(DIR2, GPIO.HIGH)
			elif(self.d == "reverse"):
				GPIO.output(DIR2, GPIO.LOW)




def direction(direction):
	if(direction == "forward"):
		m1.direction("forward")
		m2.direction("forward")
		print("##### Direction #####")
		print("Forward")
		print("HIGH Motor1: ", s1.x)
		print("LOW Motor2: ", s2.x)
	elif(direction == "reverse"):
		m1.direction("reverse")
		m2.direction("reverse")
		print("##### Direction #####")
		print("Reverse")
		print("LOW Motor1: ", s1.x)
		print("HIGH Motor2: ", s2.x)
	elif(direction == "left"):
		m1.direction("forward")
		m2.direction("Reverse")
		print("##### Direction #####")
		print("Left")
		print("HIGH Motor1: ", s1.x)
		print("LOW Motor2: ", s2.x)
	elif(direction == "right"):
		m1.direction("reverse")
		m2.direction("forward")
		print("##### Direction #####")
		print("Right")
		print("LOW Motor1: ", s1.x)
		print("HIGH Motor2: ", s2.x)

global newEvent1
global newEvent2
newEvent1 = False
newEvent2 = False




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

m1=Motor("ONE")
m2=Motor("TWO")
s1=speed()
s2=speed()
p1.start(0)
p2.start(0)



 # function to turn off motor
def motor_off():
	GPIO.output(DIR1,GPIO.LOW)
	GPIO.output(DIR2,GPIO.LOW)
	p1.ChangeDutyCycle(0)
	p2.ChangeDutyCycle(0)



axisUpDownInverted = True ##Set true if u/d swapped
axisLeftRightInverted = False
pause = 0.1



global moveUp
global moveDown
global moveDone
global moveLeft
global moveRight

moveUp = False
moveDown = False
moveDone = False
moveLeft = False
moveRight = False

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
screen = pygame.display.set_mode([300,300])
pygame.display.set_caption("JoyBorg - Press [ESC] to quit")

def Handler(leftRight, upDown, speedfactor):
	#print(upDown)
	#print(leftRight)
	global hadEvent
	global newEvent1
	global newEvent2
	global moveUp
	global moveDown
	global moveDone
	global moveLeft
	global moveRight
	for event in events:
		if event.type == pygame.QUIT:
			hadEvent = True
			moveQuit = True
		elif event.type == pygame.JOYAXISMOTION:
# A joystick has been moved, read axis positions (-1 to +1)
            hadEvent = True
            upDown = joystick.get_axis(axisUpDown)
            leftRight = joystick.get_axis(axisLeftRight)
			if axisUpDownInverted:
				upDown = -upDown
			if axisLeftRightInverted:
				leftRight = -leftRight
			if upDown < -0.1:
				newEvent1 = True
				moveUp = True
				moveDown = False
				s1.reValue(upDown, speedfactor)
				s2.reValue(upDown, speedfactor)
				p1.ChangeDutyCycle(s1.get())
				p2.ChangeDutyCycle(s2.get())
			elif upDown > 0.1:
				newEvent1 = True
				moveUp = False
				moveDown = True
				s1.reValue(upDown, speedfactor)
				s2.reValue(upDown, speedfactor)
				p1.ChangeDutyCycle(s1.get())
				p2.ChangeDutyCycle(s2.get())
			else:
				if(-0.1 <= upDown <= 0.1):
					s1.reValue(0, speedfactor)
					s2.reValue(0, speedfactor)
					p1.ChangeDutyCycle(s1.get())
					p2.ChangeDutyCycle(s2.get())
				moveUp = False
				moveDown = False
				MotorOff()
			if leftRight < -0.1:
				newEvent2 = True
				moveLeft = True
				moveRight = False
				s1.reValue(leftRight, speedfactor)
				s2.reValue(leftRight, speedfactor)
				p1.ChangeDutyCycle(s1.get())
				p2.ChangeDutyCycle(s2.get())
			elif leftRight > 0.1:
				newEvent2 = True
				moveLeft = False
				moveRight = True
				s1.reValue(leftRight, speedfactor)
				s2.reValue(leftRight, speedfactor)
				p1.ChangeDutyCycle(s1.get())
				p2.ChangeDutyCycle(s2.get())
			else:
				if(-0.1 <= leftRight <= 0.1):
					s1.reValue(0, speedfactor)
					s2.reValue(0, speedfactor)
					p1.ChangeDutyCycle(s1.get())
					p2.ChangeDutyCycle(s2.get())
				moveLeft = False
				moveRight = False
				#newEvent2 = False
				MotorOff()


#STATE_LEFT = 0
#STATE_BACK = 1
#STATE_RIGHT = 2
#STATE_FORWARD = 3

#MIN_SPEED = 10
MAX_SPEED = 100

RIGHT_ANGLE_TURN_SECS = 2





def main(X, Y, HEDGE):
	global newEvent1
	global newEvent2
	newEvent1 = False
	newEvent2 = False
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
	try:
		Degrees = numpy.arctan(xdiff/ydiff) * 180 / numpy.pi 

	except ZeroDivisionError:
		degrees = 0

	Print('press ctrl+c to quit')

	while run:
		try:
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
				time.sleep(1.5)
				break
		
			else:
				print("STATE_FORWARD")
				m1.change_direction("forward")
				m2.change_direction("forward")

			Handler(newX, newY, speedfactor)
			if newEvent1:
					newEvent1 = False
					if moveUp:
						direction("forward")
					elif moveDown:
						direction("reverse")
					else:
						MotorOff()
			if newEvent2:
					newEvent2 = False
					if moveLeft:
						direction("left")
					elif moveRight:
						direction("right")
					else:
						MotorOff()

			time.sleep(1)
		except KeyboardInterrupt:
			print("interrupted")
			MotorOff()
			pwm1.stop()
			pwm2.stop()





		# speed = math.fabs((x * y) / (X_MAX * Y_MAX)) * 100
		# if speed < MIN_SPEED:
		# 	speed = MIN_SPEED
		# elif speed > MAX_SPEED:
		# 	speed = MAX_SPEED
		# print("speed magnitude: {}".format(speed))
		# # SPD.set_both(speed)
		# if X-.5 <= pos[1] <= X+.5 and Y-.5 <= pos[2] <= Y+.5:
		# 	state = STATE_LEFT
		# 	turn_left_90()
		# 	#print("turn_left_90")
		# 	break
		# # elif x < 0 and y > 0:
		# # 	state = STATE_BACK
		# # 	print("STATE_BACK")
		# # elif x < 0 and y < 0:
		# # 	state = STATE_RIGHT
		# # 	print("STATE_RIGHT")
		# else:
		# 	state = STATE_FORWARD
		# 	# m1.DIR.change_direction("forward")
		# 	# m2.DIR.change_direction("forward")
		# 	# s1.set_both
		# 	print("STATE_FORWARD")
		# 	# run = False # End loop after driving
		# # if state != old_state:
		# # 	turn_left_90()
		# # if state = done:
		# # 	print("here")
		# # 	print("Left")
		# # 	break
		# time.sleep(1)

# try:
# 	main(5.7, -4.2, HEDGE)
# 	print("broken")
# 	main(8.5, -1.7, HEDGE)
# 	print("broken2")
# 	main(4.5, 2.5, HEDGE)
# 	print("broken3")
# 	main(2.3, .1, HEDGE)
# 	print("fineto")
# except KeyboardInterrupt:
# 	motor_off()
# 	HEDGE.stop()
# 	sys.exit()
# if __name__ == '__main__':
# 	try:
# 		main(5.7, -3.9)
# 		print("broken")
# 		main(8.9, -1.54)
# 		print("broken2")
# 		main(4.9, 2.95)
# 		print("broken3")
# 		main(1.4, -.5)
# 		print("fineto")
# 	except KeyboardInterrupt:
# 		HEDGE.stop()
# 		sys.exit()
