import kivy
kivy.require('1.9.0')
 
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader,Sound
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.switch import Switch 
from kivy.clock import mainthread
from kivy.properties import ObjectProperty, StringProperty

import utils
import threading
import MySI
import numpy as np
import os.path
from os.path import dirname, join

# You can create your kv code in the Python file
Builder.load_string("""
<TestPlayerScreen>:
    BoxLayout:
        orientation:'vertical'

        BoxLayout:
            orientation: 'vertical'
            size_hint: (1, 0.1)
            Button:
                size_hint: (0.1, 1)
                text: "Back"
                on_press:
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'test_screen'

        Label:
            text: root.speaker_name + ' is speaking...'
        Button:
            text: 'Play/Stop'
            on_press:
                root.start()

<CustLabel@Label>:
    color: 1, 1, 1, 1

<SignUp>:
    orientation: 'vertical'
    size_hint: .5, .5
    auto_dismiss: False
    title: "Enrollment"
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Enter your name'
        TextInput:
            id: user_name
            text: ''
            on_text: root.update_padding(args[0])
        Button:
            size_hint: 1, 1
            text: "Done"
            on_press:
                root.save_entered_name()
                root.open_recorder()
                root.dismiss()

<IdentifyResult>:
    orientation: 'vertical'
    size_hint: .5, .5
    auto_dismiss: False
    title: "Result"
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Identified Speaker: ' + root.speaker_name
        Button:
            size_hint: 1, 1
            text: "Okay"
            on_press:
                root.back_to_recorder()
                root.dismiss()

<EnrollResult>:
    orientation: 'vertical'
    size_hint: .5, .5
    auto_dismiss: False
    title: "Result"
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Welcome ' + root.enrolled_speaker
        Button:
            size_hint: 1, 1
            text: "Done"
            on_press:
                root.back_to_main_screen()
                root.dismiss()

<ListSpeakers>:
    orientation: 'vertical'
    size_hint: .5, .5
    auto_dismiss: False
    title: "List of speakers"
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: root.list_speakers_string
        Button:
            size_hint: 1, 1
            text: "Done"
            on_press:
                root.back_to_main_screen()
                root.dismiss()

<EnrollRecorder>
    orientation: 'vertical'
    Label:
        id: display_label
        text: '00:00'
    BoxLayout:
        orientation: 'horizontal'
        size_hint: 1, 0.2
        BoxLayout:
            size_hint: 0.5, 1
            TextInput:
                id: user_input
                text: '5'
                disabled: duration_switch.active == False
                on_text: root.enforce_numeric()
              
        BoxLayout:
            size_hint: 0.5, 1
            CustLabel:
                text: "Countdown"
            Switch:
                id: duration_switch
                active: True
                        
    BoxLayout:
        Button:
            id: start_button
            text: 'Start Recording'
            on_release: root.startRecording_clock()
  
        Button:
            id: stop_button
            text: 'Stop Recording'
            on_release: root.stopRecording()
            disabled: True


<IdentifyRecorder>
    orientation: 'vertical'
    Label:
        id: display_label
        text: '00:00'
                        
    BoxLayout:
        Button:
            id: start_button
            text: 'Start Recording'
            on_release: root.startRecording_clock()


<MainScreen>:
    BoxLayout:
        orientation: 'vertical'
        size: (50, 100)


        BoxLayout:
            orientation: 'vertical'
            size_hint: (1, 1)

            Button:
                size_hint: (1, 1)
                text: "Enroll"
                on_press:
                    root.open_sign_up()
            Button:
                text: "Identify"
                on_press:
                    # You can define the duration of the change
                    # and the direction of the slide
                    root.manager.transition.direction = 'left'
                    root.manager.transition.duration = 1
                    root.manager.current = 'identify_record_screen'

            Button:
                text: "Test"
                on_press:
                    # You can define the duration of the change
                    # and the direction of the slide
                    root.manager.transition.direction = 'left'
                    root.manager.transition.duration = 1
                    root.manager.current = 'test_screen'

            Button:
                size_hint: (1, 1)
                text: "List of speakers"
                on_press:
                    root.open_list_speakers()
 
<IdentifyRecordScreen>:
    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'vertical'
            size_hint: (1, 0.1)
            Button:
                size_hint: (0.1, 1)
                text: "Back"
                on_press:
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'main_screen'

        IdentifyRecorder:
            size_hint: (1, 0.9)

<EnrollRecordScreen>:
    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'vertical'
            size_hint: (1, 0.1)
            Button:
                size_hint: (0.1, 1)
                text: "Back"
                on_press:
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'main_screen'

        EnrollRecorder:
            size_hint: (1, 0.9)


<EnrollScreen>:
    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'vertical'
            size_hint: (1, 0.1)
            Button:
                size_hint: (0.1, 1)
                text: "Back"
                on_press:
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'main_screen'

        BoxLayout:
            size_hint: (1, 0.9)

<IdentifyScreen>:
    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'vertical'
            size_hint: (1, 0.1)
            Button:
                size_hint: (0.1, 1)
                text: "Back"
                on_press:
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'main_screen'

        BoxLayout:
            size_hint: (1, 0.9)

<TestScreen>:
    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'vertical'
            size_hint: (1, 0.1)
            Button:
                size_hint: (0.1, 1)
                text: "Back"
                on_press:
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'main_screen'

        BoxLayout:
            size_hint: (1, 0.4)

        BoxLayout:
            size_hint: (1, 0.1)
            Button:
                size_hint: 1, 1
                text: 'Start Testing.'
                on_press:
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'test_player_screen'                

        BoxLayout:
            size_hint: (1, 0.4)
""")
 
# Create a class for all screens in which you can include
# helpful methods specific to that screen
class MainScreen(Screen):
    def open_sign_up(self):
        sign_up = SignUp()
        sign_up.open()

    def open_list_speakers(self):
        list_speakers = ListSpeakers()
        list_speakers.open()

class TestPlayerScreen(Screen):
    speaker_name = StringProperty()

    def __init__(self, *args, **kwargs):
        super(TestPlayerScreen, self).__init__(*args, **kwargs)
        self.list_test_speaker = ['hung', 'quy']
        self.num_test = 5
        random_index = np.random.randint(len(self.list_test_speaker))
        self.speaker_name = self.list_test_speaker[random_index]

    def start(self):
        audio_index = np.random.randint(self.num_test) + 1
        curdir = dirname(os.path.abspath(__file__))
        audio_path = join(curdir, 'dataset', 'test', self.speaker_name + str(audio_index) + '.wav')
        self.Player = SoundLoader.load(audio_path)
        self.audio_thread = threading.Thread(target=self.plays, args=())
        self.test_thread = threading.Thread(target=MySI.testAudio, args=(audio_path,))
        self.result_thread = threading.Thread(target=self.display_result, args=())
        self.audio_thread.start()
        self.test_thread.start()
        self.result_thread.start()

    def plays(self):
        if self.Player.state == 'stop':
            self.Player.play()
        else:
            self.Player.stop()

    def display_result(self): 
        while True:
            if not self.test_thread.isAlive():
                IdentifyResult(MySI.identified_speaker).open()
                break

class EnrollScreen(Screen):
    pass

class IdentifyScreen(Screen):
    pass

class TestScreen(Screen):
    pass 

class IdentifyRecordScreen(Screen):
    pass

class EnrollRecordScreen(Screen):
    pass

class SignUp(Popup):
    def save_entered_name(self):
        global entered_name
        entered_name = self.ids['user_name'].text

    def update_padding(self, text_input, *args):
        text_width = text_input._get_text_width(
            text_input.text,
            text_input.tab_width,
            text_input._label_cached
        )
        text_input.padding_x = (text_input.width - text_width)/2

    def open_recorder(self):
        main_screen.manager.transition.direction = 'left'
        main_screen.manager.transition.duration = 1
        main_screen.manager.current = 'enroll_record_screen'


class IdentifyResult(Popup):
    speaker_name = StringProperty()

    def __init__(self, speaker_name, **kwargs):
        super(IdentifyResult, self).__init__(**kwargs)
        self.speaker_name = speaker_name

    def back_to_recorder(self):
        main_screen.manager.current = 'main_screen'

class EnrollResult(Popup):
    enrolled_speaker = StringProperty()
    def __init__(self, enrolled_speaker, **kwargs):
        super(EnrollResult, self).__init__(**kwargs)
        self.enrolled_speaker = enrolled_speaker

    def back_to_main_screen(self):
        main_screen.manager.current = 'main_screen'

class ListSpeakers(Popup):
    list_speakers_string = StringProperty()
    def __init__(self, **kwargs):
        super(ListSpeakers, self).__init__(**kwargs)
        list_speakers = MySI.load_speaker().keys()
        list_speakers_string = ''
        for speaker_name in list_speakers:
            list_speakers_string = list_speakers_string + speaker_name + '\n'
        self.list_speakers_string = list_speakers_string

    def back_to_main_screen(self):
        main_screen.manager.current = 'main_screen'

class DeleteSpeaker(Popup):
    def save_entered_name(self):
        global entered_name
        entered_name = self.ids['user_name'].text

    def update_padding(self, text_input, *args):
        text_width = text_input._get_text_width(
            text_input.text,
            text_input.tab_width,
            text_input._label_cached
        )
        text_input.padding_x = (text_input.width - text_width)/2

    def open_recorder(self):
        main_screen.manager.transition.direction = 'left'
        main_screen.manager.transition.duration = 1
        main_screen.manager.current = 'enroll_record_screen'

# source:
class AudioTool(BoxLayout):
    def __init__(self, **kwargs):
        super(AudioTool, self).__init__(**kwargs)
        Clock.schedule_once(self._finish_init)
       
    # this fixes the KeyError of ids
    def _finish_init(self, dt):
        self.start_button = self.ids['start_button']
        self.stop_button = self.ids['stop_button']
        self.display_label = self.ids['display_label']
        self.switch = self.ids['duration_switch'] # Tutorial 3
        self.user_input = self.ids['user_input']
           
 
    def enforce_numeric(self):
        '''Make sure the textinput only accepts numbers'''
        if self.user_input.text.isdigit() == False:
            digit_list = [num for num in self.user_input.text if num.isdigit()]
            self.user_input.text = "".join(digit_list)
 
    def startRecording_clock(self):
        self.mins = 0 #Reset the minutes
        self.zero = 1 # Reset if the function gets called more than once
        self.duration = int(self.user_input.text) #Take the input from the user and convert to a number
        threading.Thread(target=Clock.schedule_interval, args=(self.updateDisplay, 1, )).start()
        self.start_button.disabled = True # Prevents the user from clicking start again which may crash the program
        self.stop_button.disabled = False
        self.switch.disabled = True #TUT Switch disabled when start is pressed
       
    def stopRecording(self):
   
        Clock.unschedule(self.updateDisplay)
        self.display_label.text = 'Finished Recording!'
        self.start_button.disabled = False
        self.stop_button.disabled = True #TUT 3
        self.switch.disabled = False #TUT 3 re enable the switch
         
    def updateDisplay(self,dt):  
        if self.switch.active == False:
            if self.zero < 60 and len(str(self.zero)) == 1:
                self.display_label.text = '0' + str(self.mins) + ':0' + str(self.zero)
                self.zero += 1
               
            elif self.zero < 60 and len(str(self.zero)) == 2:
                    self.display_label.text = '0' + str(self.mins) + ':' + str(self.zero)
                    self.zero += 1
           
            elif self.zero == 60:
                self.mins +=1
                self.display_label.text = '0' + str(self.mins) + ':00'
                self.zero = 1
       
        elif self.switch.active == True:
            if self.duration == 0: # 0
                self.display_label.text = 'Recording Finished!'
                self.start_button.disabled = False # Re enable start
                self.stop_button.disabled = True # Re disable stop
                Clock.unschedule(self.updateDisplay)
                self.switch.disabled = False # Re enable the switch
               
            elif self.duration > 0 and len(str(self.duration)) == 1: # 0-9
                self.display_label.text = '00' + ':0' + str(self.duration)
                self.duration -= 1
 
            elif self.duration > 0 and self.duration < 60 and len(str(self.duration)) == 2: # 0-59
                self.display_label.text = '00' + ':' + str(self.duration)
                self.duration -= 1
 
            elif self.duration >= 60 and len(str(self.duration % 60)) == 1: # EG 01:07
                self.mins = self.duration / 60
                self.display_label.text = '0' + str(self.mins) + ':0' + str(self.duration % 60)
                self.duration -= 1
 
            elif self.duration >= 60 and len(str(self.duration % 60)) == 2: # EG 01:17
                self.mins = self.duration / 60
                self.display_label.text = '0' + str(self.mins) + ':' + str(self.duration % 60)
                self.duration -= 1

class EnrollRecorder(AudioTool):
    def __init__(self, **kwargs):
        super(AudioTool, self).__init__(**kwargs)
        Clock.schedule_once(self._finish_init)
        self.enroll_thread = None
        self.result_thread = None

    def startRecording_clock(self):
        global entered_name
        super(EnrollRecorder, self).startRecording_clock()
        self.speaker_name = entered_name
        self.enroll_thread = threading.Thread(target=MySI.enrollName, args=(self.speaker_name, self.duration,))
        self.result_thread = threading.Thread(target=self.display_result, args=())
        self.enroll_thread.start()
        self.result_thread.start()

    def display_result(self): 
        while True:
            if not self.enroll_thread.isAlive():
                EnrollResult(enrolled_speaker=self.speaker_name).open()
                break

    

class IdentifyRecorder(AudioTool):
    def __init__(self, **kwargs):
        super(AudioTool, self).__init__(**kwargs)
        Clock.schedule_once(self._finish_init)
        self.identify_thread = threading.Thread(target=MySI.identify, args=())
        self.result_thread = threading.Thread(target=self.display_result, args=())
       
    def _finish_init(self, dt):
        self.start_button = self.ids['start_button']
        self.stop_button = Button()
        self.display_label = self.ids['display_label']
        self.switch = Switch()
        self.user_input = TextInput(text='0')

    def startRecording_clock(self):
        super(IdentifyRecorder, self).startRecording_clock()
        self.duration = 10 # default is 10s-recording
        self.switch.active = True
        self.identify_thread.start()
        self.result_thread.start()

    def display_result(self): 
        while True:
            if not self.identify_thread.isAlive():
                IdentifyResult(speaker_name=MySI.identified_speaker).open()
                break


# global variable to store entered name
entered_name = "Unknown"

# The ScreenManager controls moving between screens
screen_manager = ScreenManager()
 
# Add the screens to the manager and then supply a name
# that is used to switch screens
main_screen = MainScreen(name="main_screen")
screen_manager.add_widget(main_screen)
screen_manager.add_widget(TestPlayerScreen(name='test_player_screen'))
screen_manager.add_widget(EnrollScreen(name="enroll_screen"))
screen_manager.add_widget(IdentifyScreen(name="identify_screen"))
screen_manager.add_widget(TestScreen(name="test_screen"))
screen_manager.add_widget(IdentifyRecordScreen(name='identify_record_screen'))
screen_manager.add_widget(EnrollRecordScreen(name='enroll_record_screen'))

class SpeakerIdentification(App):
    def build(self):
        return screen_manager

sample_app = SpeakerIdentification()
sample_app.run()























# <AudioTool>
#     orientation: 'vertical'
#     Label:
#         id: display_label
#         text: '00:00'
#     BoxLayout:
#         orientation: 'horizontal'
#         size_hint: 1, 0.2
#         BoxLayout:
#             size_hint: 0.5, 1
#             TextInput:
#                 id: user_input
#                 text: '5'
#                 disabled: duration_switch.active == False #TUT 3 IF SWITCH IS OFF TEXTINPUT IS DISABLED
#                 on_text: root.enforce_numeric()
              
#         BoxLayout:
#             size_hint: 0.5, 1
#             CustLabel:
#                 text: "Countdown"
#             Switch:
#                 id: duration_switch
                        
#     BoxLayout:
#         Button:
#             id: start_button
#             text: 'Start Recording'
#             on_release: root.startRecording_clock()
  
#         Button:
#             id: stop_button
#             text: 'Stop Recording'
#             on_release: root.stopRecording()
#             disabled: True