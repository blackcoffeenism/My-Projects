#Import the needed modules
#================================================================================
import kivy
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from datetime import date
#================================================================================

import data #======> py file where the database is coded


  
  
data.create_data() #Call to create tables on start
data.user_data()
Window.size = (300,500)
Builder.load_file("content.py")
class MyApp(MDApp): #========>>>> THE MAIN CLASS <<<============
    dialog = None
    def build(self):
        
        sm = ScreenManager()                    #\
        sm.add_widget(MainScreen(name = "main"))# \ Used for switching screens
        sm.add_widget(Void(name = "emp"))       #/
        if data.get_user_age() == []:
            return self.setup_profile() #Function on creating profile if not yet created
        return sm
    def setup_profile(self): #===>Function for creating profile
        if not self.dialog:
            #The MDDialog is a built-in function in kivyMD that is used in pop-ups
            self.dialog = MDDialog(
                title="Create Profile\n",
                type="custom",
                content_cls=Profile(),
                size_hint=(1, None),
                auto_dismiss = False,
                )
            self.dialog.open()
    def edit_profile(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Update Your Profile\n",
                type="custom",
                content_cls=edit_Profile(),
                size_hint=(1, None),
                auto_dismiss = False,
                )
            self.dialog.open()
    def closed(self):
        self.dialog.dismiss()
        self.dialog = None
        self.stop()
        MyApp().run()
    def open_popup(self):
        self.dialog = None
        age = data.get_user_age()
        age = int(age[-1][0])
        today = str(date.today())
        total = data.get_total_today(today)
        if (age < 9 and total == 5) or (age<13 and total==7) or (total == 10) :
            if not self.dialog:
                self.dialog = MDDialog(
                    title="Congratulations!!\n",
                    type="custom",
                    content_cls=congratulations(),
                    size_hint=(1, None),
                    auto_dismiss = False,
                    )
                self.dialog.open()
    def ends(self):
        self.dialog.dismiss()
        self.dialog = None

class Profile(BoxLayout): #===>>Class for the creating profile popup
    def user(self):
        name = str(self.ids.user.text)
        age = self.ids.age.text
        if age == "":
            age = 0
        else:
            age = int(self.ids.age.text)
        if name == "":
            name = "No Name"
        data.insert_user(name,age)
class edit_Profile(BoxLayout): #====>Class for editing profile popup
    def edit_user(self):
        name = self.ids.user.text
        if name == "":
            name = "No Name"
        age = self.ids.age.text
        if age == "":
            age = 0
        else:
            age = int(self.ids.age.text)
        data.insert_user(name,age)

class congratulations(BoxLayout):
    
    pass
class MainScreen(Screen): #====>The screen where we find the buttons 
    dialog = None
    #We have total of 10 buttons
    #The function count1 to count10 will add the count of glass of water drank
    #This functions also change the icons of button into check
    def count1(self):
        today = str(date.today())
        if  self.ids.one.icon == "check":
            return
        data.add(1,today)
        total = data.get_total_today(today)
        self.ids.one.icon = "check"
    def count2(self):
        today = str(date.today())
        if  self.ids.two.icon == "check":
            return
        data.add(1,today)
        total = data.get_total_today(today)
        self.ids.two.icon = "check"
    def count3(self):
        today = str(date.today())
        if  self.ids.three.icon == "check":
            return
        data.add(1,today)
        total = data.get_total_today(today)
        self.ids.three.icon = "check"
    def count4(self):
        today = str(date.today())
        if  self.ids.four.icon == "check":
            return
        data.add(1,today)
        total = data.get_total_today(today)
        self.ids.four.icon = "check"
    def count5(self):
        today = str(date.today())
        if  self.ids.five.icon == "check":
            return
        data.add(1,today)
        total = data.get_total_today(today)
        self.ids.five.icon = "check"
    def count6(self):
        today = str(date.today())
        if  self.ids.six.icon == "check":
            return
        data.add(1,today)
        total = data.get_total_today(today)
        self.ids.six.icon = "check"
    def count7(self):
        today = str(date.today())
        if  self.ids.seven.icon == "check":
            return
        data.add(1,today)
        total = data.get_total_today(today)
        self.ids.seven.icon = "check"
    def count8(self):
        today = str(date.today())
        if  self.ids.eight.icon == "check":
            return
        data.add(1,today)
        total = data.get_total_today(today)
        self.ids.eight.icon = "check"
    def count9(self):
        today = str(date.today())
        if  self.ids.nine.icon == "check":
            return
        data.add(1,today)
        total = data.get_total_today(today)
        self.ids.nine.icon = "check"
    def count10(self):
        today = str(date.today())
        if  self.ids.ten.icon == "check":
            return
        data.add(1,today)
        total = data.get_total_today(today)
        self.ids.ten.icon = "check"

    #The function check_btn1 to check_btn10 will change the icon of buttons
    #This changes of icons is base on the database
    def check_btn1(self):
        today = str(date.today())
        total = data.get_total_today(today)
        if total == 0:
            return "cup-water"
        else:
            return "check"
            
    def check_btn2(self):
        today = str(date.today())
        total = data.get_total_today(today)
        if total < 2:
            return "cup-water"
        else:
            return "check"
    def check_btn3(self):
        today = str(date.today())
        total = data.get_total_today(today)
        if total < 3:
            return "cup-water"
        else:
            return "check"
    def check_btn4(self):
        today = str(date.today())
        total = data.get_total_today(today)
        if total < 4:
            return "cup-water"
        else:
            return "check"
    def check_btn5(self):
        today = str(date.today())
        total = data.get_total_today(today)
        if total < 5:
            return "cup-water"
        else:
            return "check"
    def check_btn6(self):
        today = str(date.today())
        total = data.get_total_today(today)
        if total < 6:
            return "cup-water"
        else:
            return "check"
    def check_btn7(self):
        today = str(date.today())
        total = data.get_total_today(today)
        if total < 7:
            return "cup-water"
        else:
            return "check"
    def check_btn8(self):
        today = str(date.today())
        total = data.get_total_today(today)
        if total < 8:
            return "cup-water"
        else:
            return "check"
    def check_btn9(self):
        today = str(date.today())
        total = data.get_total_today(today)
        if total < 9:
            return "cup-water"
        else:
            return "check"
    def check_btn10(self):
        today = str(date.today())
        total = data.get_total_today(today)
        if total < 10:
            return "cup-water"
        else:
            return "check"
        
    def text(self): #============>This function will be called to return a text with name from the database
        name = data.get_user_name()
        
        text = "Hello "+name+"!!! This is the suggested number of glasses\n"\
               "you need to take per day."
        return text
    #The function disabling_btn6 to disabling_btn10 will disable the other buttons based on the age of user
    def disabling_btn6(self):
        age = data.get_user_age()
        if age == []:
            return False
        age = int(age[-1][0])
        if age < 9 :
            return True
    def disabling_btn7(self):
        age = data.get_user_age()
        if age == []:
            return False
        age = int(age[-1][0])
        if age < 9:
            return True
    def disabling_btn8(self):
        age = data.get_user_age()
        if age == []:
            return False
        age = int(age[-1][0])
        if age < 13:
            return True
        
    def disabling_btn9(self):
        age = data.get_user_age()
        if age == []:
            return False
        age = int(age[-1][0])
        if age < 13:
            return True
    def disabling_btn10(self):
        age = data.get_user_age()
        if age == []:
            return False
        age = int(age[-1][0])
        if age < 13:
            return True
    
            
class Void(Screen):
    pass
if __name__ == "__main__":
    MyApp().run()
