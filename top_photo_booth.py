#!/usr/bin/python

import Image, ImageDraw, ImageTk
import picam, Tkinter
import subprocess
import picture_taker, picture_looker
import led_controller, EL_controller, time

class top_photo_booth:
    def __init__(self):
        self.root = Tkinter.Tk()
        self.width = 800
        self.height = 600
        self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, 0,0))
        #self.root.overrideredirect(1)  #take off title bar
        path = "/home/pi/photo_booth/test_photos/"

        self.page_timeout = 20000
        self.countdown_time = 1.5
        self.total_pic_number = 0
        self.filename = "total_pic"
        self.filelist = list()

        self.pic_taker = picture_taker.picture_taker(path)

        self.start_screen_frame = Tkinter.Frame(self.root,cursor="none")
        self.configure_start_screen()

        self.instructions_frame = Tkinter.Frame(self.root,cursor="none")
        self.configure_instructions()

        self.preview_frame = Tkinter.Frame(self.root,cursor="none")
        self.configure_preview()

        self.count3_frame = Tkinter.Frame(self.root,cursor="none")
        self.configure_3()

        self.count2_frame = Tkinter.Frame(self.root,cursor="none")
        self.configure_2()

        self.count1_frame = Tkinter.Frame(self.root,cursor="none")
        self.configure_1()

        self.got_it_frame = Tkinter.Frame(self.root,cursor="none")
        self.configure_got_it()

        self.look_frame = Tkinter.Frame(self.root,cursor="none")
        self.configure_look_frame() 

        self.show_start_screen()

        self.led_controller = led_controller.led_controller()
        #self.led_controller.all_white()
        self.led_controller.all_off()
        self.EL_controller = EL_controller.EL_controller()
        #self.EL_controller.all_on()
        self.EL_controller.all_off()
        

    def configure_start_screen(self):
        #self.configure("start_screen_frame")
        self.start_screen_frame.place(width = self.width, height = self.height, relx = 0, rely = 0)
        self.start_screen_button = Tkinter.Button(self.start_screen_frame, command = self.show_instructions, cursor="none")
        picture = Image.open("start_screen.png")
        self.tk_start_pic = ImageTk.PhotoImage(picture)
        self.start_screen_button.configure(image = self.tk_start_pic)
        self.start_screen_button.place(width = self.width, height = self.height, relx = 0, rely = 0)

    #def configure(self, screen):
        #self.[screen].place(width = self.width, height = self.height, relx = 0, rely = 0)
        
    def configure_instructions(self):
        self.instructions_frame.place(width = self.width, height = self.height, relx = 0, rely = 0)
        self.instructions_button = Tkinter.Button(self.instructions_frame, command = self.show_preview, cursor="none")
        picture = Image.open("instructions.png")
        self.tk_instructions_pic = ImageTk.PhotoImage(picture)
        self.instructions_button.configure(image = self.tk_instructions_pic)
        self.instructions_button.place(width = self.width, height = self.height, relx = 0, rely = 0)

    def configure_preview(self):
        self.preview_frame.place(width = self.width, height = self.height, relx = 0, rely = 0)
        self.preview_panel = Tkinter.Label(self.preview_frame)
        picture = Image.open("preview.png")
        self.tk_preview_pic = ImageTk.PhotoImage(picture)
        self.preview_panel.configure(image = self.tk_preview_pic)
        self.preview_panel.place(width = self.width, height = self.height, relx = 0, rely = 0)

        self.preview_pic_frame = Tkinter.Frame(self.preview_frame,cursor="none")
        self.preview_pic_frame.place(width = 420, height = 280, relx = 0.47, rely = 0.1)
        self.pic_panel = Tkinter.Label(self.preview_pic_frame)
        self.pic_panel.place(width = 420, height = 280, relx = 0, rely = 0)

        self.preview_button_frame = Tkinter.Frame(self.preview_frame,cursor="none")
        self.preview_button_frame.place(width = 250, height = 150, relx = 0.6, rely = 0.65)
        
        self.snap_pic_button = Tkinter.Button(self.preview_button_frame)
        self.snap_pic_button.config(command = self.show_3)
        self.snap_pic_button.config(cursor="none",text="Take a picture", font=("Century Schoolbook L",20))
        self.snap_pic_button.place(width = 250, height = 150, relx = 0, rely = 0)


    def configure_3(self):
        self.count3_frame.place(width = self.width, height = self.height, relx = 0, rely = 0)
        self.count3_panel = Tkinter.Label(self.count3_frame)
        self.pic_show_3 = Image.open("count3.png")
        self.tk_3_pic = ImageTk.PhotoImage(self.pic_show_3)
        self.count3_panel.configure(image = self.tk_3_pic)
        self.count3_panel.place(width = self.width, height = self.height, relx = 0, rely = 0)

    def configure_2(self):
        self.count2_frame.place(width = self.width, height = self.height, relx = 0, rely = 0)
        self.count2_panel = Tkinter.Label(self.count2_frame)
        self.pic_show_2 = Image.open("count2.png")
        self.tk_2_pic = ImageTk.PhotoImage(self.pic_show_2)
        self.count2_panel.configure(image = self.tk_2_pic)
        self.count2_panel.place(width = self.width, height = self.height, relx = 0, rely = 0)

    def configure_1(self):
        self.count1_frame.place(width = self.width, height = self.height, relx = 0, rely = 0)
        self.count1_panel = Tkinter.Label(self.count1_frame)
        self.pic_show_1 = Image.open("count1.png")
        self.tk_1_pic = ImageTk.PhotoImage(self.pic_show_1)
        self.count1_panel.configure(image = self.tk_1_pic)
        self.count1_panel.place(width = self.width, height = self.height, relx = 0, rely = 0)

    def configure_got_it(self):
        self.got_it_frame.place(width = self.width, height = self.height, relx = 0, rely = 0)
        self.got_it_panel = Tkinter.Label(self.got_it_frame)
        picture = Image.open("got_it.png")
        self.tk_got_it_pic = ImageTk.PhotoImage(picture)
        self.got_it_panel.configure(image = self.tk_got_it_pic)
        self.got_it_panel.place(width = self.width, height = self.height, relx = 0, rely = 0)

    def configure_look_frame(self):
        self.look_frame.place(width = self.width, height = self.height, relx = 0, rely = 0)
        self.look_panel = Tkinter.Label(self.look_frame)
        picture = Image.open("look.png")
        self.tk_look_pic = ImageTk.PhotoImage(picture)
        self.look_panel.configure(image = self.tk_look_pic)
        self.look_panel.place(width = self.width, height = self.height, relx = 0, rely = 0)
        
        self.look_pic_button = list()
        self.look_pic_panel = list()

        func = [self.redo1,self.redo2,self.redo3]

        for i in range(0,3):
            self.look_pic_button.append(Tkinter.Button(self.look_frame,cursor="none"))
            self.look_pic_button[i].config(command = func[i])

        self.print_button = Tkinter.Button(self.look_frame)
        self.print_button.config(command = self.print_pic)
        self.print_button.config(cursor="none",text="Print", font=("Century Schoolbook L",20))
        self.print_button.place(width = 250, height = 150, relx = 0, rely = 0.8)

    def show_start_screen(self):
        self.pic_count = 0
        self.current_pic = 0
        self.retake = 0
        self.start_screen_frame.lift()

    def show_instructions(self):
        self.instructions_frame.lift()
        self.root.update_idletasks()
        self.id1 = self.root.after(self.page_timeout, self.show_start_screen)

    def show_preview(self):
        self.root.after_cancel(self.id1)
        self.preview_frame.lift()
        self.root.update()
        self.preview_loop()
        self.id1 = self.root.after(self.page_timeout, self.stop_preview_loop)
        self.enter3 = 1

    def preview_loop(self):
        self.pic_taker.preview_pic(self.pic_panel)
        self.root.update_idletasks()
        self.id = self.root.after(5, self.preview_loop)

    def stop_preview_loop(self):
        self.root.after_cancel(self.id)
        self.show_start_screen()

    def show_3(self):
        if(self.enter3 == 1):
            self.root.after_cancel(self.id)
            self.root.after_cancel(self.id1)

        self.count3_frame.lift()
        self.root.update()
        time.sleep(self.countdown_time)
        self.show_2()

    def show_2(self):
        self.count2_frame.lift()
        self.root.update()

        if(self.retake == 0):
            if(self.pic_count == 0):
                time.sleep(self.countdown_time)
            elif(self.pic_count == 1):
                self.image = list()
                self.image.append(Image.open(self.filelist[0]))
                self.image[0].thumbnail((400,300), Image.ANTIALIAS)
                #image1 = Image.open(self.filelist[0])
                #image1 = image1.resize((400,300), Image.ANTIALIAS)
                #image1.thumbnail((400,300), Image.ANTIALIAS)
                self.tk_pic = list()
                self.tk_pic.append(ImageTk.PhotoImage(self.image[0]))
                self.look_pic_button[0].configure(image = self.tk_pic[0])
            elif(self.pic_count == 2):
                #image1 = Image.open(self.filelist[1])
                #image1 = image1.resize((400,300), Image.ANTIALIAS)
                self.image.append(Image.open(self.filelist[1]))
                self.image[1].thumbnail((400,300), Image.ANTIALIAS)
                self.tk_pic.append(ImageTk.PhotoImage(self.image[1]))
                self.look_pic_button[1].configure(image = self.tk_pic[1])
        else:
            time.sleep(self.countdown_time)
            
        self.show_1()

    def show_1(self):
        self.count1_frame.lift()
        self.root.update()
        time.sleep(self.countdown_time)
        if(self.retake == 0):
            self.filelist.append(self.pic_taker.take_picture())
        else:
            self.filelist[self.current_pic] = self.pic_taker.take_picture()
        self.show_got_it()

    def show_got_it(self):
        self.got_it_frame.lift()
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
        self.look_frame.lift()
        self.root.update()
        loc_x = [0, 0.5, 0.5]
        loc_y = [0, 0, 0.5]

        if(self.retake == 0):
            self.image.append(Image.open(self.filelist[2]))
            #image1 = Image.open(self.filelist[2])
            #image1 = image1.resize((400,300), Image.ANTIALIAS)
            self.image[2].thumbnail((400,300), Image.ANTIALIAS)
            self.tk_pic.append(ImageTk.PhotoImage(self.image[2]))
            self.look_pic_button[2].configure(image = self.tk_pic[2])
        elif(self.retake == 1):
            self.image[self.current_pic] = Image.open(self.filelist[self.current_pic])
            #image1 = image1.resize((400,300), Image.ANTIALIAS)
            self.image[self.current_pic].thumbnail((400,300), Image.ANTIALIAS)
            self.tk_pic[self.current_pic] = ImageTk.PhotoImage(self.image[self.current_pic])
            self.look_pic_button[self.current_pic].configure(image = self.tk_pic[self.current_pic])
        for i in range(0,3):
            self.look_pic_button[i].place(width = 400, height = 300, relx = loc_x[i], rely = loc_y[i])

        self.root.update()
 
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

    def print_pic(self):
        new_pic = Image.new('RGB', (792, 528))
        new_pic.paste(self.image[0].resize((396,264), Image.ANTIALIAS), (0,0))
        new_pic.paste(self.image[1].resize((396,264), Image.ANTIALIAS), (396,0))
        new_pic.paste(self.image[2].resize((396,264), Image.ANTIALIAS), (0,264))

        self.pic_taker.print_pic(new_pic)
        
        
top = top_photo_booth()
top.root.mainloop()


