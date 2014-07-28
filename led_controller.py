#!/usr/bin/python

import wiringpi2, time
import numpy as np
import random

class led_controller:
        def __init__(self):
                self.dataPin = 1  
                self.clockPin = 3
                self.output_enable = 2
                self.latch = 0
                self.led_matrix = np.zeros((16,3), dtype=np.uint16)
                
                wiringpi2.wiringPiSetup()
                
                wiringpi2.pinMode(self.output_enable,1)
                wiringpi2.pinMode(self.latch,1)
                wiringpi2.pinMode(self.dataPin,1)
                wiringpi2.pinMode(self.clockPin,1)

                wiringpi2.digitalWrite(self.output_enable,0)
                wiringpi2.digitalWrite(self.dataPin,0)
                wiringpi2.digitalWrite(self.clockPin,0)
                wiringpi2.digitalWrite(self.latch,0)

        def update_leds(self):
                wiringpi2.digitalWrite(self.latch,0)
                for i in range(16):
                        for j in range(3):
                                string = np.binary_repr(self.led_matrix[7-i,2-j], width=12)
                                #print string
                                for k in range(12):
                                        wiringpi2.digitalWrite(self.clockPin,0)
                                        #wiringpi2.shiftOut(self.dataPin, self.clockPin, 0, int(self.led_matrix[i,j]))
                                        #print int(self.led_matrix[i,j])
                                        wiringpi2.digitalWrite(self.dataPin,int(string[k]))
                                        wiringpi2.digitalWrite(self.clockPin,1)

                wiringpi2.digitalWrite(self.clockPin,0)
                wiringpi2.digitalWrite(self.latch,1)
                wiringpi2.digitalWrite(self.latch,0)

        def set_led(self, led, red, green, blue):
                self.led_matrix[led,0] = red
                self.led_matrix[led,1] = green
                self.led_matrix[led,2] = blue

        def all_white(self):
                for i in range(16):
                        self.set_led(i,4095,4095,4095)
                        self.update_leds()

        def all_off(self):
                for i in range(16):
                        self.set_led(i,0,0,0)
                        self.update_leds()

        def chaser(self):
                self.chase_red()
                self.chase_green()
                self.chase_blue()

        def chase_red(self):
                for i in range(16):
                        self.set_led(i,4095,0,0)
                        self.update_leds()

        def chase_green(self):
                for i in range(16):
                        self.set_led(i,0,4095,0)
                        self.update_leds()

        def chase_blue(self):
                for i in range(16):
                        self.set_led(i,0,0,4095)
                        self.update_leds()

        def chase_white(self):
                for i in range(16):
                        self.set_led(i,4095,4095,4095)
                        self.update_leds()

        def random(self, num):
                for i in range(num):
                        led = random.randint(0,15)
                        red = random.randint(0,4095)
                        green = random.randint(0,4095)
                        blue = random.randint(0,4095)
                        self.set_led(led,red,green,blue)
                        self.update_leds()
