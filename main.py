import os, sys, time
from state import Light
from trafic_light import TraficLight
import revpimodio2

class MyTraficLightApp():

    def __init__(self):
        self.revPi = revpimodio2.RevPiModIO(autorefresh=True)
        self.revPi.handlesignalend(self.cleanup_revpi)

        self.tl1 = TraficLight(revPi=self.revPi, ioGreen='O_3', ioOrange='O_2', ioRed='O_1')
        

    def cleanup_revpi(self):
        self.tl1.cleanUp()

    def start(self):
        self.revPi.mainloop(blocking=False)
        print("Trafic light example is starting")
        while True:
            self.tl1.changeState(Light.red)
            time.sleep(1)
if __name__ == "__main__":
    root = MyTraficLightApp()
    root.start()
