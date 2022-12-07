from tkinter import * # import tkinter to use
import vaccinationDB
from tkinter import ttk
from tkinter.messagebox import *
vaccinationDB.data()
root = Tk()                                                     
root.title("Vaccination Status")                            #Screen appearance and orientation  
root_width = 1000
root_height = 600

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_coordinate = (screen_width/2) - (root_width/2)
y_coordinate = (screen_height/2) - (root_height/2)
root.geometry("%dx%d+%d+%d" % (root_width,root_height,x_coordinate,y_coordinate))
count = 0
count1 = 0
edit_count = 0

class MainWindow:
    def __init__(self,main):
        self.main = main
        #Create background
        canvas = Canvas(self.main, bg = "cadet blue", width = 1000, height = 600)
        canvas.grid(row = 0, column = 0, rowspan = 5)
        #Create Frame
        self.frame = Frame(self.main, bg = "blue",width = 100, relief = 'raised', bd = 5)
        self.frame.grid(row = 0, column = 0,padx = 160,pady = 20, columnspan = 3)
        #Title
        label = Label(self.frame, text = "Vaccination Status",font = ('Times new roman',60), bg = "light blue", fg = "red")
        label.grid(row = 0, column = 0)

        frame1 = Frame(self.main, width = 500, relief = 'raised', bd = 10, bg = 'light blue')
        frame1.grid(row = 1, column = 0, columnspan = 3)
        #Search
        search = Label(frame1, text = 'Search', bg = 'light blue', font = ("Times new roman", 16))
        search.grid(row = 0, column = 0, columnspan = 1)
        #search entry box
        name_search = Entry(frame1,bd = 5,width = 125, font = ("Times new roman", 10))
        name_search.grid(row = 0, column = 1)
        search_btn = Button(frame1, text = u'\u00BB', font = ("Times new roman", 15),height = 1, command = lambda:MainWindow.search(text_box, name_search))
        search_btn.grid(row = 0, column = 2)
        #scroll bar at the right
        scroll_x = Scrollbar(frame1, orient = HORIZONTAL)
        scroll_y = Scrollbar(frame1, orient = VERTICAL)

        #Tree view of data base
        text_box = ttk.Treeview(frame1,column = (1,2,3,4,5,6),show = "headings", height = '17',xscrollcommand = scroll_x.set,yscrollcommand = scroll_y.set)
        text_box.grid(row = 1, column = 1, rowspan = 4, padx = 5)

        scroll_x.grid(row = 5, column = 1, sticky = 'ew')
        scroll_y.grid(row = 1, column = 2, rowspan = 5, sticky = 'ns')

        text_box.heading(1, text = "No.")
        text_box.heading(2, text = "First Name")
        text_box.heading(3, text = "Surname")
        text_box.heading(4, text = "BRGY ID")
        text_box.heading(5, text = "Vaccinated or Not")
        text_box.heading(6, text = "Vaccine drug")
        text_box.column(1, width = 25)
        text_box.column(2, width = 150)
        text_box.column(3, width = 150)
        text_box.column(4, width = 150)
        text_box.column(5, width = 150)
        text_box.column(6, width = 150)

        #Some buttons in the main frame
        view_btn = Button(frame1, text = "View All", bg = 'light gray',font = ("Times new roman",10), width = 10,activebackground = 'gray',height = 5, command =lambda:MainWindow.view(frame1,text_box))
        view_btn.grid(row = 1, column = 0)

        filter_btn = Menubutton(frame1, text = "Filter Data", bg = 'light gray',activeforeground = "gray",font = ("Times new roman",10), width = 11, height = 5, relief = 'raised')
        filter_btn.grid(row = 2, column = 0)
        filter_btn.menu = Menu(filter_btn, tearoff = 0)
        filter_btn['menu'] = filter_btn.menu

        filter_btn.menu.add_command(label = "Vaccinated Only", command = lambda:MainWindow.vaccinated(text_box))
        filter_btn.menu.add_command(label = "Not Vaccinated Only", command = lambda:MainWindow.not_vaccinated(text_box))

        edit_btn = Menubutton(frame1, text = "Edit Data",font = ("Times new roman",10), bg = 'light gray',activeforeground = "gray", width = 11,height = 5, relief = 'raised')
        edit_btn.grid(row = 4, column = 0)
        edit_btn.menu = Menu(edit_btn, tearoff = 0)
        edit_btn['menu'] = edit_btn.menu

        edit_btn.menu.add_command(label = "Add", command = lambda:MainWindow.add())
        edit_btn.menu.add_command(label = "Edit/Remove", command = lambda:MainWindow.edit())

        vacc_btn = Menubutton(frame1, text = "Vaccine Drug", bg = 'light gray',activeforeground = "gray",font = ("Times new roman",10), width = 11,height = 5, relief = 'raised')
        vacc_btn.grid(row = 3, column = 0)
        vacc_btn.menu = Menu(vacc_btn, tearoff = 0)
        vacc_btn['menu'] = vacc_btn.menu

        vacc_btn.menu.add_command(label = "Moderna", command = lambda:MainWindow.moderna(text_box))
        vacc_btn.menu.add_command(label = "pficer", command = lambda:MainWindow.pficer(text_box))
        vacc_btn.menu.add_command(label = "sinovac", command = lambda:MainWindow.sinovac(text_box))
        vacc_btn.menu.add_command(label = "sinopharm", command = lambda:MainWindow.sinopharm(text_box))
        vacc_btn.menu.add_command(label = "aztrazeneca", command = lambda:MainWindow.aztracenica(text_box))
        vacc_btn.menu.add_command(label = "sputnik", command = lambda:MainWindow.sputnik(text_box))


    #View all data fram database
    def view(frame1,text_box):
        MainWindow.clear_screen(text_box)
        data = vaccinationDB.view_all()
        for i in data:
            text_box.insert("", "end", values = i)
        
        scroll = Scrollbar(frame1,command=text_box.yview)
        text_box['yscroll'] = scroll.set
        scroll.grid(row = 1, column = 2, rowspan = 5, sticky = 'ns')
        
    #View vaccinated only in the database
    def vaccinated(text_box):
        MainWindow.clear_screen(text_box)
        data = vaccinationDB.vaccinated_only()

        for i in data:
            text_box.insert("", "end", values = i)
            
    #View not vaccinated only form database
    def not_vaccinated(text_box):
        MainWindow.clear_screen(text_box)
        data = vaccinationDB.not_vaccinated_only()

        for i in data:
            text_box.insert("", "end", values = i)

    #Add data to the database
    def add():
        global count1
        global count
        global edit_count
        edit_count = 0
        window = Tk()                                                     
        window.title("Add data")                            #Screen appearance and orientation  
        window_width = 500
        window_height = 600

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x_coordinate = (screen_width/2) - (window_width/2)
        y_coordinate = (screen_height/2) - (window_height/2)
        window.geometry("%dx%d+%d+%d" % (window_width,300,x_coordinate,y_coordinate+150))

        add_frame = Frame(window, bg = "light blue", relief = RAISED , bd = 5, width = 500)
        add_frame.pack(padx = 5, pady = 5)

        add_title = Label(add_frame, text = "Add Data", font = ("Arial", 16), bg = "light blue",padx = 5, pady = 5)
        add_title.grid(row = 0, column = 0, columnspan = 3)

        first_name = Label(add_frame, text = "First Name :", font = ("Arial", 12), bg = "light blue",justify = RIGHT, padx = 5, pady = 5)
        first_name.grid(row = 1, column = 0)
        first_name_entry = Entry(add_frame, bd = 5, width = 50)
        first_name_entry.grid(row = 1, column = 1, padx = 7)

        surname = Label(add_frame, text = "Surname :", font = ("Arial", 12), bg = "light blue",justify = RIGHT, padx = 5, pady = 5)
        surname.grid(row = 2, column = 0)
        surname_entry = Entry(add_frame, bd = 5, width = 50)
        surname_entry.grid(row = 2, column = 1, padx = 7)

        brgyID = Label(add_frame, text = "BRGY ID :", font = ("Arial", 12), bg = "light blue",justify = RIGHT, padx = 5, pady = 5)
        brgyID.grid(row = 4, column = 0)
        brgyID_entry = Entry(add_frame, bd = 5, width = 50)
        brgyID_entry.grid(row = 4, column = 1, padx = 7)
        quest = Label(add_frame, text = "Vaccinated or Not :", font = ("Arial", 12), bg = "light blue", padx = 5, pady = 5)
        quest.grid(row = 5, column = 0)
        

        vaccine_type = Label(add_frame, text = "Vaccine drug :", font = ("Arial", 12), bg = "light blue", padx = 5, pady = 5)
        vaccine_type.grid(row = 6, column = 0)
        

        vacc = Menubutton(add_frame, text = "Options", bg = 'light blue', width = 50, relief = 'raised')
        vacc.grid(row = 5, column = 1, padx = 7)
        vacc.menu = Menu(vacc, tearoff = 0)
        vacc['menu'] = vacc.menu

        vacc.menu.add_command(label = "Vaccinated", command = lambda:MainWindow.vaccinated_count(add_frame))
        vacc.menu.add_command(label = "Not Vaccinated", command = lambda:MainWindow.not_vaccinated_count(add_frame))

        #Disables the button if not vaccinated
        if count != 2:
            vacc_btn = Menubutton(add_frame, text = "Options", bg = 'light blue', width = 50, relief = 'raised', state = NORMAL)
            vacc_btn.grid(row = 6, column = 1, padx = 7)
            vacc_btn.menu = Menu(vacc_btn, tearoff = 0)
            vacc_btn['menu'] = vacc_btn.menu

            vacc_btn.menu.add_command(label = "Moderna", command = lambda:MainWindow.count_moderna(add_frame))
            vacc_btn.menu.add_command(label = "Pficer", command = lambda:MainWindow.count_pficer(add_frame))
            vacc_btn.menu.add_command(label = "Sinovac", command = lambda:MainWindow.count_sinovac(add_frame))
            vacc_btn.menu.add_command(label = "Sinopharm", command = lambda:MainWindow.count_sinopharm(add_frame))
            vacc_btn.menu.add_command(label = "Aztrazeneca",command = lambda:MainWindow.count_aztracenica(add_frame))
            vacc_btn.menu.add_command(label = "Sputnik", command = lambda:MainWindow.count_sputnik(add_frame))
        
        #buttons
        add = Button(add_frame, text = "Add",width = 50, font = ("Arial", 12), bg = "light gray",activebackground = "gray", command = lambda:MainWindow.entry(add_frame,first_name_entry, surname_entry, brgyID_entry))
        add.grid(row = 7, column = 0, columnspan = 3, pady = 5)
        close = Button(add_frame,width = 40, text = "Close", font = ("Arial", 12),bg = "light gray",activebackground = "gray", command = lambda:window.destroy())
        close.grid(row = 8, column = 0,columnspan = 3, pady = 5)
        count = 0
        
        window.mainloop()
    #Edit data or remove data 
    def edit():
        window = Tk()                                                     
        window.title("Edit data")                            #Screen appearance and orientation  
        window_width = 500
        window_height = 600

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x_coordinate = (screen_width/2) - (window_width/2)
        y_coordinate = (screen_height/2) - (window_height/2)
        window.geometry("%dx%d+%d+%d" % (window_width,360,x_coordinate,y_coordinate+100))

        
        
        canvas = Canvas(window, bg = "cadet blue", width = 500, height = 600)
        canvas.grid(row = 0, column = 0, rowspan = 5)

        edit_frame = Frame(window, bg = "light blue", relief = RAISED , bd = 5, width = 500)
        edit_frame.grid(row = 0, column = 0, rowspan = 1)
        
        edit_title = Label(edit_frame, text = "Edit Data", font = ("Arial", 16), bg = "light blue",padx = 5, pady = 5)
        edit_title.grid(row = 0, column = 0, columnspan =3)

        searchID = Label(edit_frame, text = 'Search ID', bg = 'light blue', font = ("Times new roman", 16))
        searchID.grid(row = 1, column = 0, columnspan = 1)

        ID_search = Entry(edit_frame,bd = 5,width = 40, font = ("Times new roman", 10))
        ID_search.grid(row = 1, column = 1, padx = 5)
        search_btn = Button(edit_frame, text = u'\u00BB', font = ("Times new roman", 15),height = 1, command = lambda:MainWindow.show(edit_frame, ID_search))
        search_btn.grid(row = 1, column = 2, padx = 5)
        
        first_name = Label(edit_frame, text = "First Name :", font = ("Arial", 12), bg = "light blue",justify = RIGHT, padx = 5, pady = 5)
        first_name.grid(row = 2, column = 0)
        first_name_ = Entry(edit_frame,bd = 5, width = 30)
        first_name_.grid(row = 2, column = 1, padx = 7)
        

        surname = Label(edit_frame, text = "Surname :", font = ("Arial", 12), bg = "light blue",justify = RIGHT, padx = 5, pady = 5)
        surname.grid(row = 3, column = 0)
        surname_ = Entry(edit_frame, bd = 5, width = 30)
        surname_.grid(row = 3, column = 1, padx = 7)
        
        quest = Label(edit_frame, text = "Vaccinated or Not :", font = ("Arial", 12), bg = "light blue", padx = 5, pady = 5)
        quest.grid(row = 4, column = 0)
        

        vaccine_type = Label(edit_frame, text = "Vaccine drug :", font = ("Arial", 12), bg = "light blue", padx = 5, pady = 5)
        vaccine_type.grid(row = 5, column = 0)
        
        vacc = Menubutton(edit_frame, text = "Options", bg = 'light blue', width = 30, relief = 'raised',state = DISABLED)
        vacc.grid(row = 4, column = 1, padx = 7)

        vacc_btn = Menubutton(edit_frame, text = "Options", bg = 'light blue', width = 30, relief = 'raised', state = DISABLED)
        vacc_btn.grid(row = 5, column = 1, padx = 7)

        save = Button(edit_frame,width = 50, text = "Save", font = ("Arial", 12), bg = "light gray",state = DISABLED, command = lambda:MainWindow.update(edit_frame,first_name_, surname_,ID,ID_search))
        save.grid(row = 7, column = 0, columnspan = 3, pady = 5)

        remove_btn = Button(edit_frame,width = 45, text = "Remove this data", font = ("Arial", 12), bg = "light gray",state = DISABLED, command = lambda:MainWindow.remove(edit_frame,first_name_, surname_,ID,ID_search))
        remove_btn.grid(row = 8, column = 0, columnspan = 3, pady = 5)
        
        close = Button(edit_frame,width = 40, text = "Close", font = ("Arial", 12), bg = "light gray",activebackground = "gray", command = lambda:window.destroy())
        close.grid(row = 9, column = 0,columnspan = 3, pady = 5)
        edit_count = 0
        count = 0
        window.mainloop()
    #Function to show data to edit from database
    def show(edit_frame, ID_search):
        global edit_count
        global count
        global count1
        global text1
        global text2
        edit_count = 1
        ID = ID_search.get()
        data = vaccinationDB.check(ID)
        
        first_name = Label(edit_frame, text = "First Name :", font = ("Arial", 12), bg = "light blue",justify = RIGHT, padx = 5, pady = 5)
        first_name.grid(row = 2, column = 0)
        first_name_ = Entry(edit_frame,bd = 5, width = 30)
        first_name_.grid(row = 2, column = 1, padx = 7)
        

        surname = Label(edit_frame, text = "Surname :", font = ("Arial", 12), bg = "light blue",justify = RIGHT, padx = 5, pady = 5)
        surname.grid(row = 3, column = 0)
        surname_ = Entry(edit_frame, bd = 5, width = 30)
        surname_.grid(row = 3, column = 1, padx = 7)
        
        text1 = ''
        text2 = ''
        for record in data:
            first_name_.insert(0,record[1])
            surname_.insert(0,record[2])
            text1 = record[4]
            text2 = record[5]
        quest = Label(edit_frame, text = "Vaccinated or Not :", font = ("Arial", 12), bg = "light blue", padx = 5, pady = 5)
        quest.grid(row = 4, column = 0)
        

        vaccine_type = Label(edit_frame, text = "Vaccine drug :", font = ("Arial", 12), bg = "light blue", padx = 5, pady = 5)
        vaccine_type.grid(row = 5, column = 0)
        
        if text1 == "Vaccinated":
            count = 1
        elif text1 == "Not Vaccinated":
            count = 2
        vacc = Menubutton(edit_frame, text = text1, bg = 'light blue', width = 30, relief = 'raised')
        vacc.grid(row = 4, column = 1, padx = 7)
        vacc.menu = Menu(vacc, tearoff = 0)
        vacc['menu'] = vacc.menu

        vacc.menu.add_command(label = "Vaccinated", command = lambda:MainWindow.vaccinated_count(edit_frame))
        vacc.menu.add_command(label = "Not Vaccinated", command = lambda:MainWindow.not_vaccinated_count(edit_frame))

        save = Button(edit_frame,width = 50, text = "Save", font = ("Arial", 12), bg = "light gray",activebackground = "gray", command = lambda:MainWindow.update(edit_frame,first_name_, surname_,ID,ID_search))
        save.grid(row = 7, column = 0, columnspan = 3, pady = 5)

        if text2 == "Moderna":
            count1 = 1
        elif text2 == "Pficer":
            count1 = 2
        elif text2 == "Sinovac":
            count1 = 3
        elif text2 == "Sinopharm":
            count1 = 4
        elif text2 == "Aztrazeneca":
            count1 = 5
        elif text2 == "Sputnik":
            count1 = 6
        if count != 2:
            vacc_btn = Menubutton(edit_frame, text = text2, bg = 'light blue', width = 30, relief = 'raised', state = NORMAL)
            vacc_btn.grid(row = 5, column = 1, padx = 7)
            vacc_btn.menu = Menu(vacc_btn, tearoff = 0)
            vacc_btn['menu'] = vacc_btn.menu

            vacc_btn.menu.add_command(label = "Moderna",command = lambda:MainWindow.count_moderna(edit_frame))
            vacc_btn.menu.add_command(label = "Pficer",command = lambda:MainWindow.count_pficer(edit_frame))
            vacc_btn.menu.add_command(label = "Sinovac",command = lambda:MainWindow.count_sinovac(edit_frame))
            vacc_btn.menu.add_command(label = "Sinopharm",command = lambda:MainWindow.count_sinopharm(edit_frame))
            vacc_btn.menu.add_command(label = "Aztrazeneca",command = lambda:MainWindow.count_aztracenica(edit_frame))
            vacc_btn.menu.add_command(label = "Sputnik",command = lambda:MainWindow.count_sputnik(edit_frame))
        remove_btn = Button(edit_frame,width = 45, text = "Remove this data", font = ("Arial", 12), bg = "light gray",activebackground = "gray",state = NORMAL, command = lambda:MainWindow.remove(edit_frame,first_name_, surname_,ID,ID_search))
        remove_btn.grid(row = 8, column = 0, columnspan = 3, pady = 5)

    #Function to update row in database   
    def update(edit_frame, first_name_,surname_,ID,ID_search):
        global edit_count
        
        global count
        global count1
        global text1
        global text2
        firstname = first_name_.get()
        firstname = firstname.title()
        surname = surname_.get()
        surname = surname.title()
        ID = ID
        if count == 0:
            vaccination = text1
            drug = text2
        elif count == 1:
            vaccination = MainWindow.status(edit_frame)
            drug = MainWindow.vacc_drug(edit_frame)
        elif count ==2:
            vaccination = MainWindow.status(edit_frame)
            drug = "N/A"
        vaccinationDB.update_data(firstname,surname,ID,vaccination,drug)
        first_name_.delete(0, END)
        surname_.delete(0, END)
        edit_count = 1
        count = 0
        count1 = 0
        ID_search.delete(0,END)
        MainWindow.vacc_drug(edit_frame)
        MainWindow.status(edit_frame)

    #Function to delete row in the database
    def remove(edit_frame,first_name_, surname_,ID,ID_search):
        global count
        global count1
        vaccinationDB.delete_data(ID)
        first_name_.delete(0,END)
        surname_.delete(0,END)
        ID_search.delete(0,END)
        count = 0
        count1 = 0
        MainWindow.vacc_drug(edit_frame)
        MainWindow.status(edit_frame)


     #Function to search specific data to show in treeview       
    def search(text_box, name_search):
        MainWindow.clear_screen(text_box)
        name = name_search.get()
        data = vaccinationDB.search(name)
        for i in data:
            text_box.insert("","end",values = i)
        
        name_search.delete(0, END)
    #Function to show vaccinated with moderna only
    def moderna(text_box):
        MainWindow.clear_screen(text_box)
        data = vaccinationDB.moderna()
        for i in data:
            text_box.insert("","end",values = i)
    #Function to show vaccinated with pficer only
    def pficer(text_box):
        MainWindow.clear_screen(text_box)
        data = vaccinationDB.pficer()
        for i in data:
            text_box.insert("","end",values = i)
    #Function to show vaccinated with sinovac only
    def sinovac(text_box):
        MainWindow.clear_screen(text_box)
        data = vaccinationDB.sinovac()
        for i in data:
            text_box.insert("","end",values = i)
    #Function to show vaccinated with sinopharm only
    def sinopharm(text_box):
        MainWindow.clear_screen(text_box)
        data = vaccinationDB.sinopharm()
        for i in data:
            text_box.insert("","end",values = i)
    #Function to show vaccinated with aztracenica only
    def aztracenica(text_box):
        MainWindow.clear_screen(text_box)
        data = vaccinationDB.aztracenica()
        for i in data:
            text_box.insert("","end",values = i)
    #Function to show vaccinated with sputnik only
    def sputnik(text_box):
        MainWindow.clear_screen(text_box)
        data = vaccinationDB.sputnik()
        for i in data:
            text_box.insert("","end",values = i)
    #Add data to database after clicking the add button
    def entry(add_frame,first_name_entry, surname_entry,brgyID_entry):
        global count
        global count1
        firstname = first_name_entry.get()
        firstname = firstname.title()
        surname = surname_entry.get()
        surname = surname.title()
        if firstname == "" and surname == "":
            return
        if count == 0:
            return
        if count == 1:
            vaccination = MainWindow.status(add_frame)
            drug = MainWindow.vacc_drug(add_frame)
        elif count ==2:
            vaccination = MainWindow.status(add_frame)
            drug = "N/A"
        ID = brgyID_entry.get()
        
        data = vaccinationDB.check(ID)
        if data:
            showinfo(title = "Oooppps" , message = "BRGY ID already exist in the database!")
            first_name_entry.delete(0, END)
            surname_entry.delete(0, END)
            brgyID_entry.delete(0,END)
            count = 0
            count1 = 0
            MainWindow.vacc_drug(add_frame)
            MainWindow.status(add_frame)
            MainWindow.add()
        else:
            vaccinationDB.add_data(firstname,surname,ID,vaccination,drug)
            first_name_entry.delete(0, END)
            surname_entry.delete(0, END)
            brgyID_entry.delete(0,END)
            count = 0
            count1 = 0
            MainWindow.vacc_drug(add_frame)
            MainWindow.status(add_frame)
    #Function to clear screen on treeview
    def clear_screen(text_box):
        x = text_box.get_children()
        if x != ():
            for child in x:
                text_box.delete(child)
    #Function if not vaccinated or vaccinated
    def status(add_frame):
        global count
        global edit_count
        if count == 0:
            text = "Options"
        elif count == 1:
            text = "Vaccinated"
        elif count == 2:
            text = "Not Vaccinated"
        if edit_count == 1:
            rows = 4
            length = 30
        elif edit_count == 0:
            rows = 5
            length = 50
        vacc = Menubutton(add_frame, text = text, bg = 'light blue', width = length, relief = 'raised')
        vacc.grid(row = rows, column = 1, padx = 7)
        vacc.menu = Menu(vacc, tearoff = 0)
        vacc['menu'] = vacc.menu

        vacc.menu.add_command(label = "Vaccinated", command = lambda:MainWindow.vaccinated_count(add_frame))
        vacc.menu.add_command(label = "Not Vaccinated", command = lambda:MainWindow.not_vaccinated_count(add_frame))
        return text

    def vaccinated_count(add_frame):
        global count
        count = 1
        MainWindow.vacc_drug(add_frame)
        return MainWindow.status(add_frame)
    def not_vaccinated_count(add_frame):
        global count
        count = 2
        MainWindow.vacc_drug(add_frame)
        return MainWindow.status(add_frame)

    def vacc_drug(add_frame):
        global count1
        global count
        global edit_count
    
        if count1 == 0 and count == 1:
            text = "Unknown"
            what = NORMAL
        elif count1 ==1:
            text = "Moderna"
            what = NORMAL
        elif count1 == 2:
            text = "Pficer"
            what = NORMAL 
        elif count1 == 3:
            text = "Sinovac"
            what = NORMAL
        elif count1 == 4:
            text = "Sinopharm"
            what = NORMAL
        elif count1 == 5:
            text = "Aztrazeneca"
            what = NORMAL
        elif count1 == 6:
            text = "Sputnik"
            what = NORMAL
        elif count == 2:
            what = DISABLED
            text = "Options"
        elif(count1 == 6 and count == 2) or (count1 == 5 and count == 2) or (count1 == 4 and count == 2) or \
            (count1 == 3 and count == 2) or (count1 == 2 and count == 2) or (count1 == 1 and count == 2):
            text = "Options"
            what = DISABLED
        elif count == 0:
            text = "Options"
            what = NORMAL
        if edit_count == 1:
            rows = 5
            length = 30
        elif edit_count == 0:
            rows = 6
            length = 50
        vacc_btn = Menubutton(add_frame, text = text, bg = 'light blue', width = length, relief = 'raised', state = what)
        vacc_btn.grid(row = rows, column = 1, padx = 7)
        vacc_btn.menu = Menu(vacc_btn, tearoff = 0)
        vacc_btn['menu'] = vacc_btn.menu

        vacc_btn.menu.add_command(label = "Moderna", command = lambda:MainWindow.count_moderna(add_frame))
        vacc_btn.menu.add_command(label = "Pficer", command = lambda:MainWindow.count_pficer(add_frame))
        vacc_btn.menu.add_command(label = "Sinovac", command = lambda:MainWindow.count_sinovac(add_frame))
        vacc_btn.menu.add_command(label = "Sinopharm", command = lambda:MainWindow.count_sinopharm(add_frame))
        vacc_btn.menu.add_command(label = "Aztrazeneca",command = lambda:MainWindow.count_aztracenica(add_frame))
        vacc_btn.menu.add_command(label = "Sputnik", command = lambda:MainWindow.count_sputnik(add_frame))
        return text
    def count_moderna(add_frame):
        global count1
        count1 = 1
        return MainWindow.vacc_drug(add_frame)

    def count_pficer(add_frame):
        global count1
        count1 = 2
        return MainWindow.vacc_drug(add_frame)

    def count_sinovac(add_frame):
        global count1
        count1 = 3
        return MainWindow.vacc_drug(add_frame)

    def count_sinopharm(add_frame):
        global count1
        count1 = 4
        return MainWindow.vacc_drug(add_frame)
    
    def count_aztracenica(add_frame):
        global count1
        count1 = 5
        return MainWindow.vacc_drug(add_frame)

    def count_sputnik(add_frame):
        global count1
        count1 = 6
        return MainWindow.vacc_drug(add_frame)
main = MainWindow(root)
root.mainloop()
