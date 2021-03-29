# PythonSwiftLink

 ## Installation

PythonSwiftLink requires [Kivy](https://kivy.org)(the GUI), [Cython](https://cython.readthedocs.io/en/latest/src/tutorial/cython_tutorial.html) and [Kivy-ios](https://github.com/kivy/kivy-ios) to run.

Create the root folder for the whole build: 
```sh
mkdir kivyios_swift
cd kivyios_swift
```
create a virtual env and activate it.
```sh
python3 -m venv venv
. venv/bin/activate
```

install kivy and kivy-ios
```sh
pip install kivy
pip install kivy-ios
```
build kivy in the toolchain
```sh
toolchain build kivy
```
install PythonSwiftLink
```sh
git clone https://github.com/psychowasp/PythonSwiftLink
```

## Writing first Python wrapper file:
    Pick your Class Name vicely..
    it will be the main name type for the generated files and Protocol/Struct name
in kivyios_swift/PythonSwiftLink/imported_pys/ 

create a new file called "kivytest.py"
insert the following code
 ### Code: 
```python
from swift_types import *

class KivyTest:

    # array/list of int
    @callback
    def get_swift_array(l: List[int]):
        pass

    @callback
    def get_swift_string(s: str):
        pass


    # array/list of int
    def send_python_list(l: List[int]):
        pass

    def send_python_string(s: str):
        pass
```          

## Launch the wrapper gui
From the root folder "kivyios_swift/"
run:
```sh
python3 main.py
```
![gui_app0](https://user-images.githubusercontent.com/2526171/112910616-02e64f00-90f4-11eb-8abe-0af156a55f9a.png)
![gui_app1](https://user-images.githubusercontent.com/2526171/112910962-b2bbbc80-90f4-11eb-8a0a-20a7d3b23f86.png)
![gui_app2](https://user-images.githubusercontent.com/2526171/112911028-d8e15c80-90f4-11eb-9a47-138cf0a7e462.png)
![gui_app3](https://user-images.githubusercontent.com/2526171/112911111-0c23eb80-90f5-11eb-857b-80ae4365a74e.png)

# Xcode Project Setup

add the 2 following files
runMain.h
runMain.c
to the Classes group from the PythonSwiftLink folder

![Skærmbillede 2021-03-29 kl  01 53 14](https://user-images.githubusercontent.com/2526171/112772531-aa4e7d80-9031-11eb-9812-2db1bcc9145b.png)

they are basicly just a copy of the original main.m
but we need to replace the main.h
so we can execute/setup swift classes before python/kivy gets executed

also disable or delete the "main.m" file



Create a new group(without folder)

![New Group](https://user-images.githubusercontent.com/2526171/112898609-54d1a980-90e1-11eb-85e7-f08181ce4716.png)

name it "Headers" for now.

![Headers](https://user-images.githubusercontent.com/2526171/112898805-995d4500-90e1-11eb-85c1-2971c43c04de.png)

### Swift File:
```swift
//PythonMain.swift
class PythonMain : NSObject {
    
    var callback: KivyTestCallback?
    
    static var shared: PythonMain?
    
    class func sharedInstance() -> PythonMain {
        if shared == nil {
            shared = PythonMain()
        }
        return shared!
    }
    
    override init() {
        super.init()
        
    }
}
```

```swift
extension PythonMain : KivyTestDelegate {
    
}
```

![protocol error](https://user-images.githubusercontent.com/2526171/112770707-41163c80-9028-11eb-9582-ca6666b7763b.png)

![protocol auto fix](https://user-images.githubusercontent.com/2526171/112770747-70c54480-9028-11eb-8fc4-08f825f49d25.png)

![protocol fixed](https://user-images.githubusercontent.com/2526171/112770891-39a36300-9029-11eb-8155-4850723c7422.png)

replace ```code``` in func ```set_KivyTest_Callback```
with the following:
```swift
self.callback = callback
```

replace ```code``` in func ```send_python_list```
with the following:
```swift
let array = pointer2array(data: list1, count: list1_size)
print("python list: ", array)

callback!.get_swift_array(array.reversed(), array.count)
```
replace ```code``` in func ```send_python_string```
with the following:
```swift
print(String.init(cString: string))
        
let swift_string = "Hallo from swift !!!!"
callback!.get_swift_string(swift_string)
```
![Final Extension](https://user-images.githubusercontent.com/2526171/112771360-ba635e80-902b-11eb-9f89-d5994d3ba2ef.png)

of course we got no function yet called "pointer2array" to convert a c pointer to an array.
so lets add that:

![Skærmbillede 2021-03-29 kl  01 17 55](https://user-images.githubusercontent.com/2526171/112771532-9d7b5b00-902c-11eb-8b13-3009cdba3a20.png)
```swift
// this function is using generic type, so it should cover most of the pointer array types from c/python
func pointer2array<T>(data: UnsafePointer<T>,count: Int) -> [T] {

    let buffer = UnsafeBufferPointer(start: data, count: count);
    return Array<T>(buffer)
}
```
![run main class](https://user-images.githubusercontent.com/2526171/112787149-370c3200-9058-11eb-80e0-887c741c6f5e.png)

# Python File

## main.py
```python
#main.py

from kivytest_cy import KivyTest


class KivyTestCallback:

    # array/list of int
    def get_swift_array(self, list1: [int]):
        print("swift_array",list1)
    # array/list of int

    def get_swift_string(self, string: str):
        print(string)


callback = KivyTestCallback()

kivy_test = KivyTest(callback)

kivy_test.send_python_list([5,4,3,2,1])

kivy_test.send_python_string("Hallo from python and kivy")
```

![xcode running](https://user-images.githubusercontent.com/2526171/112787816-bc441680-9059-11eb-8572-c3b28d33b908.png)




### Arg Types:

| Python        | Objective-C   |             Swift            |
| ------------- |:--------------|:-----------------------------|
| bytes         | const char*   | UnsafeMutablePointer\<Int8\> |
| str           | const char*   | UnsafeMutablePointer\<Int8\> |
| int           | int           |   Int32                      |
| long          | long          |   Int                        |
| float         | float         |   Float                      |
| double        | double        |   Double                     |

### Special list types:
| Python            | Objective-C          |             Swift               |
|:------------------|:---------------------|:--------------------------------|
| List[int]         | const int*           |   UnsafeMutablePointer\<Int32\> |
| List[long]        | const long*          |   UnsafeMutablePointer\<Int\>   |
|List[uint]         | const unsigned int*  |   UnsafeMutablePointer\<UInt32\>  |
|List[ulong]        | const unsigned long* |   UnsafeMutablePointer\<UInt\>  |
| List[float]       | const float*         |   UnsafeMutablePointer\<Float\> |
| List[double]      | const double*        |  UnsafeMutablePointer\<Double\> |

