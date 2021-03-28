# PythonSwiftLink

 ## Installation

PythonSwiftLink requires [Kivy](https://kivy.org) (the GUI), [Cython](https://cython.readthedocs.io/en/latest/src/tutorial/cython_tutorial.html) and [Kivy-ios](https://github.com/kivy/kivy-ios) to run.

Install the dependencies and devDependencies and start the server.

```sh
mkdir kivyios_swift
cd kivyios_swift
```
```sh
python3 -m venv venv
. venv/bin/activate
```
```sh
pip install kivy
pip install kivy-ios
```

For production environments...

```sh
npm install --production
NODE_ENV=production node app
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
### Swift File:
```swift
class PythonMain : NSObject,KivyTestDelegate {
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
        InitKivyTestDelegate(self)
    }

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

