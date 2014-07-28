#!/usr/bin/python

import wiringpi2

class EL_controller:
        def __init__(self):
                self.amyPin = 4  
                self.benPin = 5
                
                wiringpi2.wiringPiSetup()
                
                wiringpi2.pinMode(self.amyPin,1)
                wiringpi2.pinMode(self.benPin,1)

        def amy_on(self):
                wiringpi2.digitalWrite(self.amyPin,0)

        def amy_off(self):
                wiringpi2.digitalWrite(self.amyPin,1)

        def ben_on(self):
                wiringpi2.digitalWrite(self.benPin,0)

        def ben_off(self):
                wiringpi2.digitalWrite(self.benPin,1)

        def all_on(self):
                self.amy_on()
                self.ben_on()

        def all_off(self):
                self.amy_off()
                self.ben_off()

        
