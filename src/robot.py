#!/usr/bin/env python

from marvelmind import MarvelmindHedge

class Robot(object):
    def __init__(self):
        self.hedge = MarvelmindHedge(tty="/dev/ttyACM0", adr=10, debug=False)
    def start(self):
        self.hedge.start()
    def stop(self):
        self.hedge.stop()