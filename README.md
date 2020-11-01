# PythonSwiftLink
...
...
...

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

## Generate Files:
    in Terminal:
        1. goto to the root of "PythonSwiftLink" folder
        2. type "python pythoncall_builder.py <filename.py>"
            if filename = mypythonfile.py
            then type: `python pythoncall_builder.py mypythonfile.py`

## Writing Python File:
    Pick your Class Name vicely..
    it will be the main name type for the generated files and Protocol/Struct name
    
    code:
    
    class PythonSwiftTest:
        
        @callback
        def func0(test: int_list,test2: int):
                pass

        @callback
        def func1(test: int_list,test2: int):
                pass

        @callback
        def func2(test: long_list,test2: int):
                pass

        @callback
        def func3(test: uint8_list,test2: float):
                pass

        def func4(test: float_list,test2: float):
                pass

        def func5(test: double_list,test2: float):
                pass

        def func6(test: str,test2: float):
                pass
