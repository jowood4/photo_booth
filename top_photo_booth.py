#! /usr/bin/python

import Image, ImageDraw, ImageTk
import Tkinter, subprocess, time
import picture_taker, led_controller, EL_controller

class top_photo_booth:
    def __init__(self):
        self.root = Tkinter.Tk()
        self.width = 800
        self.height = 600
        self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, 0,0))
        self.root.overrideredirect(1)  #take off title bar
        #path = "/home/pi/photo_booth/test_photos/"
        path = "/media/Photo_Booth/Photo_Booth/"

        self.page_timeout = 30000
        self.finish_timeout = 15000
        self.countdown_time = 0.7
        self.total_pic_number = 0
        self.filename = "total_pic"
        self.filelist = list()
        self.filelist.append("")
        self.filelist.append("")
        self.filelist.append("")

        self.pic_taker = picture_taker.picture_taker(path)
        self.stamp = Image.open('/home/pi/photo_booth/quarter_pic.png')
        
        self.frame = {}
        self.frame['start_screen'] = Tkinter.Frame(self.root,cursor="none")
        self.frame['instructions'] = Tkinter.Frame(self.root,cursor="none")
        self.frame['preview'] = Tkinter.Frame(self.root,cursor="none")
        self.frame['count3'] = Tkinter.Frame(self.root,cursor="none")
        self.frame['count2'] = Tkinter.Frame(self.root,cursor="none")
        self.frame['count1'] = Tkinter.Frame(self.root,cursor="none")
        self.frame['cheese'] = Tkinter.Frame(self.root,cursor="none")
        self.frame['got_it'] = Tkinter.Frame(self.root,cursor="none")
        self.frame['look'] = Tkinter.Frame(self.root,cursor="none")
        self.frame['finish'] = Tkinter.Frame(self.root,cursor="none")
        self.command = {}
        self.command['start_screen'] = self.show_instructions
        self.command['instructions'] = self.show_preview
        self.command['preview'] = self.show_3
##        self.command['count3'] = self.show_2
##        self.command['count2'] = self.show_1
##        self.command['count1'] = self.show_got_it
##        self.command['got_it'] = self.show_look
        self.command['look'] = self.show_finish
        self.backgnd_pic = {}
        self.backgnd_pic['start_screen'] = "/home/pi/photo_booth/start_screen.png"
        self.backgnd_pic['instructions'] = "/home/pi/photo_booth/instructions.png"
        self.backgnd_pic['preview'] = "/home/pi/photo_booth/preview.png"
        self.backgnd_pic['count3'] = "/home/pi/photo_booth/count3.png"
        self.backgnd_pic['count2'] = "/home/pi/photo_booth/count2.png"
        self.backgnd_pic['count1'] = "/home/pi/photo_booth/count1.png"
        self.backgnd_pic['cheese'] = "/home/pi/photo_booth/cheese.png"
        self.backgnd_pic['got_it'] = "/home/pi/photo_booth/got_it.png"
        self.backgnd_pic['look'] = "/home/pi/photo_booth/look.png"
        self.backgnd_pic['finish'] = "/home/pi/photo_booth/finish.png"
        self.button = {}
        self.panel = {}
        self.tk_backgnd_pic = {}
        
        self.configure_button('start_screen')
        self.configure_button('instructions')
        self.configure_preview()
        self.configure_panel('count3')
        self.configure_panel('count2')
        self.configure_panel('count1')
        self.configure_panel('cheese')
        self.configure_panel('got_it')
        self.configure_look_frame()
        self.configure_panel('finish')

        self.led_controller = led_controller.led_controller()
        self.EL_controller = EL_controller.EL_controller()
        self.EL_controller.all_on()

        self.show_start_screen()
        
    def configure_button(self, screen):
        self.frame[screen].place(width = self.width, height = self.height, relx = 0, rely = 0)
        self.button[screen] = Tkinter.Button(self.frame[screen], command = self.command[screen], cursor="none")
        picture = Image.open(self.backgnd_pic[screen])
        self.tk_backgnd_pic[screen] = ImageTk.PhotoImage(picture)
        self.button[screen].configure(image = self.tk_backgnd_pic[screen])
        self.button[screen].place(width = self.width, height = self.height, relx = 0, rely = 0)
        
    def configure_panel(self, screen):
        self.frame[screen].place(width = self.width, height = self.height, relx = 0, rely = 0)
        self.panel[screen] = Tkinter.Label(self.frame[screen])
        picture = Image.open(self.backgnd_pic[screen])
        self.tk_backgnd_pic[screen] = ImageTk.PhotoImage(picture)
        self.panel[screen].configure(image = self.tk_backgnd_pic[screen])
        self.panel[screen].place(width = self.width, height = self.height, relx = 0, rely = 0)

    def configure_preview(self):
        self.configure_panel('preview')

        self.preview_pic_button = Tkinter.Button(self.frame['preview'],cursor="none")
        self.preview_pic_button.config(command = self.quit_photo_booth)
        self.preview_pic_button.place(width = 420, height = 280, relx = 0.44, rely = 0.04)
        
        self.snap_pic_button = Tkinter.Button(self.frame['preview'])
        self.snap_pic_button.config(command = self.show_3)
        self.snap_pic_button.config(cursor="none",text="Take a picture", font=("Century Schoolbook L",20))
        self.snap_pic_button.place(width = 250, height = 150, relx = 0.55, rely = 0.6)

    def quit_photo_booth(self):
        self.root.after_cancel(self.id)
        self.root.after_cancel(self.id1)

        self.led_controller.all_off()
        self.EL_controller.all_off()
        
        self.root.destroy()

    def configure_look_frame(self):
        self.configure_panel('look')
        
        self.look_pic_button = list()
        self.look_pic_panel = list()

        func = [self.redo1,self.redo2,self.redo3]

        for i in range(0,3):
            self.look_pic_button.append(Tkinter.Button(self.frame['look'],cursor="none"))
            self.look_pic_button[i].config(command = func[i])

        self.print_button = Tkinter.Button(self.frame['look'])
        self.print_button.config(command = self.command['look'])
        self.print_button.config(cursor="none",text="Print", font=("Century Schoolbook L",20))
        self.print_button.place(width = 250, height = 100, relx = 0.06, rely = 0.82)

    def show_start_screen(self):
        self.pic_count = 0
        self.current_pic = 0
        self.retake = 0
        self.led_controller.random(25)
        self.frame['start_screen'].lift()

    def show_instructions(self):
        self.frame['instructions'].lift()
        self.root.update()
        self.led_controller.random(5)
        self.id1 = self.root.after(self.page_timeout, self.show_start_screen)

    def show_preview(self):
        self.root.after_cancel(self.id1)
        self.frame['preview'].lift()
        self.root.update()
        #self.led_controller.random()
        self.preview_loop()
        self.id1 = self.root.after(self.page_timeout, self.stop_preview_loop)
        self.enter3 = 1

    def preview_loop(self):
        self.pic_taker.preview_pic(self.preview_pic_button)
        self.root.update_idletasks()
        self.id = self.root.after(5, self.preview_loop)

    def stop_preview_loop(self):
        self.root.after_cancel(self.id)
        self.show_start_screen()

    def show_3(self):
        if(self.enter3 == 1):
            self.root.after_cancel(self.id)

        self.root.after_cancel(self.id1)

        self.frame['count3'].lift()
        self.root.update()
        self.led_controller.chase_red()
        time.sleep(self.countdown_time)
        self.show_2()

    def show_2(self):
        self.frame['count2'].lift()
        self.root.update()

        self.led_controller.chase_green()
        if(self.retake == 0):
            if(self.pic_count == 0):
                time.sleep(self.countdown_time)
            elif(self.pic_count == 1):
                self.image = list()
                self.image.append(Image.open(self.filelist[0]))
                self.image[0].thumbnail((400,300), Image.ANTIALIAS)
                self.tk_pic = list()
                self.tk_pic.append(ImageTk.PhotoImage(self.image[0]))
                self.look_pic_button[0].configure(image = self.tk_pic[0])
            elif(self.pic_count == 2):
                self.image.append(Image.open(self.filelist[1]))
                self.image[1].thumbnail((400,300), Image.ANTIALIAS)
                self.tk_pic.append(ImageTk.PhotoImage(self.image[1]))
                self.look_pic_button[1].configure(image = self.tk_pic[1])
        else:
            time.sleep(self.countdown_time)
            
        self.show_1()

    def show_1(self):
        self.frame['count1'].lift()
        self.root.update()
        self.led_controller.chase_white()
        time.sleep(self.countdown_time)
        self.show_cheese()

    def show_cheese(self):
        self.frame['cheese'].lift()
        self.root.update()
        #if(self.retake == 0):
            #self.filelist.append(self.pic_taker.take_picture())
        #else:
        self.filelist[self.current_pic] = self.pic_taker.take_picture()
        self.show_got_it()

    def show_got_it(self):
        self.frame['got_it'].lift()
        self.root.update()

        time.sleep(self.countdown_time)
        
        if(self.pic_count < 2):
            self.current_pic = self.current_pic + 1
            self.pic_count = self.pic_count + 1
            self.enter3 = 2
            self.show_3()
        else:
            self.show_look()

    def show_look(self):
        self.frame['look'].lift()
        self.root.update()
        loc_x = [0, 0.5, 0.5]
        loc_y = [0, 0, 0.5]

        if(self.retake == 0):
            self.image.append(Image.open(self.filelist[2]))
            self.image[2].thumbnail((400,300), Image.ANTIALIAS)
            self.tk_pic.append(ImageTk.PhotoImage(self.image[2]))
            self.look_pic_button[2].configure(image = self.tk_pic[2])
        elif(self.retake == 1):
            self.image[self.current_pic] = Image.open(self.filelist[self.current_pic])
            self.image[self.current_pic].thumbnail((400,300), Image.ANTIALIAS)
            self.tk_pic[self.current_pic] = ImageTk.PhotoImage(self.image[self.current_pic])
            self.look_pic_button[self.current_pic].configure(image = self.tk_pic[self.current_pic])
        for i in range(0,3):
            self.look_pic_button[i].place(width = 400, height = 300, relx = loc_x[i], rely = loc_y[i])

        self.root.update()
        self.led_controller.random(25)

        self.id1 = self.root.after(self.page_timeout, self.show_start_screen)
 
    def redo1(self):
        self.current_pic = 0;
        self.retake = 1
        self.show_3()
    
    def redo2(self):
        self.current_pic = 1;
        self.retake = 1
        self.show_3()
        
    def redo3(self):
        self.current_pic = 2;
        self.retake = 1
        self.show_3()

    def show_finish(self):
        self.frame['finish'].lift()
        self.root.update()

        new_pic = Image.new('RGB', (792, 528))
        new_pic.paste(self.image[0].resize((396,264), Image.ANTIALIAS), (0,0))
        new_pic.paste(self.image[1].resize((396,264), Image.ANTIALIAS), (396,0))
        new_pic.paste(self.image[2].resize((396,264), Image.ANTIALIAS), (0,264))
        new_pic.paste(self.stamp.resize((396,264), Image.ANTIALIAS), (396,264))

        self.pic_taker.print_pic(new_pic)

        self.id1 = self.root.after(self.finish_timeout, self.show_start_screen)
        
        
top = top_photo_booth()
top.root.mainloop()


