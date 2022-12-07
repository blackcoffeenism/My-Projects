from tkinter import *
from tkinter.messagebox import *
from PIL import ImageTk, Image
root = Tk()
class MPG:
    def __init__(self,master):
        self.master = master
        #designs and orientations
        w = 700
        h = 500
        self.canvas = Canvas(self.master,width = w, height = h)
        self.canvas.pack()
        self.master.resizable(width = False, height = False)
        
        self.master.title("MPG Calculator")
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        x_coordinate = (screen_width/2) - (w/2)
        y_coordinate = (screen_height/2) - (h/2)
        #To put window at the center of the screen
        self.master.geometry("%dx%d+%d+%d" % (w,h,x_coordinate,y_coordinate))
        #frames
        self.frame1 = Frame(bg = 'deep sky blue', relief = 'raised', bd = 10)
        self.frame1.pack()
        self.frame2 = Frame(bg = 'deep sky blue', relief = 'raised', bd = 10)
        self.frame2.pack()
        MPG.display(self)
    def display(self):
        #background
        self.bg = Image.open('data\\gasoline.jpg')
        self.bg = self.bg.resize((700,500), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(self.bg)
        self.canvas.create_image(0,0, anchor = NW , image = self.bg)
        self.canvas.image = self.bg

        self.canvas.create_text(350,50, text = "MPG CALCULATOR", font=("castellar",50),fill = "red") 

        self.canvas.create_text(585,265, text = "Car Details", font = ("times new roman", 25), fill = "black")

        self.canvas.create_window(25,75, anchor = NW , window = self.frame1, width = 200, height = 350)
        self.canvas.create_window(500,250, anchor = NW , window = self.frame2, width = 175, height = 225)
        MPG.entry_frame(self)
        MPG.detail_frame(self)
        
    def entry_frame(self):
        #title in calculator and labels
        title = Label(self.frame1, text = "MPG Calculator", bg = "sky blue", font = ("times new roman", 18),fg = "black", relief = 'raised',bd = 5)
        title.place(relx = 0.5, rely = 0.1, anchor = CENTER)
        
        number = Label(self.frame1, text = "Number of gallons", bg = "deep sky blue", font = ("times new roman", 14),fg = "black")
        number.place(relx = 0.5, rely = 0.3, anchor = CENTER)

        self.number_entry = Entry(self.frame1, bg = 'gray89', font = ("times new roman", 12))
        self.number_entry.place(relx = 0.5, rely = 0.4, anchor = CENTER)

        mile = Label(self.frame1, text = "Miles driven", bg = "deep sky blue", font = ("times new roman", 14),fg = "black")
        mile.place(relx = 0.5, rely = 0.5, anchor = CENTER)

        self.mile_entry = Entry(self.frame1, bg = 'gray89', font = ("times new roman", 12))
        self.mile_entry.place(relx = 0.5, rely = 0.6, anchor = CENTER)

        calculate = Button(self.frame1, bg = "sky blue", text = "Calculate",font = ("times new roman", 14),activebackground = "deep sky blue", command =lambda:MPG.calculate(self))
        calculate.place(relx = 0.5, rely = 0.8, anchor = CENTER)

        self.result = Label(self.frame1, bg = "deep sky blue", font = ("times new roman", 16),fg = "black")
        self.result.place(relx = 0.5, rely = 0.9, anchor = CENTER)
    def calculate(self):
        #if no entry
        if (self.number_entry.get()== '') or (self.mile_entry.get()==''):
            showinfo(title='Oopps!', message="No entered value!")
            self.number_entry.delete(0,END)
            self.mile_entry.delete(0,END)
        #if number of gallon greater than the full tank
        
        elif eval(self.number_entry.get())> 23.78:
            showinfo(title='Oopps', message='Your car cannot hold that much gallon of petrol.\n Check the details of your car!')
            self.number_entry.delete(0,END)
            self.mile_entry.delete(0,END)

        else:
            res = round(float(self.mile_entry.get())/float(self.number_entry.get()),2)
            res = str(res)

            self.result.configure(text = res+'MPG')
            
            self.number_entry.delete(0,END)
            self.mile_entry.delete(0,END)
    def detail_frame(self):
        #car information
        title = Label(self.frame2, text = "Car Details", bg = "sky blue", font = ("times new roman", 18),fg = "black", relief = 'raised',bd = 5)
        title.place(relx = 0.5, rely = 0.1, anchor = CENTER)
        
        line = Label(self.frame2, text = "--------------------", bg = "deep sky blue", font = ("times new roman", 12))
        line.place(relx = 0.5, rely = 0.43, anchor = CENTER)

        car_model = Label(self.frame2, text = "Car model:\nLamborghini Aventador", bg = "deep sky blue", font = ("times new roman", 12))
        car_model.place(relx = 0.5, rely = 0.3, anchor = CENTER)
        
        fuel = Label(self.frame2, text = "Fuel Type:\nPetrol", bg = "deep sky blue", font = ("times new roman", 12))
        fuel.place(relx = 0.5, rely = 0.55, anchor = CENTER)

        full = Label(self.frame2, text = "Full Tank:\n23.78 Gallons", bg = "deep sky blue", font = ("times new roman", 12))
        full.place(relx = 0.5, rely = 0.85, anchor = CENTER)

        line2 = Label(self.frame2, text = "--------------------", bg = "deep sky blue", font = ("times new roman", 12))
        line2.place(relx = 0.5, rely = 0.70, anchor = CENTER)


class quit:
    def quitter():
        answer = askquestion(title = "Quit?", message = "Do you really want to quit\n MPG calculator?")
        if answer == "yes":
            root.destroy()
#if the user want to quit
root.protocol("WM_DELETE_WINDOW",quit.quitter)

MPG(root)
