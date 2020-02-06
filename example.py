import time
import numpy

from marvelmind import MarvelmindHedge
from time import sleep
import sys


global pos
global HEDGE
global Z
Z=True
HEDGE = MarvelmindHedge(tty= "/dev/ttyACM0", adr=10, debug=False)
HEDGE.start()

# Example comment
def position(HEDGE):
	try:
		#print(hedge.position()) #get last position and print
		pos = HEDGE.position()
		print("Addr: " + str(pos[0]))
		print("X: " + str(pos[1]))
		print("Y: " + str(pos[2]))
		print("time: " + str(pos[5]))
		return pos
	except KeyboardInterrupt:
			HEDGE.stop()
			sys.exit()

def main(X, Y, Z):
 #   hedge = MarvelmindHedge(tty = "/dev/ttyACM0", adr=10, debug=False) # create MarvelmindHedge thread
 #   hedge.start() # start thread
    while Z:
	A = HEDGE.position()
	X_diff = X - A[1]
	Y_diff = Y -A[2]
	m = numpy.sqrt((X_diff*X_diff)+(Y_diff*Y_diff))
	Xnew = X_diff/m
	Ynew = Y_diff/m
	if (A[1] - 1 <=  X <= A[1] + 1 and A[2]-1 <= Y <= A[2] + 1):
		print("Arrived")
		Z = False
		break
	print ("X1: " + str(X))
	print("Y1: " + str(Y))
	print("X2: " + str(Xnew))
	print("Y2: " + str(Ynew))
	time.sleep(1)
#	sys.exit()
main(1, -.5, Z)
    #    try:
     #       sleep(1)
      #      # print (hedge.position()) # get last position and print
       #     hedge.print_position()
        #    if (hedge.distancesUpdated):
	#			hedge.print_distances()
       # except KeyboardInterrupt:
        #    hedge.stop()  # stop and close serial port
         #   sys.exit()
#main()
