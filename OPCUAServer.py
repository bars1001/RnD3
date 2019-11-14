import sys, os, time
sys.path.insert(0, "..")
from opcua import ua, Server
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

    def start(self, color):
        if color == 1:
           self.tl1.changeState(Light.red)
        if color == 2:
           self.tl1.changeState(Light.green)
        if color == 3:
           self.tl1.changeState(Light.orange)

if __name__ == "__main__":
    # setup our server
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    # setup our own namespace, not really necessary but should as spec
    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    # get Objects node, this is where we should put our nodes
    objects = server.get_objects_node()

    # populating our address space
    myobj = objects.add_object(idx, "MyObject")
    myvar = myobj.add_variable(idx, "Light", 0)
    myvar.set_writable()    # Set MyVariable to be writable by clients
    # starting!
    server.start()
    try:
        count = 0
        root = MyTraficLightApp()
        while True:
            if myvar.get_value() == 1:
                root.start(1)
            elif myvar.get_value() == 2:
                root.start(2)
            elif myvar.get_value() == 3:
                root.start(3)
            else:
                root.cleanup_revpi()
                time.sleep(1)
                count += 0.1
            print(myvar.get_value())
    finally:
        #close connection, remove subcsriptions, etc
        server.stop()
