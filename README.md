# PythonSwiftLink

 ## Installation

PythonSwiftLink requires [Kivy](https://kivy.org) (the GUI), [Cython](https://cython.readthedocs.io/en/latest/src/tutorial/cython_tutorial.html) and [Kivy-ios](https://github.com/kivy/kivy-ios) to run.

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



## Writing Python File:
    Pick your Class Name vicely..
    it will be the main name type for the generated files and Protocol/Struct name
    
![image](https://user-images.githubusercontent.com/2526171/112758247-96812800-8fed-11eb-8523-fc4e6c3dff86.png)
 ### Code:
    
```python
class KivyTest:

    @callback
    # array/list of int
    def get_swift_array(list1: [int]):
        pass
        
    # array/list of int
    def send_python_list(list1: [int]):
        pass

    @callback
    def get_swift_string(string: str):
        pass

    def send_python_string(string: str):
        pass
```          



# Xcode Project Setup


![New Group](https://user-images.githubusercontent.com/2526171/112771700-65c0e300-902d-11eb-9ce1-1740161fcc62.png)

add the 2 following files
runMain.h
runMain.c
to the Classes group from the PythonSwiftLink folder

![Skærmbillede 2021-03-29 kl  01 53 14](https://user-images.githubusercontent.com/2526171/112772531-aa4e7d80-9031-11eb-9812-2db1bcc9145b.png)

they are basicly just a copy of the original main.m
but we need to replace the main.h
so we can execute/setup swift classes before python/kivy gets executed

also disable or delete the "main.m" file

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





## Arg Types:
### Special list types:
        int_list = const int*
        float_list = const float*
        double_list = const double*
        long_list = const long*
        uint8_list = const unsigned char*

    str = const char*

    float = float
    double = double
    long = long (int64)
    int = int32

