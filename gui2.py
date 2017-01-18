
from Tkinter import *
import tkSimpleDialog
import tkMessageBox
import time
from PIL import ImageTk, Image
from neopixel import *


LARGE_FONT= ("Verdana", 12)

root = Tk()
root.wm_geometry("800x400")
root.columnconfigure(0, weight = 1)
root.rowconfigure(0,weight = 1)

LED_COUNT      = 10      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 200     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()

class Clothes:

    def __init__(self):
        self.type = ["none","none","none","none","none","none","none","none","none","none"]
        self.worn_time = [0,0,0,0,0,0,0,0,0,0]
        self.date_created = ["0","0","0","0","0","0","0","0","0","0"]
        self.image_name = ["0.jpg", "1.jpg","2.jpg","3.jpg", "4.jpg", "5.jpg", "6.jpg","7.jpg","8.jpg","9.jpg"]
        self.status = [0,0,0,0,0,0,0,0,0,0]
        self.permanent = [0,0,0,0,0,0,0,0,0,0]

    def get_current_number(self):
        num = 0
        for i in self.status:
            if(i == 1):
                num = num +1
        return num

    def get_permanent_number(self):
        num = 0
        for i in self.permanent:
            if(i == 1):
                num = num +1
        return num
                
    def get_return_number(self):
        num = 0
        for idx,val in enumerate(self.permanent):
            if(val == 1 and self.status[idx] == 0):
                num = num +1
        return num

    def get_return_list(self):
        list = []
        for idx,val in enumerate(self.permanent):
            if(val == 1 and self.status[idx] == 0):
                list.append(idx)
        return list

    def add_clothes(self, index, type, date):
        if(index>=0 and index<=9):
            self.type[index] = type
            self.date_created[index] = date
            self.status[index] = 1
            self.permanent[index] = 1

    def pick_clothes(self, index):
        if(index>=0 and index<=9):
            self.status[index] = 0
            self.worn_time[index] = self.worn_time[index]+1
            
    def return_clothes(self,index):
        if(index>=0 and index<=9):
            self.status[index] = 1

    def delete_clothes(self,index):
        if(index>=0 and index<=9):
            self.status[index] = 0
            self.permanent[index] = 0


    def assign_index(self,type):
        emptyslots = [i for i, e in enumerate(self.permanent) if e == 0]
        index = emptyslots[0]
        
        if(type == "Long-sleeve shirt"):
            for i in emptyslots:
                if(i >= 2):
                    index = i
                    break
        if(type == "Short-sleeve shirt"):
            for i in emptyslots:
                if(i >= 4):
                    index = i
                    break
        if(type == "Jacket"):
            for i in emptyslots:
                if(i >= 6):
                    index = i
                    break
        print "index is %i" % index
        return index

class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
        * Use the 'interior' attribute to place widgets inside the scrollable frame
        * Construct and pack/place/grid normally
        * This frame only allows vertical scrolling
        
        """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)
        
        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL, width = 50)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=TRUE)
        canvas = Canvas(self, bd=0, highlightthickness=0,yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)
        
        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)
        
        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,anchor=NW)
        
        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (800, 2000)
            canvas.config(scrollregion="0 0 %s %s" % size)
            if 800 != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=800)
            if 400 != canvas.winfo_height():
                # update the canvas's height to fit the inner frame
                canvas.config(height=400)

        interior.bind('<Configure>', _configure_interior)
        
        def _configure_canvas(event):
            if 800 != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
            if 400 != canvas.winfo_height():
                # update the inner frame's height to fill the canvas
                canvas.itemconfigure(interior_id, height=canvas.winfo_height())

        canvas.bind('<Configure>', _configure_canvas)

class ConfirmPhoto(tkSimpleDialog.Dialog):
    
    def body(self, master):
        self.index = self.input-1
        imgin = Image.open(str(self.index)+".jpg")
        imgin = imgin.resize((200,300), Image.ANTIALIAS)
        cimage1 = ImageTk.PhotoImage(imgin)
        label1 = Label(self, image = cimage1)
        label1.photo = cimage1
        label1.pack()
    
    
    
    def apply(self):
        clothes.add_clothes(self.input, self.input2, self.input3)
        strip.setPixelColorRGB((self.input-1), 0,255,255)
	strip.show()
        #yellow led on
        if tkMessageBox.askyesno("Confirmation","Done?"):
            #led off
            strip.setPixelColorRGB((self.input-1), 0,0,0)
	    strip.show()
            print "yellow led off"
        else:
            #wait 1 minute, led off
            time.sleep(60)
            strip.setPixelColorRGB((self.input-1), 0,0,0)
            strip.show()
	    print "wait 1 minute led off"


class TypeChoice(tkSimpleDialog.Dialog):
    
    def body(self, master):
        
        self.var = IntVar()
        b1 = Radiobutton(master, indicatoron = 0, text = "Coat", variable = self.var, value = 1)
        b1.pack(anchor=W)
        b2 = Radiobutton(master, indicatoron = 0, text = "Long-sleeve shirt", variable = self.var, value = 2)
        b2.pack(anchor=W)
        b3 = Radiobutton(master, indicatoron = 0, text = "Short-sleeve shirt", variable = self.var, value = 3)
        b3.pack(anchor=W)
        b4 = Radiobutton(master, indicatoron = 0, text = "Jacket", variable = self.var, value = 4)
        b4.pack(anchor=W)
        if(self.var.get()):
           print self.var.get()
    
    
    def apply(self):
        if(self.var.get()):
            if(self.var.get() == 1):
                type = "Coat"
            if(self.var.get() == 2):
                type = "Long-sleeve shirt"
            if(self.var.get() == 3):
                type = "Short-sleeve shirt"
            if(self.var.get() == 4):
                type = "Jacket"
            if tkMessageBox.askyesno("Confirmation", "The type is %s ?" % type):
                    print type
                    index = clothes.assign_index(type)
                    #take photo
                    #save photo
                    d = ConfirmPhoto(root,title = "Photo Confirmation", input = (index+1), input2 = type, input3 = time.strftime("%Y/%m/%d"))



def StorePressed():
    if (clothes.get_permanent_number() < 10):
        d = TypeChoice(root, title= "Choose Type")
    else:
        tkMessageBox.showerror("Error", "The closet is full.")


def LaundryPressed():
    #light on
    strip.setPixelColorRGB(0,255,255,255)
    strip.show()
    if tkMessageBox.askyesno("Confirmation", "Have picked all of them?"):
        #light off
	strip.setPixelColorRGB(0,0,0,0)
	strip.show()
        print "done"



class main(Frame):
    
    def __init__(self, *args, **kwargs):
        
        Frame.__init__(self, *args, **kwargs)
        container = Frame(self, width = 800, height = 480)
        
        container.pack(side = "top", fill="both", expand = True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        
        for F in (StartPage, PagePick, PageReturn, PageDelete):
            
            frame = F(container, self)
            
            self.frames[F] = frame
            
            frame.grid(row=0, column=0, sticky="nsew")
        
        
        self.show_frame(StartPage)
    
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        label = Label(self, text="Home Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        PickButton = Button(self, text="Pick", command = lambda: controller.show_frame(PagePick), bg = "red")
        PickButton.place(x = 50, y = 40, height = 150, width = 200)
        StoreButton = Button(self, text="Store", command = StorePressed, bg = "yellow")
        StoreButton.place(x = 300, y = 40, height = 150, width = 200)
        ReturnButton = Button(self, text="Return", command = lambda: controller.show_frame(PageReturn), bg = "green")
        ReturnButton.place(x = 550, y = 40, height = 150, width = 200)
        LaundryButton = Button(self, text="Laundry", command = LaundryPressed, bg = "blue")
        LaundryButton.place(x = 50, y = 230, height = 150, width = 200)

        DeleteButton = Button(self, text="Delete", command = lambda: controller.show_frame(PageDelete), bg = "purple")
        DeleteButton.place(x = 300, y = 230, height = 150, width = 200)
        if clothes.get_permanent_number() == 0:
            DeleteButton.config(state = DISABLED)



picked_index = IntVar()
class PagePick(Frame):
    
    def PickSelected(*args):
        num = picked_index.get()
        if tkMessageBox.askyesno("Confirmation", "Are you sure to pick up number %i clothes?" % (num + 1)):
            clothes.pick_clothes(num)
            #light on
            #motor move and return to home position

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.verticalframe = VerticalScrolledFrame(self)
        self.verticalframe.pack()
        labels = []
    
        
        NumOfLabels = 0
        c_num = clothes.get_current_number()
        if c_num == 1 or c_num == 2:
            NumOfLabels = 22
        if c_num == 3 or c_num == 4:
            NumOfLabels = 44
        if c_num == 5 or c_num == 6:
            NumOfLabels = 66
        if c_num == 7 or c_num == 8:
            NumOfLabels = 88
        if c_num == 9 or c_num == 10:
            NumOfLabels = 110

        for i in range(NumOfLabels):
            labels.append(Label(self.verticalframe.interior, text=""))
            labels[i].pack()
        
        occupied_slots = [i for i, e in enumerate(clothes.status) if e != 0]
        positionx = [30,390,30,390,30,390,30,390,30,390]
        positiony = [25,25,425,425,825,825,1225,1225,1625,1625]
        
        for idx,val in enumerate(occupied_slots):
            imgin = Image.open(str(val)+".jpg")
            imgin = imgin.resize((300,400), Image.ANTIALIAS)
            cimage = ImageTk.PhotoImage(imgin)
            b = Radiobutton(self.verticalframe.interior, image = cimage, variable = picked_index, value = val)
            b.image = cimage
            b.place(x = positionx[idx], y = positiony[idx], height = 350, width = 300)

        picked_index.trace("w", self.PickSelected)

        HomeButton = Button(self.verticalframe.interior, text = "Home Page", command=lambda: controller.show_frame(StartPage) )
        HomeButton.pack()




return_index = IntVar()
class PageReturn(Frame):
    
    def ReturnSelected(*args):
        num = return_index.get()
        if tkMessageBox.askyesno("Confirmation", "Are you sure to return number %i clothes?" % (num + 1)):
            clothes.return_clothes(num)
            #light on
            #motor move and return to home position

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.verticalframe = VerticalScrolledFrame(self)
        self.verticalframe.pack()
        labels = []
        
        NumOfLabels = 0
        r_num = clothes.get_return_number()
        print "r_num = %i" % r_num
        if r_num == 1 or r_num == 2:
            NumOfLabels = 22
        if r_num == 3 or r_num == 4:
            NumOfLabels = 44
        if r_num == 5 or r_num == 6:
            NumOfLabels = 66
        if r_num == 7 or r_num == 8:
            NumOfLabels = 88
        if r_num == 9 or r_num == 10:
            NumOfLabels = 110
        print "NumOfLabels = %i" % NumOfLabels
        for i in range(NumOfLabels):
            labels.append(Label(self.verticalframe.interior, text=""))
            labels[i].pack()
        
        
        return_slots = clothes.get_return_list()
        positionx = [30,390,30,390,30,390,30,390,30,390]
        positiony = [25,25,425,425,825,825,1225,1225,1625,1625]
        
        for idx,val in enumerate(return_slots):
            imgin = Image.open(str(val)+".jpg")
            imgin = imgin.resize((300,400), Image.ANTIALIAS)
            cimage = ImageTk.PhotoImage(imgin)
            b = Radiobutton(self.verticalframe.interior, image = cimage, variable = return_index, value = val)
            b.image = cimage
            b.place(x = positionx[idx], y = positiony[idx], height = 350, width = 300)
        
        return_index.trace("w", self.ReturnSelected)
        
        HomeButton = Button(self.verticalframe.interior, text = "Home Page", command=lambda: controller.show_frame(StartPage) )
        HomeButton.pack()



delete_index = IntVar()
class PageDelete(Frame):
    
    def DeleteSelected(*args):
        num = delete_index.get()
        if tkMessageBox.askyesno("Confirmation", "Are you sure to delete number %i clothes?" % (num + 1)):
            clothes.delete_clothes(num)
            #light on
            #motor move and return to home position

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.verticalframe = VerticalScrolledFrame(self)
        self.verticalframe.pack()
        labels = []
        NumOfLabels = 0
        p_num = clothes.get_permanent_number()
        if p_num == 1 or p_num == 2:
            NumOfLabels = 22
        if p_num == 3 or p_num == 4:
            NumOfLabels = 44
        if p_num == 5 or p_num == 6:
            NumOfLabels = 66
        if p_num == 7 or p_num == 8:
            NumOfLabels = 88
        if p_num == 9 or p_num == 10:
            NumOfLabels = 110
        
        for i in range(NumOfLabels):
            labels.append(Label(self.verticalframe.interior, text=""))
            labels[i].pack()
        
        occupied_slots = [i for i, e in enumerate(clothes.permanent) if e != 0]
        positionx = [30,390,30,390,30,390,30,390,30,390]
        positiony = [25,25,425,425,825,825,1225,1225,1625,1625]
        
        for idx,val in enumerate(occupied_slots):
            imgin = Image.open(str(val)+".jpg")
            imgin = imgin.resize((300,400), Image.ANTIALIAS)
            cimage = ImageTk.PhotoImage(imgin)
            b = Radiobutton(self.verticalframe.interior, image = cimage, variable = delete_index, value = val)
            b.image = cimage
            b.place(x = positionx[idx], y = positiony[idx], height = 350, width = 300)
        

        delete_index.trace("w", self.DeleteSelected)
        
        HomeButton = Button(self.verticalframe.interior, text = "Home Page", command=lambda: controller.show_frame(StartPage) )
        HomeButton.pack()


clothes = Clothes()
num = clothes.get_permanent_number()
print "Now there are %i clothes in the closet" % num


app = main(root)
app.pack(side="top",fill="both",expand=True)






root.mainloop()







