#!/usr/bin/python

import Image, ImageDraw, ImageTk, StringIO, sys
import time, Tkinter, cups
import subprocess, shlex

class picture_taker:
    def __init__(self, path): #root, width, height, path):
        self.filename = "image"#"/dev/shm/image.jpg"
        self.pic_path = path  #"/home/pi/photo_booth/test_photos/"
        self.pic_number = 0
        self.total_pic_number = 0

        self.conn = cups.Connection()
        printers = self.conn.getPrinters()
        self.printer_name = printers.keys()[0]

    def take_picture(self):

        self.pic_number = self.pic_number + 1
        filename = (self.pic_path + "singles/" + self.filename + str(self.pic_number) + ".png")

        command = "raspistill -n -t 500 -q 100 -e png -vf -hf\
                    -br 50 -co 0 -sa 0 -sh 0 -ex auto\
                    -awb auto -ev 5 -mm average -o %s -e jpg &" \
                    % filename
                    
        subprocess.check_output(command, shell=True)
        return filename
        

    def preview_pic(self, panel):

        self.imageData = StringIO.StringIO()
        command = "raspistill -n -w %s -h %s -t 500 -vf -hf\
                    -br 50 -co 0 -sa 0 -sh 0 -q 100  -ex auto\
                    -awb auto -ev 5 -mm average -e jpg -o - &" % (420, 280)
        self.imageData.write(subprocess.check_output(command, shell=True))
        self.imageData.seek(0)
        self.image1 = Image.open(self.imageData)
        self.tk_pic = ImageTk.PhotoImage(self.image1)
        panel.configure(image = self.tk_pic)
        panel.place()
        self.imageData.close()

    def print_pic(self, pic):
        filename = self.pic_path + "fours/" + "total_pic" + str(self.total_pic_number) + ".png"
        pic.save(filename)

        options = {'orientation-requested':'4','media':'4x6'}
        self.conn.printFile(self.printer_name, filename, filename, options)
        
        self.total_pic_number = self.total_pic_number + 1
