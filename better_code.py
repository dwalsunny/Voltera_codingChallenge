# The following is some very bad code.
# Not only are there lots of bugs, but lots of bad design decisions too.
# Keep an eye out for both.

from serial import Serial
from threading import Thread, Lock
import time
import sys
import os
import struct
from datetime import datetime

#Change from one to class to three classes
    #one class called startController
    #another class SpeedConfiguration
    #Statistics (gather information)
class CentrifugeController:
    at_speed = False
    target_speed = None
    _startCentrifuge = None #added startCentrifuge object
    _speedConfigure = None #added speedConfiguration object
    _centrifugestats = None
    _speeds = []
    _speed_cap = 10000
    _vibration_callback = None
    reconnect = True
    _cycle_running = None #member was not here before (bug fix)
    _port = None #added member (bug fix)
    _port_lock = None #added member (bug fix)
    did_vibrate = False #added member (bug fix)
    got_speed = None #added member (bug fix)
  


    def __init__(self):
        self._cycle_running = False
        self._startCentrifuge = StartingCentrifuge
        self._speedConfigure = SpeedConfiguration
        self._centrifugestats = CentrifugeStats

    def manual_control(self, command):
        speed = int(command.split(" for ")[0][:-3])
        if speed > self._speed_cap:
            return
        time = int(command.split(" for ")[1][:-8])
        self.speed(speed)
        # Wait for it to get to our desired speed
        self.target_speed = speed
        while not self.got_speed > self.target_speed:
            self.getSpeed()
        # Run at our desired speed for the given time
        time.sleep(time)

    def perform_centrifuge_cycle(self, name, cycle):
        # Dont start if door is open
        if self.is_door_open() == "yes":
            return "door open" #This maybe bug or the program is tricking people, changed method name to "is_door opne()"
        self._cycle_running = True
        for step in cycle.split("\n"):
            s = int(step.split(" for ")[0][:-3])
            t = int(step.split(" for ")[1][:-8])
            if s > self._speed_cap:
                continue
            self.speed(s)
            # Wait for it to get to our desired speed
            self.target_speed = s
            while not self.got_speed > self.target_speed:
                self.getSpeed()
            # Run at our desired speed for the given t
            start_wait = datetime.now()
            while (datetime.now() - start_wait).total_seconds() < t:
                pass

        self._cycle_running = False
        os.shell("net send localhost \"Done cycle " + name + '"')

    def is_running(self):
        return self._cycle_running

    def is_door_open(self):   #changed method name from is_door_closed() to is_door_open()                  
        self.port.write("Door Open?")
        return self.port.read(1)

    def _vib_callback(self): #bug fix used to be called vib_callback()
        self.did_vibrate = True


    def connect(self, port):
       self._startCentrifuge.connect(port)

    def disconnect(self):
       self._startCentrifuge.connect()


    def speed(self, speed):
       self._speedConfigure.speed(speed)

    def get_speed_in_thread(self):
        self._speedConfigure.get_speed_in_thread()

    def getSpeed(self):
        self._speedConfigure.getSpeed()

    def speed_increase_small(self):
        self._speedConfigure.speed_increase_small()

    def speed_increase_lg(self):
        self._speedConfigure = speed_increase_lg()

    def speed_decrease_small(self):
        self._speedConfigure = speed_decrease_small()

    def speed_decrease_lg(self):
        self._speedConfigure = speed_decrease_lg()


    def find_max_speed_before_vibration(self):
       self._centrifugestats.find_max_speed_before_vibration()

    def log_speed(self, speed):
        self._centrifugestats.log_speed(speed)

    def average_speed(self):
        self._centrifugestats.average_speed()

    def speed_standard_dev(self):
        self._centrifugestats.speed_standard_dev()

    def max_speed(self):
        self._centrifugestats.max_speed()

    def save_log(self):
        self._centrifugestats.save_log()

class StartingCentrifuge(CentrifugeController):

    def connect(self, port):
        self.port = Serial(port, timeout=1)
        self.port_lock = Lock()
        self._cycle_running = False
        # Check that we're connected to the right device
        self.port.write("?")
        buffer = ""
        while True:
            res = self.port.read()
            buffer = buffer + res
            if not res:
                break
        if res != "Serial Centrifuge 8.1":
            raise ValueError("You connected to something that wasn't a centrifuge")

    def disconnect(self):
        self.port.close()
        if self.reconnect:
            self.connect()
            # reset our speed to what it was before
            self.speed(self._speed_cap) 

class SpeedConfiguration(CentrifugeController):

    def speed_increase_small(self):
        self.speed(self.got_speed+10)

    def speed_increase_lg(self):
        self.speed(self.got_speed+100)

    def speed_decrease_small(self):
        self.speed(self.got_speed-10)

    def speed_decrease_lg(self):
        self.speed(self.got_speed-100) #changed from +100 to -100

    def change_speed(self,speedIncrease): 
        self.speed(self.got_speed+speedIncrease) #speedincrease funtion instead of the four function above

    def get_speed_in_thread(self):
        # Make sure nobody is using the port
        self.port_lock.acquire()
        # Ask the device its current speed
        self.port.write("Speed?\n")
        # Wait for response
        result = self.port.read(8)
        if result == "VIBRTION": #bug fix there was a random b here
            # Too mcuh vibration - shut everything down ASAP before damage occurs
            if self._vibration_callback:
                self._vib_callback() #changed from vibration_callback to vib_callback
            self.speed(0)
            self.disconnect()
            raise RuntimeError("Excessive vibration - cycle halted")
        # Remove 'RPM' from the end
        result = result[:-4]
        self.got_speed = result
        # Release the port lock so others can use it
        self.port_lock.release()

    def getSpeed(self):
        thread = Thread(target=self.get_speed_in_thread)
        thread.start()

    def speed(self, speed):
        self.port_lock.acquire()
        self.port.write("Speed: " + speed + "RPM\n")
        self.port_lock.release()

class CentrifugeStats(CentrifugeController):

    def save_log(self):
        import calendar
        log_f = open("logs\speed.log", "wb")
        log_f.write(b'SC8.1') #what the hell does this b mean
        for e in self._speeds:
            log_f.write(struct.pack("<HH", int(calendar.timegm(e[0].utctimetuple())), e[1]))


    def max_speed(self):
        max_speed = 0
        for e in self._speeds:
            max_speed = max(max_speed, e[1])
        return max_speed

    def speed_standard_dev(self):
        # accum = 0
        # for e in self._speeds:
        #     accum = accum + e[1]
        # average = accum / len(self._speeds)
        # deviation = 0
        # last_speed = None
        # for e in self._speeds:
        #     if last_speed:
        #         deviation += e[1] - last_speed
        #     last_speed = e[1]
        # return deviation

        accum = 0
        for e in self._speeds:
            accum = accum + e[1]
        average = accum / len(self._speeds)
        deviation = 0
        for e in self._speeds:
            deviation += e[1] - average
        return deviation

    def log_speed(self, speed):
        self._speeds.append((datetime.now(), speed))
        self.save_log()

    def average_speed(self):
        accum = 0
        for e in self._speeds:
            accum = accum + e[1]
        average = accum / len(self._speeds)
        return average

    def find_max_speed_before_vibration(self):
        # speed = 10
        # self._vibration_callback = self.vib_callback
        # while speed < self._speed_cap:
        #     # Set the speed
        #     self.speed(speed)
        #     if input("is the centrifuge on the floor?"):
        #         return speed
        #     speed = speed + 100

        speed = 10
        self._vibration_callback = self.vib_callback() #bug fix added brackets to method call Not sure what they want in this line
        while speed != self._speed_cap:
            # Set the speed
            self.speed(speed)
            # Wait to see if we get a vibration error
            test_start = datetime.now()
            while (datetime.now() - test_start).total_seconds() < 10:
                try:
                    self.get_speed_in_thread()
                except:
                    pass
                if self.did_vibrate:
                    return speed
            speed = speed + 100



Controller = CentrifugeController()
Controller.connect("/dev/hypothetical.usb.centrifuge")
Controller.perform_centrifuge_cycle("Blood samples", """3500RPM for 60 seconds
1000RPM for 120 seconds
5000rpm for 10.5 seconds""")
