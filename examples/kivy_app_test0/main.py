import kivy
kivy.require('1.0.7')

from kivy.app import App
from kivy.uix.button import Button
from osclivecallback2_cy import OSCLiveCallback2
import LiveOscLib

class TestApp(App):

    def build(self):
        self.osclive = OSCLiveCallback2(self)
        # return a Button() as a root widget
        self.btn = Button(text='press me')
        self.btn.bind(on_release=self.send_2_swift)
        self.btn.bind(on_press=self.init_btn_text)
        return self.btn

    def init_btn_text(self,wid):
        wid.text = "Im Pressed"

    def send_2_swift(self,wid):
        wid.text = self.osclive.update_btn()

    def update_btn(self,string):
        self.btn.text = string

if __name__ == '__main__':
    TestApp().run()
