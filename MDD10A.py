import math
import RPi.GPIO as GPIO
from time import sleep
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


class direction():
	def __init__(self):
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
		currentspeed=self.s
		self.s=0.0
	def up(self):
		if self.s<100.0:
			self.s=self.s+10.0
	def down(self):
		if self.s>0.0:
			self.s=self.s-10.0
	def rampdown(self):
		while self.s > 0.0:
			self.s=self.s-10.0
			sleep(.1)
			p1.ChangeDutyCycle(self.s)
			p2.ChangeDutyCycle(self.s)
			if self.s<0:
				self.s=10.0
				p1.ChangeDutyCycle(0)
				p2.ChangeDutyCycle(0)
	def set_motor(self, motor, speed):
		current = math.round(self.s)
		while current != speed:
			sign = (speed - current) / math.abs(speed - current)
			motor.ChangeDutyCycle(current + (1 * sign))
			sleep(0.01)
	def set_left(self, speed):
		self.set_motor(p1, speed)
	def set_right(self, speed):
		self.set_motor(p2, speed)
	def set_both(self, speed):
		self.set_left(speed)
		self.set_right(speed)
	def get(self):
		return float(self.s)
m1=motor("ONE")
m2=motor("TWO")
s1=speed()
s2=speed()
p1.start(0)
p2.start(0)
# p1.ChangeDutyCycle(s1.get())
# p2.ChangeDutyCycle(s2.get())
# while (1):
# 	q = raw_input()
# 	if q=='w':
# 		print("forward")
# 		m1.change_direction("forward")
# 		m2.change_direction("forward")
# 		s1.up()
# 		s2.up()
# 		p1.ChangeDutyCycle(s1.get())
# 		p2.ChangeDutyCycle(s2.get())
# 		print(s1.s)
# 		print(s2.s)
# 		q='z'
# 	if q=='e':
# 		print("rampdown")
# 		s1.rampdown()
# 		s2.rampdown()
# 		p1.ChangeDutyCycle(s1.get())
# 		p2.ChangeDutyCycle(s2.get())
# 		print(s1.s)
# 		print(s2.s)
# 		q='z'
# 	if q=='x':
# 		print("reverse")
# 		m1.change_direction("reverse")
# 		m2.change_direction("reverse")
# 		s1.up()
# 		s2.up()
# 		p1.ChangeDutyCycle(s1.get())
# 		p2.ChangeDutyCycle(s2.get())
# 		print(s1.s)
# 		print(s1.s)
# 		q='z'
# 	if q =='s':
# 		print("slow down")
# 		s1.down()
# 		s2.down()
# 		p1.ChangeDutyCycle(s1.get())
# 		p2.ChangeDutyCycle(s2.get())
# 		print(s1.s)
# 		print(s2.s)
# 	if q=='d':
# 		print("right")
# 		s1.rampdown()
# 		m2.change_direction("reverse")
# 		m1.change_direction("forward")
# 		p1.ChangeDutyCycle(50)
# 		p2.ChangeDutyCycle(50)
# 		q='z'
# 	if q=='a':
# 		print("left")
# 		s2.rampdown()
# 		m2.change_direction("forward")
# 		m1.change_direction("reverse")
# 		p1.ChangeDutyCycle(50)
# 		p2.ChangeDutyCycle(50)
# 		q='z'
# 	if q=='l':
# 		print("low")
# 		p1.ChangeDutyCycle(10)
# 		p2.ChangeDutyCycle(10)
# 		sleep(.3)
# 		p1.ChangeDutyCycle(20)
#                 p2.ChangeDutyCycle(20)
#                 sleep(.3)
#                 p1.ChangeDutyCycle(25)
#                 p2.ChangeDutyCycle(25)
#                 sleep(.3)

# 		q='z'
# 	if q=='m':
# 		print("medium")
# 		p1.ChangeDutyCycle(10)
# 		p2.ChangeDutyCycle(10)
# 		sleep(.3)
# 		p1.ChangeDutyCycle(20)
#                 p2.ChangeDutyCycle(20)
# 		sleep(.3)
# 		p1.ChangeDutyCycle(30)
#                 p2.ChangeDutyCycle(30)
# 		sleep(.3)
# 		p1.ChangeDutyCycle(40)
#                 p2.ChangeDutyCycle(40)
# 		sleep(.3)
# 		p1.ChangeDutyCycle(50)
#                 p2.ChangeDutyCycle(50)
# 		q='z'
# 	if q=='h':
# 		print("high")
# 		p1.ChangeDutyCycle(10)
# 		p2.ChangeDutyCycle(10)
# 		sleep(.3)
# 		p1.ChangeDutyCycle(20)
# 		p2.ChangeDutyCycle(20)
#                 sleep(.3)
#                 p1.ChangeDutyCycle(30)
#                 p2.ChangeDutyCycle(30)
#                 sleep(.3)
#                 p1.ChangeDutyCycle(40)
#                 p2.ChangeDutyCycle(40)
#                 sleep(.3)
#                 p1.ChangeDutyCycle(50)
#                 p2.ChangeDutyCycle(50)
#                 sleep(.3)
#                 p1.ChangeDutyCycle(60)
#                 p2.ChangeDutyCycle(60)
# 		sleep(.3)
#                 p1.ChangeDutyCycle(70)
#                 p2.ChangeDutyCycle(70)
#                 sleep(.3)
#                 p1.ChangeDutyCycle(80)
#                 p2.ChangeDutyCycle(80)

# 		q='z'
