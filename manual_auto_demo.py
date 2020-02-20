import sys
import time

import RPi.GPIO as GPIO
import numpy
import pygame
import pygame.joystick
import pygame.display
import math
from marvelmind import MarvelmindHedge

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
PWM1 = 11
PWM2 = 12
DIR1 = 13
DIR2 = 15
GPIO.setup(PWM1, GPIO.OUT)
GPIO.setup(PWM2, GPIO.OUT)
GPIO.setup(DIR1, GPIO.OUT)
GPIO.setup(DIR2, GPIO.OUT)
p1 = GPIO.PWM(PWM1, 1000)
p2 = GPIO.PWM(PWM2, 1000)
p1.start(0)
p2.start(0)

global pos

class direction():
    def __init__(self, motor):
        self.m = motor

    def change_direction(self, direction):
        self.d = direction
        if (self.m == "ONE"):
            if self.d == "forward":
                GPIO.output(DIR1, GPIO.HIGH)
            elif self.d == "reverse":
                GPIO.output(DIR1, GPIO.LOW)
        elif self.m == "TWO":
            if self.d == "forward":
                GPIO.output(DIR2, GPIO.LOW)
            elif self.d == "reverse":
                GPIO.output(DIR2, GPIO.HIGH)


class speed():
    def __init__(self):
        self.s = 0.0

    def set_motor(self, speed, motor):
        print(self.s)
        if (self.s < speed):
            self.s = self.s + 5
            motor.ChangeDutyCycle(self.s)
        elif (self.s > speed):
            self.s = self.s - 5
            if self.s < 0:
                self.s = 0
            print('New speed: {}'.format(self.s))
            motor.ChangeDutyCycle(self.s)

    def get(self):
        return float(self.s)


def motor_off():
    GPIO.output(DIR1, GPIO.LOW)
    GPIO.output(DIR2, GPIO.LOW)
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)


MIN_SPEED = 10
MAX_SPEED = 100

RIGHT_ANGLE_TURN_SECS = 5

m1 = direction("ONE")
m2 = direction("TWO")
s1 = speed()
s2 = speed()


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

axisUpDown = 1
axisLeftRight = 3
axisUpDownInverted = False
axisLeftRightInverted = False
pause = 0.1

# pygame.init()
# pygame.joystick.init()
# joystick = pygame.joystick.Joystick(0)
# joystick.init()
# pygame.display.set_caption("JoyBorg - Press [ESC] to quit")

left_y_axis = 1
right_y_axis = 3
joystick_deadzone = 0.15
events = pygame.event.get

def jesses_handler(events, joystick):
    for event in events:
        if event.type == pygame.JOYAXISMOTION:
            left_motor_speed = joystick.get_axis(left_y_axis)
            right_motor_speed = joystick.get_axis(right_y_axis)
            if math.fabs(left_motor_speed) <= joystick_deadzone:
                left_motor_speed = 0
            if math.fabs(right_motor_speed) <= joystick_deadzone:
                right_motor_speed = 0
            left_motor_forward = left_motor_speed > 0
            right_motor_forward = right_motor_speed > 0
            left_motor_speed = math.fabs(left_motor_speed) * 100
            right_motor_speed = math.fabs(right_motor_speed) * 100
            s1.set_motor(left_motor_speed, p1)
            s2.set_motor(right_motor_speed, p2)
            m1.change_direction("forward" if left_motor_forward else "reverse")
            m2.change_direction("forward" if right_motor_forward else "reverse")
            print("left_motor_speed: {}".format(left_motor_speed))
            print("right_motor_speed: {}".format(right_motor_speed))
            print("left_motor_direction: {}".format(left_motor_forward))
            print("right_motor_direction: {}".format(right_motor_forward))


def manual():
    pygame.init()
    pygame.joystick.init()
    pygame.display.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    pygame.display.set_caption("JoyBorg - Press [ESC] to quit")
    try:
        print('Press [ESC] to quit')
        while 1:
            jesses_handler(pygame.event.get(), joystick)
    except KeyboardInterrupt:
        motor_off()


HEDGE = MarvelmindHedge(tty="/dev/ttyACM0", adr=10, debug=False)
HEDGE.start()


def main(X, Y, HEDGE):
    run = True
    state = None
    pos = HEDGE.position()
    x = pos[1]
    y = pos[2]
    xdiff = X - x
    ydiff = Y - y
    m_i = numpy.sqrt(xdiff * xdiff + ydiff * ydiff)
    print(m_i)

    while True:
        pos = HEDGE.position()
        x = pos[1]
        y = pos[2]
        print(x)
        print(y)
        xdiff = X - x
        ydiff = Y - y
        m_c = numpy.sqrt(xdiff * xdiff + ydiff * ydiff)
        print(m_c)
        print("Current position: ({}, {})".format(x, y))
        speed = (m_c / m_i) * 100
        print("speed magnitude: {}".format(speed))
        s1.set_motor(speed, p1)
        s2.set_motor(speed, p2)
        if X - .5 <= pos[1] <= X + .5 and Y - .5 <= pos[2] <= Y + .5:
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

        time.sleep(1)


try:
    manual()
except KeyboardInterrupt:
    motor_off()
    HEDGE.stop()
    sys.exit()
