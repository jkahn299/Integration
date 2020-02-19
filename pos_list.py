from marvelmind import MarvelmindHedge
from time import sleep

hedge = MarvelmindHedge(tty="/dev/ttyACM0", adr=10, debug=False)
hedge.start()
91
while(1):
    pos_list = hedge.position_list()

    print(pos_list[1])
    print(pos_list[2])
    print(pos_list[3])
    sleep(.5)

