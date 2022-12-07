<MainScreen>:
    name: "main"
    MDBoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title:'Drinking Reminder'
            elevation: 10
            MDIconButton:
                icon: "account-edit"
                on_release:
                    app.edit_profile()
        
        FloatLayout:
            MDLabel: #==== The text on Main Screen
                id: info
                text: root.text()
                pos_hint:{"center_x":.5,"center_y":.9}
                font_style: "Caption"
                size: self.texture_size

            #The 10 buttons
            MDFloatingActionButton:
                id: one
                icon: root.check_btn1()
                md_bg_color: app.theme_cls.primary_color
                pos_hint:{"center_x":.1,"center_y":-.1}
                disabled: False
                on_press:
                    root.count1()
                    app.open_popup()

            MDFloatingActionButton:
                id: two
                icon: root.check_btn2()
                md_bg_color: app.theme_cls.primary_color
                pos_hint:{"center_x":.3,"center_y":-.1}
                disabled: False
                on_press:
                    root.count2()
                    app.open_popup()

            MDFloatingActionButton:
                id: three
                icon: root.check_btn3()
                md_bg_color: app.theme_cls.primary_color
                pos_hint:{"center_x":.5,"center_y":-.1}
                disabled: False
                on_press:
                    root.count3()
                    app.open_popup()

            MDFloatingActionButton:
                id: four
                icon: root.check_btn4()
                md_bg_color: app.theme_cls.primary_color
                pos_hint:{"center_x":.7,"center_y":-.1}
                disabled: False
                on_press:
                    root.count4()
                    app.open_popup()

            MDFloatingActionButton:
                id: five
                icon: root.check_btn5()
                md_bg_color: app.theme_cls.primary_color
                pos_hint:{"center_x":.9,"center_y":-.1}
                disabled: False
                on_press:
                    root.count5()
                    app.open_popup()                

            MDFloatingActionButton:
                id: six
                icon: root.check_btn6()
                md_bg_color: app.theme_cls.primary_color
                pos_hint:{"center_x":.1,"center_y":-.4}
                disabled: root.disabling_btn6()
                on_press:
                    root.count6()
                    app.open_popup()

            MDFloatingActionButton:
                id: seven
                icon: root.check_btn7()
                md_bg_color: app.theme_cls.primary_color
                pos_hint:{"center_x":.3,"center_y":-.4}
                disabled: root.disabling_btn7()
                on_press:
                    root.count7()
                    app.open_popup()

            MDFloatingActionButton:
                id: eight
                icon: root.check_btn8()
                md_bg_color: app.theme_cls.primary_color
                pos_hint:{"center_x":.5,"center_y":-.4}
                disabled: root.disabling_btn8()
                on_press:
                    root.count8()
                    app.open_popup()

            MDFloatingActionButton:
                id: nine
                icon: root.check_btn9()
                md_bg_color: app.theme_cls.primary_color
                pos_hint:{"center_x":.7,"center_y":-.4}
                disabled: root.disabling_btn9()
                on_press:
                    root.count9()
                    app.open_popup()

            MDFloatingActionButton:
                id: ten
                icon: root.check_btn10()
                md_bg_color: app.theme_cls.primary_color
                pos_hint:{"center_x":.9,"center_y":-.4}
                disabled: root.disabling_btn10()
                on_press:
                    root.count10()
                    app.open_popup()
        Widget:

<Profile>: #Content of profile creating popup
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "120dp"

    MDTextField: #User name input
        id: user
        hint_text: "Username"
        icon_right: "account"
        pos_hint:{"center_x":.5, "center_y":.2}
    MDTextField: #User age input
        id: age
        hint_text: "Age"
        icon_right: "account"
        input_filter: 'int'
        pos_hint:{"center_x":.5, "center_y":.1}

    MDFlatButton:
        text: "OK"
        theme_text_color:"Custom"
        text_color:app.theme_cls.primary_color
        pos_hint:{"center_x":.5, "center_y":0}
        on_press:
            root.user()
        on_release:
            app.closed()
<edit_Profile>: #Content of editing profile popup. Almost the same on creating profile
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "120dp"
    MDTextField:
        id: user
        hint_text: "Username"
        icon_right: "account"
        pos_hint:{"center_x":.5, "center_y":.2}
    MDTextField:
        id: age
        hint_text: "Age"
        icon_right: "account"
        input_filter: 'int'

    MDFlatButton:
        text: "OK"
        theme_text_color:"Custom"
        text_color:app.theme_cls.primary_color
        pos_hint:{"center_x":.5, "center_y":0}
        on_press:
            root.edit_user()
            app.root.current = "emp"
        on_release:
            app.closed()
            
<Void>: #Empty screen to clear screen
    name: "emp"
    MDBoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title:''
            elevation: 10
        Widget:
    
<congratulations>: #Congratulation message every finished task
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "120dp"

    MDLabel:
        text: "Congratulations!! You completed your daily goal."

    MDFlatButton:
        text: "OK"
        theme_text_color:"Custom"
        text_color:app.theme_cls.primary_color
        pos_hint:{"center_x":.5, "center_y":0}
        on_release:
            app.ends()
    
