import threading
import time

class State(object):
    FORWARD1=1
    LEFT1=2
    FORWARD2=3
    LEFT2=4


class Schmedge(threading.Thread):
    def __init__(self):
        super(Schmedge, self).__init__()
        self._x = 2.3
        self._y = 0.1
        self._state = State.FORWARD1

    def position(self):
        return None, self._x, self._y

    def run(self):
        while True:
            self._x = round(self._x, 1)
            self._y = round(self._y, 1)
            time.sleep(0.3)
            if self._state == State.FORWARD1:
                if self._x == 5.7 and self._y == -4.2:
                    self._state = State.LEFT1
                    continue
                if self._x < 5.7:
                    self._x += 0.1
                elif self._x > 5.7:
                    self._x -= 0.1
                if self._y > -4.2:
                    self._y -= 0.1
                elif self._y < -4.2:
                    self._y += 0.1
            elif self._state == State.LEFT1:
                if self._x == 8.5 and self._y == -1.7:
                    self._state = State.FORWARD2
                    continue
                if self._x < 8.5:
                    self._x += 0.1
                elif self._x > 8.5:
                    self._x -= 0.1
                if self._y < -1.7:
                    self._y += 0.1
                elif self._y > -1.7:
                    self._y -= 0.1
            elif self._state == State.FORWARD2:
                if self._x == 4.5 and self._y == 2.5:
                    self._state = State.LEFT2
                    continue
                if self._x > 4.5:
                    self._x -= 0.1
                elif self._x < 4.5:
                    self._x += 0.1
                if self._y > 2.5:
                    self._y -= 0.1
                elif self._y < 2.5:
                    self._y += 0.1
            elif self._state == State.LEFT2:
                if self._x == 2.3 and self._y == 0.1:
                    self._state = State.FORWARD1
                    continue
                if self._x >  2.3:
                    self._x -= 0.1
                elif self._x < 2.3:
                    self._x += 0.1
                if self._y > 0.1:
                    self._y -= 0.1
                elif self._y < 0.1:
                    self._y += 0.1