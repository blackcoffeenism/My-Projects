from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.uix.label import MDLabel

from kivymd.uix.dialog import MDDialog
from kivy.core.clipboard import Clipboard
from kivymd.uix.button import MDRaisedButton

from kivymd.uix.card import MDCard
import requests
from bs4 import BeautifulSoup




class MD3Card(MDCard):
    '''Implements a material design v3 card.'''

    text = StringProperty()
    source = StringProperty()
    link = StringProperty()
    job_location = StringProperty()
    job_salary = StringProperty()
    company = StringProperty()
    benefit = StringProperty()
    def button_pressed(self):
        title = self.ids.label.text
        self.link = self.ids.link.link
        job_location = self.ids.link.job_location
        job_salary = self.ids.link.job_salary
        company = self.ids.link.company
        copy_link = MDRaisedButton(text="Copy Link",
                                   pos_hint = {'center_x': 0.5,'center_y': 0.5},
                                   md_bg_color= '#2F3C7E',
                                   on_release = self.cop)
        info = (company+'\n'+job_location+'\n'+job_salary)
        dialog = MDDialog(title=title, text=info,buttons=[copy_link])
        dialog.open()

    def cop(self,obj):
        Clipboard.copy(self.link)

class MyApp(MDApp):
    def build(self):
        return Builder.load_file('main.kv')
    
    def on_start(self):
        html_text = requests.get('https://www.jobstreet.com.ph/python-developer-jobs').text
        soup = BeautifulSoup(html_text, 'html.parser')
        job = soup.find_all('div', class_ = 'z1s6m00 _1hbhsw69y _1hbhsw68u _1hbhsw67e _1hbhsw67q')
        for vacant in job:
            job_name = vacant.h1.text
            com_name = vacant.find('span', class_ = 'z1s6m00 bev08l1 _1hbhsw64y _1hbhsw60 _1hbhsw6r').text
            location = vacant.find('span', class_ = 'z1s6m00 _1hbhsw64y y44q7i0 y44q7i3 y44q7i21 y44q7ih').text
            salary = vacant.find_all('span', class_ = 'z1s6m00 _1hbhsw64y y44q7i0 y44q7i3 y44q7i21 y44q7ih')

             
            link1 = str(vacant.a.get('href'))
            link1 = ('www.jobstreet.com.ph'+link1)
        
            imgs = vacant.find('img', class_ = 'z1s6m00 rqoqz6')
            if imgs == None:
                img_url = "replacement.jpg"
            else:
                img_url = imgs['src']
                img_url = str(img_url)
                
            if salary[-1].text == location:
                salary = "Not Available! Check online"
            else:
                salary = salary[-1].text
            self.root.ids.box.add_widget(
                MD3Card(
                    line_color=(0.2, 0.2, 0.2, 0.8),
                    style='elevated',
                    text=job_name,
                    source = img_url,
                    link = link1,
                    job_location = location,
                    job_salary = salary,
                    company = com_name,
                    md_bg_color="#ffffff",
                    shadow_offset=(0, -1),
                )
            )
        self.root.ids.box.add_widget(
            MDLabel(text="Developer: Gerald Delima",
            halign = 'center'),
        )
        
    


MyApp().run()