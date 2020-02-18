import time
import numpy
from marvelmind import MarvelmindHedge
from time import sleep
import sys
import math
import pygame
import RPi.GPIO as GPIO

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


MIN_SPEED = 10
MAX_SPEED = 100

RIGHT_ANGLE_TURN_SECS = 5

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

global newEvent1
global newEvent2
newEvent1 = False
newEvent2 = False

axisUpDownInverted = True
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
pygame.display.set_caption("JoyBorg - Press [ESC] to quit")

def Handler(p1, p2, events):
	for event in events:
		if event.type == pygame.QUIT:
			hadEvent = True
			moveQuit = True
		elif event.type == pygame.JOYAXISMOTION:
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
				s1.set_motor(upDown, p1)
				s2.set_motor(upDown, p2)
			elif upDown > 0.1:
				newEvent1 = True
				moveUp = False
				moveDown = True
				s1.set_motor(upDown, p1)
				s2.set_motor(upDown, p2)
			else:
				if(-0.1 <= upDown <= 0.1):
					s1.set_motor(0, p1)
					s2.set_motor(0, p2)
					moveUp = False
					moveDown = False
					MotorOff()
			if leftRight < -0.1:
				newEvent2 = True
				moveLeft = True
				moveRight = False
				s1.set_motor(leftRight, p1)
				s2.set_motor(leftRight, p2)
			elif leftRight > 0.1:
				newEvent2 = True
				moveLeft = False
				moveRight = True
				s1.set_motor(leftRight, p1)
				s2.set_motor(leftRight, p2)
			else:
				if(-0.1 <= leftRight <= 0.1):
					s1.set_motor(0, p1)
					s2.set_motor(0, p2)
					moveLeft = False
					moveRight = False
					MotorOff()

def manual():
	try:
		print 'Press [ESC] to quit'
    # Loop indefinitely
	    while True:
	        # Get the currently pressed keys on the keyboard
	        Handler(pygame.event.get())
	        if hadEvent:
	            # Keys have changed, generate the command list based on keys
	            hadEvent = False
	            if moveQuit:
	                break
	            elif moveLeft:
	                m1.change_direction("forward")
	                m2.change_direction("reverse")
	            elif moveRight:
	                m1.change_direction("reverse")
	                m2.change_direction("forward")
	            elif moveUp:
	                m1.change_direction("forward")
	                m2.change_direction("forward")
	            elif moveDown:
	            	m1.change_direction("reverse")
	                m2.change_direction("reverse")
	            else:
	                motor_off()
	        		time.sleep(interval)
    
    MotorOff()
except KeyboardInterrupt:
    # CTRL+C exit, disable all drives
    MotorOff()

    