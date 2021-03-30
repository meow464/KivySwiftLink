# Kivy App

```python
#main.py
from typing import List
from kivytest import KivyTest
import json

from kivy.app import App
from kivy.uix.label import Label
from kivy.lang import Builder

kv = """
GridLayout:
    rows: 2
    cols: 2
    Label:
        id: label0
    Button:
        id: btn0
        text: "get_swift_string"
        on_press:
            label0.text = ""
        on_release:
            app.kivytest.send_python_string("Hallo from python and kivy")
    Label:
        id: label1
    Button:
        id: btn1
        text: "get_swift_array"
        on_press:
            label1.text = ""
        on_release:
            app.kivytest.send_python_list([5,4,3,2,1])

"""


class MyApp(App):

    def build(self):
        
        self.kivytest = KivyTest(self)
        wid = Builder.load_string(kv)
        self.ids = wid.ids
        return wid

    def get_swift_array(self, l: List[int]):
        self.ids.label1.text = str(l)

    def get_swift_string(self, string: str):
        self.ids.label0.text = string

if __name__ == '__main__':
    MyApp().run()
```

Here is a basic Kivy App class with 2 labels and 2 buttons.

The same 2 callback functions from previous example are now instead inserted into the App class instead, and the callback is now set as the App instead by using the Apps self.

The wrapper class (KivyTest) callback can use any python class, as long it has the same functions and parameters. We promised cython that the called python object will have the 2 functions named:

​	get_swift_array(self, list)

​	get_swift_string(self,str)

so as long the callback class has the same function names as the wrapper file functions that was with marked @callback, then any class can be used as callback.

Same goes for the Swift side, as long the swift class you are extentending with your Wrappers function, has NSObject as base class then you can easy add the functions by just using 

```swift
extension SwiftClass: PythonDelegate{
    
}
```

if the class you are using doesn't conform to NSObject

then you basicly have to make a Swift class like previous and then add the non NSObejct class as a var / wrap the functions inside that and then add the extension to that class

and last call those from the functions that is triggered from python.

More about this in a later example.

Next example we look into how to access the Apple API and wrap functions to launch the following:

- ios native "Files "app, to access files
- ios native PDF Reader
- ios native Web Page Viewer

[Using Apple API part 1](https://github.com/psychowasp/PythonSwiftLink/tree/main/examples/2%20Using%20Apple%20API%20part%201)