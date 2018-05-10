from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader,Sound
from kivy.lang import Builder
Builder.load_string('''
<MenuPage>:
    BoxLayout:
        orientation:'vertical'
        Button:
            text:'song'
            on_press:root.plays()
''')

class MenuPage(Screen):
    M = SoundLoader.load('C:/Users/lengo/Desktop/Speaker Identification/dataset/enroll/khang.wav')

    def plays(self):
        if MenuPage.M.state == 'stop':
            MenuPage.M.play()
        else:
            MenuPage.M.stop()


sm = ScreenManager()
menu = MenuPage(name='menu')
sm.add_widget(menu)


class TestApp(App):
    def build(self):
        return sm




TestApp().run()