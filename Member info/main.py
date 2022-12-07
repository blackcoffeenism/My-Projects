from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
from tkcalendar import Calendar
import datetime
from PIL import ImageTk, Image
import os
import csv
import info_data

root = Tk()
root.title("MEMBER DATABASE SYSTEM")
root_width = 1200
root_height = 600

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_coordinate = (screen_width/2) - (root_width/2)
y_coordinate = (screen_height/2) - (root_height/2)
root.geometry("%dx%d+%d+%d" % (root_width,root_height,x_coordinate,y_coordinate))
root.resizable(0,0)

data = []
count = 0
class Screen:
    def front_end(root):
        global data
        canvas = Canvas(root, bg = "cadet blue", width = 1200, height = 600)
        canvas.grid(row = 0, column = 0, rowspan = 5)
        
#========================= TOP ==================================================================================================================
#=================== LOGO AND TITLE =============================================================================================================
        top_frame = LabelFrame(root,text = "DATABASE",width = 125, bd = 1)
        top_frame.grid(row = 0, column = 0, columnspan = 3, sticky = 'nesw')
        #img1 = Image.open('logo.png')
        #img1 = img1.resize((250,75), Image.ANTIALIAS)

        #image1 = ImageTk.PhotoImage(img1)
        
        #logo = Label(top_frame, image = image1)
        #logo.image = image1
        #logo.pack()
        label = Label(top_frame, text = "MEMBER DATABASE SYSTEM",font = ('Times new roman',25), fg = "black")
        label.pack(side=TOP)
#=================================================================================================================================================

#====================== NEXT FRAME ===============================================================================================================
#==================== SEARCH AND FILTER ==========================================================================================================
        search_frame = LabelFrame(root,text = "SEARCH",width = 125, bd = 1)
        search_frame.grid(row = 1, column = 0, columnspan = 3, sticky = 'nwes')
        #SEARCH ENTRY
        name_search = Entry(search_frame,bd = 0,width = 20, font = ("Times new roman", 12),relief = 'flat')
        name_search.pack(side = LEFT, padx = 10)
        #GENDER FILTER BUTTON
        Gender_btn = Menubutton(search_frame, text = "Gender", font = ('Times new roman',12), bg = "white", fg = "black", height = 1, width = 5, activeforeground = 'gray')
        Gender_btn.pack(side = LEFT, padx = 10)
        Gender_menu = Menu(Gender_btn)
        Gender_btn.configure(menu=Gender_menu)
        gen = "Male"
        Gender_menu.add_radiobutton(label = "Male", command = lambda:Screen.gender_filter(text_box,frame,"Male"))
        Gender_menu.add_radiobutton(label = "Female", command = lambda:Screen.gender_filter(text_box,frame,"Female"))
        
        #ROLE FILTER BUTTON
        Pledge_btn = Menubutton(search_frame, text = "Role", font = ('Times new roman',12), bg = "white", fg = "black", height = 1, width = 5, activeforeground = 'gray')
        Pledge_btn.pack(side = LEFT, padx = 10)
        Pledge_menu = Menu(Pledge_btn)
        Pledge_btn.configure(menu=Pledge_menu)
        Pledge_menu.add_radiobutton(label = "Leader", command = lambda:Screen.pledge_filter(text_box,frame,"Leader"))
        Pledge_menu.add_radiobutton(label = "Member", command = lambda:Screen.pledge_filter(text_box,frame,"Member"))
        #VIEW ALL BUTTON
        view_btn = Button(search_frame, text = "All", font = ('Times new roman',12),
                            bg = "white", fg = "black", height = 1, width = 10, activeforeground = 'gray',
                            command = lambda:Screen.all(text_box,frame))
        view_btn.pack(side = LEFT, padx = 10)
        #IMPORT CSV BUTTON
        import_btn = Button(search_frame, text = "Import", font = ('Times new roman',12),
                            bg = "white", fg = "black", height = 1, width = 10, activeforeground = 'gray',
                            command = lambda:Screen.importcsv(text_box, frame))
        import_btn.pack(side = LEFT, padx = 5)
        #EXPORT CSV BUTTON
        export_btn = Button(search_frame, text = "Export", font = ('Times new roman',12),
                            bg = "white", fg = "black", height = 1, width = 10, activeforeground = 'gray',
                            command = lambda:Screen.export())
        export_btn.pack(side = LEFT, padx = 5)

#==================== THIRD FRAME ================================================================================================================
#==================== TREE VIEW ==================================================================================================================
        frame = LabelFrame(root, text = "TREE VIEW",width = 100, bd = 1)
        frame.grid(row = 2, column = 0,columnspan = 3,sticky = 'nesw')

        scroll_x = Scrollbar(frame, orient = HORIZONTAL)
        scroll_y = Scrollbar(frame, orient = VERTICAL)
        
        scroll_y.grid(row = 1, column = 2, rowspan = 5, sticky = 'ns')
        
        text_box = ttk.Treeview(frame,column = (1,2,3,4,5),show = "headings", height = '17',xscrollcommand = scroll_x.set,yscrollcommand = scroll_y.set)
        text_box.grid(row = 1, column = 1, rowspan = 4, padx = 5, sticky = 'nesw')
        
        text_box.heading(1, text = "No.")
        text_box.heading(2, text = "Name")
        text_box.heading(3, text = "Gender")
        text_box.heading(4, text = "Role")
        text_box.heading(5, text = "Birthday")
        text_box.column(1, width = 25)
        text_box.column(2, width = 187)
        text_box.column(3, width = 187)
        text_box.column(4, width = 187)
        text_box.column(5, width = 187)

        
        edit_btn = Button(frame, text = "Edit", bd = 1, font = ("Times new roman", 12), width = 6, command = lambda:Screen.edit(frame,text_box))
        edit_btn.grid(row = 1, column = 3, padx = 13)

        del_btn = Button(frame, text = "Delete", bd = 1, font = ("Times new roman", 12), width = 6, command = lambda:Screen.delete_item(text_box,frame))
        del_btn.place(anchor = NW, relx = 0.678, rely = 0.2)
        Screen.add_edit(root,frame,text_box)
        Screen.all(text_box, frame)
        name_search.bind('<Return>',lambda event:Screen.search(name_search,frame,text_box))
        
#=================================== LAST FRAME ============================================================================================
#================================= ADDING AND EDITING ======================================================================================
    def add_edit(root,frame,text_box):
        global individual_info
        data_frame = LabelFrame(root, text = "ADD MEMBER",width = 150, bd = 1, bg = 'sky blue')
        data_frame.place(anchor = NW, relx = 0.77, rely = 0.14)

        name = Entry(data_frame,bd = 0,width = 20, font = ("Times new roman", 12))
        name.place(anchor = NW, relx = 0.35)

        nameLabel = Label(data_frame, text = "Name", font = ("Times new roman", 12), bg = 'sky blue')
        nameLabel.grid(row = 0, column = 0, sticky = 'w')



        #GENDER RADIO BUTTON
        GenderLabel = Label(data_frame, text = "Gender", font = ("Times new roman", 12),bg = "light blue")
        GenderLabel.grid(row = 1, column = 0,columnspan = 2, sticky = 'news')

        genderselection = StringVar()
        Gender1 = Radiobutton(data_frame,text = "Male", bd = 0, font = ("Times new roman", 12), bg = 'sky blue', variable = genderselection, value = "Male")
        Gender1.grid(row = 2, column = 0, sticky = 'w')

        Gender2 = Radiobutton(data_frame,text = "Female", bd = 0, font = ("Times new roman", 12), bg = 'sky blue', variable = genderselection, value = "Female")
        Gender2.grid(row = 2, column = 1, sticky = 'w')



        #ROLE RADIO BUTTON
        PledgeLabel = Label(data_frame, text = "Role", font = ("Times new roman", 12), bg = 'light blue')
        PledgeLabel.grid(row = 5, column = 0,columnspan = 2, sticky = 'news')
        
        pledgeselection = StringVar()
        pledge1 = Radiobutton(data_frame,text = "Leader", bd = 0, font = ("Times new roman", 12), bg = 'sky blue', variable = pledgeselection,
                              value = "Leader")
        pledge1.grid(row = 6, column = 0, sticky = 'w')

        pledge2 = Radiobutton(data_frame,text = "Member", bd = 0, font = ("Times new roman", 12), bg = 'sky blue', variable = pledgeselection,
                              value = "Member")
        pledge2.grid(row = 6, column = 1, sticky = 'w')


        #BIRHTDAY
        birthLabel = Label(data_frame, text = "Birthday", font = ("Times new roman", 12), bg = 'light blue')
        birthLabel.grid(row = 7, column = 0, columnspan = 2, sticky = 'news')
        birthLabel.config(text = "Birthday")
        
        current_time = datetime.datetime.now()
        calendar = Calendar(data_frame, selectmode = 'day',
               year = current_time.year, month = current_time.month,
               day = current_time.day, width = 1)
        calendar.grid(row = 8, column = 0, columnspan = 2)
        Screen.clr(name, genderselection,pledgeselection)
        add_btn = Button(data_frame, text = "Add", bd = 1, font = ("Times new roman", 12), width = 6,
                         command = lambda:Screen.add(name,genderselection,pledgeselection,calendar,frame,text_box))
        add_btn.grid(row = 9, column = 0)
        
        clear_btn = Button(data_frame, text = "Cancel", bd = 1, font = ("Times new roman", 12),
                           width = 6, command = lambda:Screen.clr(name, genderselection,
                                                                  pledgeselection))
        clear_btn.grid(row = 9, column = 1)
# ================== ADDING TO DATABASE =====================================================================================
    def add(name,genderselection,pledgeselection,calendar,frame,text_box):
        names = name.get()
        gender = genderselection.get()
        pledge = pledgeselection.get()
        bday = calendar.get_date()
        info_data.add(names.title(),gender,pledge,bday)
        Screen.all(text_box, frame)
        return Screen.clr(name,genderselection,pledgeselection)

#================= CLEAR ADD/EDIT SECTION =============================================================================================
    def clr(name, genderselection, pledgeselection):
        name.delete(0, END)
        genderselection.set(None)
        pledgeselection.set(None)
        return

    def edit(frame,text_box):
        selected_item = text_box.selection()        
        if len(selected_item) == 0:
            messagebox.showerror("Notice!", "No selected data!!")
            return
        elif len(selected_item) >1:
            messagebox.showerror("Notice!", "You can edit one at a time!!")
            return
        item = text_box.item(selected_item)
        items = item.get("values")
        root = Tk()
        root.title("MEMBER DATABASE SYSTEM")
        root_width = 250
        root_height = 450

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x_coordinate = (screen_width/2) - (root_width/2)
        y_coordinate = (screen_height/2) - (root_height/2)
        root.geometry("%dx%d+%d+%d" % (root_width,root_height,x_coordinate,y_coordinate))
        root.resizable(0,0)
        data_frame = LabelFrame(root, text = "EDIT MEMBERSHIP",width = 150, bd = 1, bg = 'sky blue')
        data_frame.pack()

        name = Entry(data_frame,bd = 0,width = 20, font = ("Times new roman", 12))
        name.place(anchor = NW, relx = 0.35)

        nameLabel = Label(data_frame, text = "Name", font = ("Times new roman", 12), bg = 'sky blue')
        nameLabel.grid(row = 0, column = 0, sticky = 'w')



        #GENDER RADIO BUTTON
        GenderLabel = Label(data_frame, text = "Gender", font = ("Times new roman", 12),bg = "light blue")
        GenderLabel.grid(row = 1, column = 0,columnspan = 2, sticky = 'news')

        gendersel = StringVar()
        Gender1 = Radiobutton(data_frame,text = "Male", bd = 0, font = ("Times new roman", 12), bg = 'sky blue', variable = gendersel, value = "Male",
                              command = lambda:gendersel.set("Male"))
        Gender1.grid(row = 2, column = 0, sticky = 'w')

        Gender2 = Radiobutton(data_frame,text = "Female", bd = 0, font = ("Times new roman", 12), bg = 'sky blue', variable = gendersel, value = "Female",
                              command = lambda:gendersel.set("Female"))
        Gender2.grid(row = 2, column = 1, sticky = 'w')



        #ROLE RADIO BUTTON
        PledgeLabel = Label(data_frame, text = "Role", font = ("Times new roman", 12), bg = 'light blue')
        PledgeLabel.grid(row = 5, column = 0,columnspan = 2, sticky = 'news')
        
        pledgesel = StringVar()
        pledge1 = Radiobutton(data_frame,text = "Leader", bd = 0, font = ("Times new roman", 12), bg = 'sky blue', variable = pledgesel,
                              value = "Leader",command = lambda:pledgesel.set("Leader"))
        pledge1.grid(row = 6, column = 0, sticky = 'w')

        pledge2 = Radiobutton(data_frame,text = "Member", bd = 0, font = ("Times new roman", 12), bg = 'sky blue', variable = pledgesel,
                              value = "Member", command = lambda:pledgesel.set("Member"))
        pledge2.grid(row = 6, column = 1, sticky = 'w')


        #BIRHTDAY
        birthLabel = Label(data_frame, text = "Birthday", font = ("Times new roman", 12), bg = 'light blue')
        birthLabel.grid(row = 7, column = 0, columnspan = 2, sticky = 'news')
        birthLabel.config(text = "Birthday")
        
        current_time = datetime.datetime.now()
        cal = items[4].split('/')
        if int(cal[2])== 00 or int(cal[2])<= 50:
            cal[2] = '20'+cal[2]
        else:
            cal[2] = '19'+cal[2]
        calendar = Calendar(data_frame, selectmode = 'day',
               year = int(cal[2]), month =int(cal[0]),
                day = int(cal[1]), width = 1)
        calendar.grid(row = 8, column = 0, columnspan = 2)
        
        
        ids = info_data.sel_id(items[1])
        ids = ids[0][0]
        name.insert(0,items[1])
        gendersel.set(items[2])
        pledgesel.set(items[3])
        
        update_btn = Button(data_frame, text = "Update", bd = 1, font = ("Times new roman", 12), width = 6,
                            command = lambda:Screen.update(name,gendersel,pledgesel,calendar,frame,text_box,root,ids))
        update_btn.grid(row = 9, column = 0)
        
        clear_btn = Button(data_frame, text = "Cancel", bd = 1, font = ("Times new roman", 12),
                           width = 6, command = lambda:root.destroy())
        clear_btn.grid(row = 9, column = 1)

        root.mainloop()

    def update(name,gendersel,pledgesel,calendar,frame,text_box,root,ids):
        names = name.get()
        gender = gendersel.get()
        pledge = pledgesel.get()
        bday = calendar.get_date()
        info_data.update(names.title(),gender,pledge,bday,ids)
        Screen.all(text_box, frame)
        return root.destroy()
    
    def delete_item(text_box,frame):
        selected_item = text_box.selection()
        items = []
        for i in selected_item:
            item = text_box.item(i)
        
            items.append(item.get("values"))
            text_box.delete(i)
        for item in items:
            info_data.delete_item(item[1])

        Screen.all(text_box, frame)

        return

    #EXPORT CSV
    def export():
        global data
        data_count = 0
        if len(data) == 0:
            messagebox.showerror("Notice", "No available data to export!!")
            return False

        else:
            fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save CSV", filetypes=(("CSV File", "*.csv"), ("All Files", "*.")))
            with open(fln,'w', newline = "") as myfile:
                fieldnames = ["No.", "Name", "Gender", "Role", "Birthday"]
                exp_writer = csv.DictWriter(myfile, fieldnames=fieldnames)

                exp_writer.writeheader()
                for i in data:
                    data_count+=1
                    exp_writer.writerow({"No.":data_count, "Name":i[1], "Gender":i[2], "Role":i[3], "Birthday":i[4]})

            messagebox.showinfo("Done", "Successfully Exported")
                

    #IMPORT CSV
    def importcsv(text_box, frame):
        master_list = info_data.get_all()
        fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open CSV file", filetypes=(("CSV File","*.csv"),("All Files","*.*")))
        if fln:
            with open(fln) as myfile:
                csvread = csv.reader(myfile, delimiter=',')
                for i in csvread:
                    a = i[3].split('/')
                    if len(a[2]) > 2:
                        i[3] = i[3][:-4]+i[3][-2:]
                    info_data.add(i[0].title(), i[1], i[2], i[3])
            Screen.all(text_box, frame)
        else:
            return

        #SHOW ALL
    def all(text_box,frame):
        global data
        data.clear()
        master_list = info_data.get_all()
        Screen.clear_screen(text_box)
        count = 0
        for i in master_list:
            new = list(i)
            new[0] = count+1
            text_box.insert("", "end", values = new)
            count+=1

        scroll = Scrollbar(frame,command=text_box.yview)
        text_box['yscroll'] = scroll.set
        scroll.grid(row = 1, column = 2, rowspan = 5, sticky = 'ns')
        data = master_list

    def gender_filter(text_box,frame,gen):
        global data
        data.clear()
        master_list = info_data.get_gender(gen)
        Screen.clear_screen(text_box)
        count = 0
        for i in master_list:
            new = list(i)
            new[0] = count+1
            text_box.insert("", "end", values = new)
            count+=1

        scroll = Scrollbar(frame,command=text_box.yview)
        text_box['yscroll'] = scroll.set
        scroll.grid(row = 1, column = 2, rowspan = 5, sticky = 'ns')
        data = master_list


    def pledge_filter(text_box,frame,pledge):
        global data
        data.clear()
        master_list = info_data.get_status(pledge)
        Screen.clear_screen(text_box)
        count = 0
        for i in master_list:
            new = list(i)
            new[0] = count+1
            text_box.insert("", "end", values = new)
            count+=1

        scroll = Scrollbar(frame,command=text_box.yview)
        text_box['yscroll'] = scroll.set
        scroll.grid(row = 1, column = 2, rowspan = 5, sticky = 'ns')
        data = master_list

    #CLEAR SCREEN
    def clear_screen(text_box):
        x = text_box.get_children()
        if x != ():
            for child in x:
                text_box.delete(child)

        return
    #SEARCHING
    def search(name_search,frame,text_box):
        master_list = info_data.search(name_search.get())
        Screen.clear_screen(text_box)
        count = 0
        for i in master_list:
            new = list(i)
            new[0] = count+1
            text_box.insert("", "end", values = new)
            count+=1

        scroll = Scrollbar(frame,command=text_box.yview)
        text_box['yscroll'] = scroll.set
        scroll.grid(row = 1, column = 2, rowspan = 5, sticky = 'ns')

        
        




Screen.front_end(root)
root.mainloop()
