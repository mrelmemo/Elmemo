from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen , SlideTransition
import requests
from bs4 import BeautifulSoup
from kivymd.uix.button import MDRectangleFlatButton
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivymd.uix.textfield import MDTextFieldRound
import arabic_reshaper
from bidi.algorithm import get_display
global found
global Bseries
Bseries = False
found =[]
Window.size = (400,630)
class BidiTextInput(MDTextFieldRound):
    def _create_line_label(self, text, hint=False):
        reshaped_text = arabic_reshaper.reshape(text)
        text = get_display(reshaped_text)
        super(BidiTextInput, self)._create_line_label(text, hint)
class WindowManager(ScreenManager):
    pass
class FResults(Screen):
    def get_buttons(self):
        for i in range(len(found)):
            x = found[i].text.rstrip()
            x = x.rstrip()
            x = x.rstrip()
            x = x.strip('\n')
            x = x.strip('\n')
            x = x.replace('\n', ' ')
            button = MDRectangleFlatButton(text=x,    theme_text_color="Primary")
            self.ids.bl_main.add_widget(button)
    def go_back(self):
        self.manager.transition.direction = 'down'
        self.manager.current = 'ssearch' if Bseries else 'fsearch'


class FSearch(Screen):
    def i_clicked(self,s):
        global found
        found = []
        i=1
        while True:
            fbool = found
            result_new = requests.get("https://mycima.world/search/" + s + "/page/" + str(i))
            srcm = result_new.content
            soup = BeautifulSoup(srcm, "lxml")
            Found = soup.find_all("strong", {"dir": "auto"})
            found = found + Found
            if fbool == found:
                break
            i = i + 1
        if found:
            self.manager.get_screen('fresults').get_buttons()
            self.manager.transition.direction = 'up'
            self.manager.current='fresults'
    def series(self):
        global Bseries
        Bseries= True
        self.manager.transition.direction = 'right'
        self.manager.current = 'ssearch'
class SSearch(Screen):
    def i_clicked(self,s):
        global found
        found = []
        i=1
        while True:
            fbool = found
            result_new = requests.get("https://mycima.run:2096/search/" + s + "/list/series/?page_number=" + str(i))
            srcm = result_new.content
            soup = BeautifulSoup(srcm, "lxml")
            Found = soup.find_all("strong", {"dir": "auto"})
            found = found + Found
            if fbool == found:
                break
            i = i + 1
        if found:
            self.manager.get_screen('fresults').get_buttons()
            self.manager.transition.direction = 'up'
            self.manager.current='fresults'
    def movies(self):
        global Bseries
        Bseries= False
        self.manager.transition.direction = 'left'
        self.manager.current = 'fsearch'




hm_cinema = """
WindowManager:
    FSearch:
    FResults:
    SSearch:
<FSearch>:
    name: "fsearch"
    canvas:
        Color:
            rgb: 0x26 / 255.0, 0x32 / 255.0, 0x38 / 255.0
        Rectangle:
            size: self.size  
    Image:
        source: 'img/head.jpeg'
        size: 100,50
        pos: (0,0.2)
        pos_hint: { 'center_x' :0.5,'y':0.4}
    Label:
        text: 'Welcome to HM Cinema Movies section'
        font_size: 14
        pos_hint: { 'center_x' :0.5,'y':0.15}

    MDRectangleFlatButton:
        text: 'Series'
        on_release: root.series()
        size: 100,50
        pos_hint: { 'center_x' :0.1,'y':0.74}
    MDTextFieldRound:
        icon_left: "magnify"
        hint_text: "Search"
        id: input
        multiline: False
        size: 100,50
        pos_hint: { 'center_x' :0.5,'y':0.57}
        size_hint:  0.85,0.05
    MDRectangleFlatButton:
        text: 'Fuck search'
        size_hint:(0.6,0.08)
        on_release: root.i_clicked(input.text)
        pos_hint: { 'center_x' :0.5,'y':0.45}

<FResults>:
    canvas:
        Color:
            rgb: 0x26 / 255.0, 0x32 / 255.0, 0x38 / 255.0

        Rectangle:
            size: self.size     
    name: 'fresults'
    ScrollView:
        size_hint: (1, 1)
        width: 390  # Button width plus BoxLayout padding
        pos_hint: {'right':1}
        BoxLayout:
            id: bl_main
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            padding: [20, 20, 20, 20]
            spacing: 10
            MDRectangleFlatButton:
                text: 'Go Back'
                on_release: root.go_back()
<SSearch>:
    name: "ssearch"
    canvas:
        Color:
            rgb: 0x26 / 255.0, 0x32 / 255.0, 0x38 / 255.0
        Rectangle:
            size: self.size  
    Image:
        source: 'img/head.jpeg'
        size: 100,50
        pos: (0,0.2)
        pos_hint: { 'center_x' :0.5,'y':0.4}
    Label:
        text: 'Welcome to HM Cinema Series section'
        font_size: 14
        pos_hint: { 'center_x' :0.5,'y':0.15}

    MDRectangleFlatButton:
        text: 'Movies'
        on_release: root.movies()
        size: 100,50
        pos_hint: { 'center_x' :0.9,'y':0.74}
    MDTextFieldRound:
        icon_left: "magnify"
        hint_text: "Search"
        id: input
        multiline: False
        size: 100,50
        pos_hint: { 'center_x' :0.5,'y':0.57}
        size_hint:  0.85,0.05
    MDRectangleFlatButton:
        text: 'Fuck search'
        size_hint:(0.6,0.08)
        on_release: root.i_clicked(input.text)
        pos_hint: { 'center_x' :0.5,'y':0.45}    
    """
class MyMainApp(MDApp):
    def build(self):
        self.root_widget= Builder.load_string(hm_cinema)
        self.theme_cls.primary_palette = "Green"  # "Purple", "Red"
        self.theme_cls.primary_hue = "200"
        self.title = 'HM Cinema'
        #self.theme_cls.theme_style="Dark"
        return self.root_widget
if __name__ == "__main__":
    MyMainApp().run()
