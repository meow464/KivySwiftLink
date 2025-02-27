from functools import wraps
import parser
import ast
from ast import *
from uuid import uuid4
from time import time
import astor
from pprint import pprint
import re
import sys
import os
import subprocess
from PythonSwiftLink.build_files.pack_files import pack_all,remove_cache_file
import configparser
import json
from os.path import join
import shutil
import random
import string

from typing import List

from PythonSwiftLink.def_types import types2dict



print(os.path.basename(sys.argv[0]))
print(os.path.dirname(sys.argv[0]))
root_path = os.path.dirname(sys.argv[0])

#cstruct_list: list

#calltitle = None 


# ctypedef_types_dict = {
#     "str": "const char*",
#     "int": "int",
#     "float": "float",
#     "long": "long",
#     "object": "const void*",
#     "json": "const char*",
#     "jsondata": "const unsigned char*",
#     "bytes": "const char*",
#     "short": "short",

#     "data": "const unsigned char*",

#     "uint8": "unsigned char",

#     "bool": "bool_t",

#     "PythonCallback": "PythonCallback"
# }
ctypedef_types_dict = types2dict("cython")
print("\n\n\n\tctypedef_types_dict:\n")
pprint(ctypedef_types_dict)
ctypedef_list_dict = types2dict("cython", True)
print("\n\n\n\tctypedef_list_dict:\n")
pprint(ctypedef_list_dict)
# ctypedef_list_dict = {
#     "int": "const int*",
#     "long": "const long*",
#     "uint8": "const unsigned char*",
#     "float": "const float*",
#     "double": "const double*",
#     "str": "const char* const*",
#     "short": "const short*"
    
# }
typedef_types_dict = types2dict("objc")
print("\n\n\n\ttypedef_types_dict:\n")
pprint(typedef_types_dict)
# typedef_types_dict = {

#     "str": "const char* _Nonnull",
#     "int": "int",
#     "float": "float",
#     "long": "long",
#     "object": "const void* _Nonnull",
#     "json": "const char* _Nonnull",
#     "jsondata": "const unsigned char* _Nonnull",
#     "bytes": "const char*  _Nonnull",
#     "data": "const unsigned char* _Nonnull",
#     "short": "short",
#     "bool": "BOOL",

#     "uint8": "unsigned char",

#     "PythonCallback": "PythonCallback"
# }

typedef_list_dict = types2dict("objc", True, True)
print("\n\n\n\ttypedef_list_dict:\n")
pprint(typedef_list_dict)

# typedef_list_dict = {
#     "int": "const int* _Nonnull",
#     "long": "const long* _Nonnull",
#     "uint8": "const unsigned char* _Nonnull",
#     "float": "const float* _Nonnull",
#     "double": "const double* _Nonnull",
#     "str": "const char* _Nonnull const* _Nonnull",
#     "short": "const short*  _Nonnull"
# }
python_types_dict = types2dict("python")
print("\n\n\n\tpython_types_dict:\n")
pprint(python_types_dict)
# python_types_dict = {

#     "str": "str",
#     "int": "int",
#     "float": "float",
#     "long": "int",
#     "uint8": "int",
#     "uint16": "int",
#     "object": "object",
#     "json" : "object",
#     "jsondata": "object",
#     "bytes": "bytes",
#     "data": "bytes",
#     "short": "int",

#     "PythonCallback": "PythonCallback"
# }

send_args_dict = types2dict("send_arg")
print("\n\n\n\tsend_args_dict:\n")
pprint(send_args_dict)
# send_args_dict = {
#     "str": "{arg}.encode('utf-8')",
#     "int": "{arg}",
#     "float": "{arg}",
#     "long": "{arg}",
#     "object": "<const void*>{arg}",
#     "json": "json.dumps({arg}).encode('utf-8')",
#     "jsondata": "json.dumps({arg}).encode('utf-8')",
#     "bytes": "{arg}",

#     "PythonCallback": "{arg}",
#     "": "{arg}"
# }
call_args_dict = types2dict("call_arg")
print("\n\n\n\tcall_args_dict:\n")
pprint(call_args_dict)
# call_args_dict = {
#     "str": "{arg}.decode('utf8')",
#     "int": "{arg}",
#     "float": "{arg}",
#     "long": "{arg}",
#     "object": "<object>{arg}",
#     "json": "json.loads({arg})",
#     "jsondata": "json.loads({arg}[:{arg}_size])",
#     "bytes": "{arg}",
#     "data": "<bytes>{arg}[0:{arg}_size]",

#     "PythonCallback": "PythonCallback"
# }

call_list_dict = types2dict("list_call_arg")
print("\n\n\n\tcall_list_dict:\n")
pprint(call_list_dict)

# call_list_dict = {
#     "int": "[{arg}[x] for x in range({arg}_size)]",
#     "long": "[{arg}[x] for x in range({arg}_size)]",
#     "uint8": "{arg}[:{arg}_size]",
#     "bytes": "{arg}",
#     "data": "{arg}[:{arg}_size]",
#     "float": "[{arg}[x] for x in range({arg}_size)]",
#     "double": "[{arg}[x] for x in range({arg}_size)]",
#     "str": "[{arg}[x].decode('utf8') for x in range({arg}_size)]",
#     "PythonCallback": "PythonCallback"
# }

arg_size_dict = types2dict("size")
print("\n\n\n\targ_size_dict:\n")
pprint(arg_size_dict)
# arg_size_dict = {
#         "str": 1,
#         "data": 1,
#         "uint8": 1,
#         "int": 4,
#         "float": 4,
#         "long": 8,
#         "double": 8,
#         "short": 2,
#     }
ptr_type_dict = types2dict("cython")
print("\n\n\n\tptr_type_dict:\n")
pprint(ptr_type_dict)
# ptr_type_dict = {
#         "str": "const char*",
#         "int": "long",
#         "float": "float",
#         "long": "long",
#         "double": "double",
#         "uint8": "unsigned char",
#         "short": "short",
        
#     }


func_pointer_string = """\
ctypedef void (*{title})({args})
"""

func_pointer_string2 = """\
ctypedef {returns} (*{title})({args})
"""

objc_func_pointer_string = """\
typedef void (*{title})({args});
"""

objc_func_pointer_string2 = """\
typedef {returns} (*{title})({args});
"""


#def get_cython_class_string(_class_, call_var, )

cython_class = """\
cdef public void* {_class}_voidptr
cdef class {_class}:

\t@staticmethod
\tdef default(call: object):
\t\tglobal {_class}_shared
\t\tif {_class}_shared != None:
\t\t\treturn {_class}_shared
\t\telse:
\t\t\t{_class}_shared = {_class}(call)
\t\t\treturn {_class}_shared

\tdef __init__(self,object callback_class):
\t\tglobal {call_var}
\t\t{call_var} = <const void*>callback_class
\t\tprint("{call_var} init:", (<object>{call_var}))
"""

cython_class_dispatch = """\
cdef public void* {_class}_voidptr
cdef public void* {_class}_dispatch
cdef public {_class} {_class}_shared
cdef class {_class}(EventDispatcher):
\t__events__ = {events}

\t@staticmethod
\tdef default(call: object):
\t\tglobal {_class}_shared
\t\tif {_class}_shared != None:
\t\t\treturn {_class}_shared
\t\telse:
\t\t\t{_class}_shared = {_class}(call)
\t\t\treturn {_class}_shared

\tdef __init__(self,object callback_class):
\t\tglobal {call_var}
\t\tglobal {_class}_dispatch
\t\t{_class}_dispatch = <const void*>self.dispatch
\t\t{call_var} = <const void*>callback_class
\t\tprint("{call_var} init:", (<object>{call_var}))
"""


ext_cyfunc = "\t{returns} {title}({args})"

class_cyfunc_send = """\
\tdef {title}(self,{args}):
\t\tpass
"""
class_cyfunc_send_rtn = """\
\tdef {title}(self,{args}) -> {rtn_arg}:
{body}
\t\t{call}
"""

class_cyfunc_send_rtn_noargs = """\
\tdef {title}(self):
{body}
\t\t{call}
"""

class_cyfunc_send_plain = """\
\tdef {title}(self,{args}):
{body}
\t\t{call}
"""


global_event_function = """\
\tdef {title}(self,*largs,**kwargs):
\t\tpass
"""


call_args_dict2 = {
    "str": "{arg}.decode('utf8')",
    "int": "{arg}",
    "float": "{arg}",
    "long": "{arg}",

    "PythonCallback": "PythonCallback"
}





list_2_array =  """\
\t\tcdef int {arg}_size = len({arg})
\t\tcdef {arg_type} *{arg}_array = <{arg_type} *> malloc({arg}_size  * {type_size})
\t\tcdef int {arg}_i
\t\tfor {arg}_i in range({arg}_size):
\t\t\t{arg}_array[{arg}_i] = {decode}{arg}[{arg}_i]
"""
strlist_2_array =  """\
\t\t{arg}_bytes = [x.encode('utf-8') for x in {arg}]
\t\tcdef int {arg}_size = len({arg})
\t\tcdef {arg_type} *{arg}_array = <{arg_type} *> malloc({arg}_size  * {type_size})
\t\tcdef int {arg}_i
\t\tfor {arg}_i in range({arg}_size):
\t\t\t{arg}_array[{arg}_i] = {decode}{arg}_bytes[{arg}_i]
"""

ext_objcfunc_m = """\
{returns} {title}({args}){{
    [{subtitle} {call}:{args2}];
}}
"""

ext_objcfunc_m_rtn = """\
{returns} {title}({args}){{
    return [{subtitle} {call}:{args2}];
}}
"""

ext_objcfunc_m_noarg = """\
{returns} {title}({args}){{
    [{subtitle} {call}];
}}
"""

ext_objcfunc_m_rtn_noarg = """\
{returns} {title}({args}){{
    return [{subtitle} {call}];
}}
"""

ext_objcfunc_h = """\
{returns} {title}({args});
"""

ext_send_callback = """\
{returns} Init{title}Delegate(id<{title_l}Delegate> _Nonnull callback){{
    {subtitle} = callback;
    NSLog(@"setting {title} delegate %@",{subtitle});
}}
"""
ext_send_callback_h = """\
{returns} Init{title}Delegate(id<{title_l}Delegate> _Nonnull callback);
"""

objc_arg_first = "({t}){arg}"
objc_arg = "{arg}:({t}){arg}"




cython_callback = """\
cdef void {_class}_{title}({args}) with gil:
\t(<object> {call_class}).{title}{callback}

"""
cython_callback2 = """\
cdef {returns} {_class}_{title}({args}) with gil:
\t(<object> {call_class}).{call}{callback}

"""

cython_global_dispatch = """\
cdef {returns} {_class}_{title}({args}) with gil:
\t{call_class}{callback}
"""

cython_callback3 = """\
cdef {returns} {_class}_{title}({args}) with gil:
\t{code}
\t(<object> {call_class}).{call}{callback}

"""

objc_structinit_string = """\
typedef struct {title}Struct {call};

"""

c_structinit_string = """\
\tctypedef {title}Struct {call}

"""

protocol_start = "@protocol {title}Delegate <NSObject>"
protocol_line_start = "- ({returns}){title}:{args};"
protocol_line_noarg = "- ({returns}){title};"
protocol_arg = "{arg}:({type}){arg}"
protocol_first_arg = "({type}){arg}"
protocol_id = "typedef id<{title}Delegate> {title}Delegate;"
protocol_static = "\nstatic id<{title}Delegate> _Nonnull {subtitle};"


m_header_string = """\
#import <Foundation/Foundation.h>
#import "_{title}.h"
"""
class Arg():
    python_type: str
    python_name: str
    cy_type: str
    cy_name: str
    objc_type: str
    objc_name: str
    call_name: str
    return_name: str
    is_list: bool
    is_counter: bool
    is_json: bool
    is_data: bool
    counter_name: str
    list_type: str
    custom_call: bool
    call_code: str

    def __init__(self):
        self.python_type = ""
        self.python_name = ""
        self.cy_type = ""
        self.cy_name = ""
        self.objc_type = ""
        self.objc_name = ""
        self.call_name = ""
        self.return_name = ""
        self.is_list = False
        self.is_tuple = False
        self.is_counter = False
        self.is_json = False
        self.is_data = False
        self.custom_call = False
        self.counter_name = ""
        self.list_type = ""
        self.call_code = ""
    
    @staticmethod
    def generate_general_arg(_arg: ast.arg,_dec: str,func_arg_list: list, func,  i ):
        
        temp: Function = func
        func_arg = Arg()
        temp.args_.append(func_arg)
        func_arg.objc_name = "arg%d" % i
        func_arg.call_name = _arg.arg

        func_arg.python_name = _arg.arg
        func_arg.cy_name = _arg.arg
        
        if isinstance(_arg.annotation,(ast.List,ast.Bytes)):
            arg_type = _arg.annotation.elts[0].id
            func_arg.is_list = True
            func_arg.python_type = "list"
            func_arg.cy_type = ctypedef_list_dict[arg_type]
            func_arg.list_type = arg_type

            func_arg.objc_type = typedef_list_dict[arg_type]

            list_counter = Arg()
            temp.args_.append(list_counter)
            list_counter.is_counter = True

            list_counter.cy_type = "long"
            list_counter.cy_name = "%s_size" % _arg.arg
            list_counter.python_name = "%s_size" % _arg.arg
            list_counter.objc_type = "long"
            list_counter.objc_name = "arg%d_size" % i
        else:

            #print("not list",_arg.__dict__)
            
            # if isinstance(_arg.annotation, ast.Subscript):
            #     #print(_arg.annotation.__dict__)
            #     #print(_arg.annotation.slice.__dict__)
            #     #print(_arg.annotation.value.__dict__)
            #     arg_type = _arg.annotation.slice.value.id
            #     _arg_id = _arg.arg

            #else:
            arg_type = _arg.annotation.id
            #print("\t argtype:",arg_type)
            func_arg.is_list = False
            func_arg.python_type = python_types_dict[arg_type]
            func_arg.cy_type = ctypedef_types_dict[arg_type]

            func_arg.objc_type = typedef_types_dict[arg_type]

            #func_arg_list.append(arg_type)
            #func_arg_list.append(_arg.annotation.id)
            temp.arg_types.append(arg_type)
            #temp.arg_types.append(_arg.annotation.id)
            temp.python_args.append(python_types_dict[arg_type])
            if arg_type in ("json", "jsondata"):
                func_arg.is_json = True

            if arg_type in ("data","jsondata"):
                func_arg.is_data = True
                list_counter = Arg()
                temp.args_.append(list_counter)
                list_counter.is_counter = True

                list_counter.cy_type = "long"
                list_counter.cy_name = "%s_size" % _arg.arg
                list_counter.python_name = "%s_size" % _arg.arg
                list_counter.objc_type = "long"
                list_counter.objc_name = "arg%d_size" % i

        return (func_arg, arg_type)

#objc_arg_first = "({t}){arg}"
#objc_arg = "{arg}:({t}){arg}"

    def gen_send(self, i:int, objc=False, header=False):
        if objc:
            if header:
                return f"{self.cy_type} {self.cy_name}"
            else:
                if self.python_name is "":
                    send_arg = self.objc_name
                else:
                    send_arg = self.python_name
                if i == 0:
                    tmp_str = f"({self.objc_type}){send_arg}"
                else:
                    tmp_str = f"{send_arg}:({self.objc_type}){send_arg}"
                return tmp_str
        else:
            if header:
                return f"{self.cy_type} {self.cy_name}"
            else:
                pass


class Function():
    args_: List[Arg]
    args: List[ast.arg]
    args2: list
    arg_types: list
    arg_names: list
    extra_args: list
    real_args: list
    real_args2: list
    python_args: list
    python_arg_names: list
    call_args: list
    returns: str
    name: str
    callback: str
    func_ptr: str
    decs: list
    code: str
    call_class: str
    call_target: str
    compare_string: str
    global_dispatch: bool
    uuid: str
    wrap_class: object
    init_func: bool

    def __init__(self,main):
        self.args_ = []
        self.args = []
        self.args2 = []
        self.arg_types = []
        self.real_args = []
        self.real_args2 = []
        self.arg_names = []
        self.python_args = []
        self.python_arg_names = []
        self.call_args = []
        self.decs = []
        self.returns = None
        self.name = ""
        self.callback = ""
        self.func_ptr = ""
        self.code = ""
        self.wrap_class = main
        self.call_class = main.calltitle + "_voidptr"
        self.call_target = ""
        self.compare_string = ""
        self.global_dispatch = False
        self.uuid = self.uniqid()
        self.init_func = False
    
    def uniqid(self):
        return f"{random.choice(string.ascii_letters)}{hex(int(time()*10000000))[6:]}{random.choice(string.ascii_letters)}"

    @property
    def func_uuid(self):
        return f"func_{self.uuid}"

class WrapClass:
    calltitle: str
    func_pointers: List[Function]
    new_func_ptrs: List[Function]
    send_functions: list
    kivy_properties: list
    pointer_types: list
    enum_list: list
    dispatch_mode: bool
    cy_pointers: list
    objc_pointers: list

    pointer_compare_strings: List[str]


    def __init__(self) -> None:
        self.func_pointers = []
        self.new_func_ptrs = []
        self.send_functions = []
        self.kivy_properties = []
        self.calltitle = None
        self.enum_list = []
        self.dispatch_mode = False

        self.pointer_compare_strings = []
        self.pointer_types = []
        self.cy_pointers = []
        self.objc_pointers = []


    @staticmethod
    def new_from_parsed_code(string:str) -> list:
        module = ast.parse(string.replace("List[","["))
        wrap_list = []
        #wrap_class.parse_code(module)


        for class_body in module.body:
            
            if isinstance(class_body,ast.Assign):
                pass
            
            if isinstance(class_body,ast.ClassDef):
                wrap_class = WrapClass()
                wrap_class.parse_code(class_body)
                wrap_class.setup_callback_type()
                wrap_list.append(wrap_class)
        
        return wrap_list
        
        #global kivy_properties
        

    
    
    def parse_code(self,class_body):

        func_pointers: List[Function] = self.func_pointers
        new_func_ptrs: List[Function] = self.new_func_ptrs
        send_functions = self.send_functions
        kivy_properties = self.kivy_properties
        #global calltitle
        #self.calltitle = ""
        # for class_body in module.body:
        #     if isinstance(class_body,ast.Assign):
        #         pass
            
        #if isinstance(class_body,ast.ClassDef):

        self.calltitle = class_body.name
        
        #self.gen_send_start_function(send_functions)
        _cdec = self.handle_class_decorators(class_body)
        # if _cdec:
        #     new_func_ptrs.extend(func_pointers)
        #if not _cdec:
        
        self.gen_send_start_function(send_functions)
        
        _cdec = None #Quick fix for deco bug
        if not _cdec:
            for cbody in class_body.body:
                
                if isinstance(cbody,ast.FunctionDef):

                    #print(ast.get_docstring(cbody))

                    temp = Function(self)
                    temp.code = ast.get_docstring(cbody)
                    new_func_ptrs.append(temp)
                    

                    _call_class = ""

                    self.handle_function_return(cbody, temp)
                    _dec = self.handle_function_decorators(cbody, temp, func_pointers)

                    if not _dec:
                        # temp.name = f"{temp.wrap_class.calltitle}_{cbody.name}"
                        temp.name = cbody.name
                        send_functions.append(temp)
                    else:
                        temp.name = cbody.name

                    func_arg_list = []

                    for i,_arg in enumerate(cbody.args.args):
                        func_arg: Arg
                        arg_type: str
                        func_arg, arg_type = Arg.generate_general_arg(_arg, _dec, func_arg_list, temp, i)

                    for child in cbody.body:

                        if isinstance(child,ast.Expr):
                            item: Expr = child

                            temp.callback = item.value.s
                ##Property Handler
                if isinstance(cbody,ast.AnnAssign):
                    #print("found AnnAssign",cbody.__dict__)
                    #print("\t%s"%cbody.target.id)
                    #print("\t%s"%cbody.annotation.id)
                    if cbody.annotation.id in ("NumericProperty"):
                        print("Dictionary")
                if isinstance(cbody,ast.Assign):
                    #print("found Assign",cbody.__dict__)
                    #print(cbody.targets[0].__dict__,cbody.value.__dict__)
                    if isinstance(cbody.value,ast.Call):
                        if hasattr(cbody.value,"func"):
                            #print(cbody.value.__dict__)
                            func_id = cbody.value.func.id
                            _func = cbody.value.func

                            #print(cbody.value.func.__dict__)
                            if func_id == "NumericProperty":
                                
                                prop_body: ast.Assign = cbody
                                target_id = prop_body.targets[0].id
                                prop_arg_type = cbody.value.args[0].id 

                                #print(func_id,target_id,prop_arg_type,prop_body.targets[0].__dict__)
                                self.kivy_properties.append(target_id)

                                #send_functions.append(temp)
                                prop_temp = Function(self)
                                prop_temp.name = "on_%s" % target_id
                                send_functions.append(prop_temp)
                                for i,_arg_tuple in enumerate([("wid","object"),(target_id,prop_arg_type)]):
                                    _arg_name,_arg_type = _arg_tuple
                                    prop_arg = Arg()
                                    prop_temp.args_.append(prop_arg)
                                    prop_arg.objc_name = "arg%d" % i
                                    prop_arg.call_name = _arg_name

                                    prop_arg.python_name = _arg_name
                                    prop_arg.cy_name = _arg_name
                                    prop_arg.python_type = python_types_dict[_arg_type]
                                    prop_arg.cy_type = ctypedef_types_dict[_arg_type]

                                    prop_arg.objc_type = typedef_types_dict[_arg_type]
                                prop_temp.call_args.append(_arg_name)
                                #if _cdec is "struct":
                                # cstruct_args = []
                                # for line in class_body.body:
                                #     cstruct_args.append((line.annotation.id,line.target.id))
                                # #print(cstruct_args)
                                # #print(self.gen_c_struct_custom(class_body.name,cstruct_args))
                                # cstruct_list.append((class_body.name,cstruct_args))
                                # python_types_dict.update({class_body.name:class_body.name})
                                # #print(python_types_dict)
                                # ctypedef_types_dict.update({class_body.name:class_body.name})
                                # typedef_types_dict.update({class_body.name:class_body.name})
                                # call_args_dict.update({class_body.name:"{arg}"})
                                # send_args_dict.update({class_body.name:"{arg}"})
                                #prop.
                                
        
        ptr_compare = []
        ptr_types2 = []
        
        #print("new_func_ptrs count", len(new_func_ptrs))
        pointer_test = func_pointers
        for func in pointer_test:
            self.add_callback_function(func)

        #     rtns = func.returns

        #     if not rtns:
        #         rtns = "void"

        #     #_arg: Arg
        #     compare =  [rtns]
        #     #compare.append(rtns)
        #     for _arg in func.args_:
        #         compare.append(_arg.cy_type)
            
        #     compare_string = " ".join(compare)
        #     func.compare_string = compare_string
        #     if 'callback' in func.decs:
        #         #print(compare_string not in ptr_compare, compare_string)
        #         if compare_string not in ptr_compare:
        #             print(f"adding {func.name}")
        #             ptr_compare.append(compare_string)
        #             ptr_types2.append(func)
        #         else:
        #             print(f"{func.name} already in there")
        #print(ptr_compare[0])
            
        for func in send_functions:
            real_arg = tuple(zip(func.arg_types,func.args))
            name = func.name

            _real_arg = list(dict.fromkeys(real_arg))
            func.real_args = real_arg
        #self.pointer_types = ptr_types2
        return (func_pointers,send_functions,ptr_types2)

    def setup_callback_type(self):
        
        for i, string in enumerate(self.pointer_compare_strings):
            for real_func in self.func_pointers:
                    #print(f"{func.name}:\n\tfunc: {func.compare_string}\n\tcompare {real_func.name}:{real_func.compare_string} \n\tmatch:{real_func.compare_string == func.compare_string}")

                if real_func.compare_string == string:
                #if [arg.cy_type for arg in real_func.args_ ] == [arg.cy_type for arg in func.args_ ]:
                    real_func.func_ptr = f"{self.calltitle}_ptr{i}"


    def add_callback_function(self,func: Function):
        # pointer_test = func_pointers
        # for func in pointer_test:

        rtns = func.returns

        if not rtns:
            rtns = "void"

        #_arg: Arg
        compare =  [rtns]
        #compare.append(rtns)
        for _arg in func.args_:
            compare.append(_arg.cy_type)
        
        compare_string = " ".join(compare)
        func.compare_string = compare_string
        #if 'callback' in func.decs:
        #print(compare_string not in ptr_compare, compare_string)
        if compare_string not in self.pointer_compare_strings:
            self.pointer_compare_strings.append(compare_string)
            #ptr_types2.append(func)
            self.pointer_types.append(func)
        else:
            print(f"{func.name} already in there")
        #self.func_pointers.append(func)

    def gen_cyfunction_pointers(self, objc=True):
        #print("gen_cyfunction_pointers",func_list, ptr_types) 
        #ptr_types = []
        #calltitle = self.calltitle
        #func_list = self.func_pointers
        #ptr_types: List[Function] = self.pointer_types
        count = 0
        function_pointers = []
        for func in self.pointer_types:
            types_list = []
            _arg: Arg
            for _arg in func.args_:
                _types = []

                if objc:
                    _types.append(_arg.objc_type)
                else:
                    _types.append(_arg.cy_type)
                _types.append(_arg.objc_name)

                str0 = " ".join(_types)
                types_list.append(str0)
            types_str = ", ".join(types_list)
            rtns = func.returns
            if rtns:
                if objc:
                    _rtns = typedef_types_dict[rtns]
                else:
                    _rtns = ctypedef_types_dict[rtns]
            else:
                _rtns = "void"
            if objc:
                obj_point = objc_func_pointer_string2.format(

                    #title= f"{calltitle}_ptr{count}",
                    title = func.func_ptr,
                    args=types_str, returns=_rtns

                    )
            else:
                obj_point = func_pointer_string2.format(
                    
                    title = func.func_ptr,
                    #title= f"{calltitle}_ptr{count}",
                    args=types_str, returns=_rtns
                    
                    )
            function_pointers.append(obj_point)

            # for real_func in func_list:
            #     #print(f"{func.name}:\n\tfunc: {func.compare_string}\n\tcompare {real_func.name}:{real_func.compare_string} \n\tmatch:{real_func.compare_string == func.compare_string}")

            #     if real_func.compare_string == func.compare_string:
            #     #if [arg.cy_type for arg in real_func.args_ ] == [arg.cy_type for arg in func.args_ ]:
            #         real_func.func_ptr = f"{calltitle}_ptr{count}"

            # count += 1
        return function_pointers


    def gen_send_start_function(self, pointers:list):
        calltitle = self.calltitle
        typedef_types_dict['PythonCallback'] = calltitle.lower()
        ctypedef_types_dict['PythonCallback'] = calltitle.lower()

        send = Function(self)
        send.arg_types = ['PythonCallback']
        send_arg = Arg()
        send_arg.objc_type = "struct " + calltitle + "Callback"
        send_arg.cy_type = calltitle + "Callback"
        send_arg.objc_name = 'callback'
        send_arg.cy_name = 'callback'
        send.args_.append(send_arg)
        send.name = 'set_%s_Callback' % calltitle
        send.init_func = True
        # send.real_args = ((calltitle.lower(),'callback')),

        pointers.append(send)

    def handle_class_decorators(self,cbody):
        func_ptrs = self.func_pointers
        new_func_pointers = self.new_func_ptrs
        id = None
        for cdec in cbody.decorator_list:
            #print(cdec.__dict__)
            
            if isinstance(cdec,ast.Call):
                id: ast.Name = cdec.func.id
            else:
                id = cdec.id
        # if not _cdec:
        #     calltitle = cbody.name
        #     self.gen_send_start_function(send_functions)
        #else:
            if id == "EventDispatcher":
                self.dispatch_mode = True
                self.handle_event_dispatcher(cdec, func_ptrs, new_func_pointers)
            if id == "enum":
                enum_args = []
                for line in cbody.body:
                    pass
                    #enum_args.append((line.annotation.id,line.target.id))

            if id == "struct":
                cstruct_args = []
                for line in cbody.body:
                    cstruct_args.append((line.annotation.id,line.target.id))
                #print(cstruct_args)
                #print(self.gen_c_struct_custom(class_body.name,cstruct_args))
                self.cstruct_list.append((cbody.name,cstruct_args))
                python_types_dict.update({cbody.name:cbody.name})
                #print(python_types_dict)
                ctypedef_types_dict.update({cbody.name:cbody.name})
                typedef_types_dict.update({cbody.name:cbody.name})
                call_args_dict.update({cbody.name:"{arg}"})
                send_args_dict.update({cbody.name:"{arg}"})
        return id

    def handle_event_dispatcher(self, decorator: ast.Call, func_ptrs: List[Function], new_func_pointers: List[Function]):
        #print("handle_event_dispatcher", decorator)
        #pprint(decorator.__dict__)
        calltitle = self.calltitle
        if len(decorator.args) != 0:
            events: ast.List = decorator.args[0]
            
            #key: ast.Constant
            d = {}
            ptr_compare = []
            self.global_events = _events_ = [event.value for event in events.elts]
            enum = (self.calltitle,_events_)
            self.enum_list.append(enum)

            # for i, key in enumerate(events.elts):
            #     #print(key.__dict__)
            #     value = key.value
                
                # d[key.value] = value

            func: Function = Function(self)
            func.name = "dispatchEvent"
            func.call_class = f"{calltitle}_shared.dispatch"
            func.call_target = ""
            func.code = None
            func.global_dispatch = True
            body_name = f"{calltitle}Events"
            #func_ptrs.append(func)
            
            arg0 = Arg()
            #arg0.is_json = True
            arg0.python_name = "event"
            arg0.cy_name = "event"
            arg0.cy_type = body_name
            arg0.python_type = "object"
            arg0.objc_name = "arg0"
            arg0.objc_type = body_name
            arg0.custom_call = True
            arg0.call_code = f"{calltitle}_events[<int>arg0]"
            

            # arg0.call_code = f"{calltitle}"
            
            func.args_.append(arg0)
            
            arg1 = Arg()
            arg1.is_json = True
            arg1.python_name = "largs"
            arg1.cy_name = "largs"
            arg1.cy_type = ctypedef_types_dict["json"]
            arg1.python_type = "object"

            arg1.objc_name = "arg1"
            arg1.objc_type = typedef_types_dict["json"]
            func.args_.append(arg1)
            arg1.custom_call = True
            arg1.call_code = f"*json.loads(arg1)"

            arg2 = Arg()
            arg2.is_json = True
            arg2.python_name = "kwargs"
            arg2.cy_name = "kwargs"
            arg2.cy_type = ctypedef_types_dict["json"]
            arg2.python_type = "object"
            arg2.custom_call = True
            arg2.call_code = f"**json.loads(arg2)"

            arg2.objc_name = "arg2"
            arg2.objc_type = typedef_types_dict["json"]
            func.args_.append(arg2)
            #func.
            #func.call_args.extend(["event", "value"])
            objc = False
            types_list = []

            #func.compare_string = compare_string = " ".join(["void", arg0.cy_type, arg1.cy_type])
            func.decs.append("callback")

            func_ptrs.append(func)


            
            python_types_dict.update({body_name:body_name})
            #print(python_types_dict)
            ctypedef_types_dict.update({body_name:body_name})
            typedef_types_dict.update({body_name:body_name})
            call_args_dict.update({body_name:"{arg}"})
            send_args_dict.update({body_name:"{arg}"})

    def handle_function_return(self, body: FunctionDef, func: Function):
        rtns = body.returns
        if rtns:
            if isinstance(rtns, ast.Subscript):
                d = {
                    "value": rtns.value.__dict__,
                    "slice": rtns.slice.__dict__,
                    "ctx": rtns.ctx.__dict__
                }
                pprint(d)
            else:
                func.returns = rtns.id
        else:
            func.returns = None

    def handle_function_decorators(self, body: FunctionDef, func: Function, func_pointers: List[Function]) -> str:
        _dec = None
        for dec in body.decorator_list:
            #print(dec.__dict__)
            if isinstance(dec,ast.Call):
                _dec = dec.func.id
            else:
                _dec = dec.id
            if _dec:
                #print(_dec)
                func.decs.append(_dec)
                if _dec == 'callback':
                    pass
                    #self.add_callback_function(func)
                    func_pointers.append(func)
                elif _dec == 'call_args':
                    for arg in dec.args:
                        #print(arg.id)
                        func.call_args.append(arg.id)
                elif _dec == "call_class":
                    #print("call_class:",dec.args[0].id)
                    func.call_class = dec.args[0].id
                    _call_class = dec.args[0].id
                elif _dec == "call_target":
                    #print("call_target:",dec.args[0].id)
                    func.call_target = dec.args[0].id
        return _dec

class PythonCallBuilder():
    app_dir: str
    root_path: str
    dispatch_mode: bool
    wrap_classes: List[WrapClass]
    def __init__(self,app_dir,root_path):
        self.app_dir = app_dir
        self.root_path = root_path
        self.dispatch_mode = False
        self.wrap_classes = []


    def get_calltitle(self):
        return self.module_title

    def get_typedef_types(self,t):
        if t in ["list(int)","list(long)","list(uint8)","list(float)","list(double)"]:
            pass
        else: 
            return t

    
        
    def gen_send_start_function(self, pointers:list):
        calltitle = self.calltitle
        typedef_types_dict['PythonCallback'] = calltitle.lower()
        ctypedef_types_dict['PythonCallback'] = calltitle.lower()

        send = Function(self)
        send.arg_types = ['PythonCallback']
        send_arg = Arg()
        send_arg.objc_type = "struct " + calltitle + "Callback"
        send_arg.cy_type = calltitle + "Callback"
        send_arg.objc_name = 'callback'
        send_arg.cy_name = 'callback'
        send.args_.append(send_arg)
        send.name = 'set_%s_Callback' % calltitle
        # send.real_args = ((calltitle.lower(),'callback')),

        pointers.append(send)

    def parse_helper(self, string: str):
        module = ast.parse(string)
        body_list = module.body
        for class_body in body_list:
            if isinstance(class_body,ast.ClassDef):
                class_list = class_body.body
                
                cbody_del_list = []
                for cbody in class_body.body:
                    _cdec = None
                    decorator_list = cbody.decorator_list
                    #dec_list = [dec.id for dec in cbody.decorator_list]
                    dec_list = []

                    for dec in decorator_list:
                        if isinstance(dec,ast.Call):
                            pass
                        if isinstance(dec,ast.Name):
                            dec_list.append(dec.id)
                    

                    if "callback" in dec_list:
                        #class_body.body.remove(cbody)
                        cbody_del_list.append(cbody)
                    else:
                        cbody: ast.FunctionDef
                        for arg in cbody.args.args:
                            anno = ast.Name
                            anno.id = "class"
                        cbody.args.args.insert(0,ast.arg(arg="self",annotation = None))
                        #cbody.args.args()
                
                for rem_body in cbody_del_list:
                    class_body.body.remove(rem_body)

        src = astor.to_source(module)
        return src


            
    def gen_cyfunction_pointers(self,wrap: WrapClass, objc=True):
        #print("gen_cyfunction_pointers",func_list, ptr_types) 
        #ptr_types = []
        calltitle = wrap.calltitle
        func_list = wrap.func_pointers
        ptr_types = wrap.pointer_types
        count = 0
        function_pointers = []
        for func in ptr_types:
            types_list = []
            _arg: Arg
            for _arg in func.args_:
                _types = []

                if objc:
                    _types.append(_arg.objc_type)
                else:
                    _types.append(_arg.cy_type)
                _types.append(_arg.objc_name)

                str0 = " ".join(_types)
                types_list.append(str0)
            types_str = ", ".join(types_list)
            rtns = func.returns
            if rtns:
                if objc:
                    _rtns = typedef_types_dict[rtns]
                else:
                    _rtns = ctypedef_types_dict[rtns]
            else:
                _rtns = "void"
            if objc:
                obj_point = objc_func_pointer_string2.format(

                    title= f"{calltitle}_ptr{count}",
                    args=types_str, returns=_rtns

                    )
            else:
                obj_point = func_pointer_string2.format(
                    
                    title= f"{calltitle}_ptr{count}",
                    args=types_str, returns=_rtns
                    
                    )
            function_pointers.append(obj_point)

            for real_func in func_list:
                #print(f"{func.name}:\n\tfunc: {func.compare_string}\n\tcompare {real_func.name}:{real_func.compare_string} \n\tmatch:{real_func.compare_string == func.compare_string}")

                if real_func.compare_string == func.compare_string:
                #if [arg.cy_type for arg in real_func.args_ ] == [arg.cy_type for arg in func.args_ ]:
                    real_func.func_ptr = f"{calltitle}_ptr{count}"

            count += 1
        return function_pointers

    def gen_c_struct(self,wrap: WrapClass):
        cython_struct = f"\tctypedef struct {wrap.calltitle}Callback:"
        struct_strings = [cython_struct]
        func: Function
        for func in wrap.func_pointers:
            string = f"\t\t{func.func_ptr} {func.name}"
            struct_strings.append(string)

        return "\n".join(struct_strings)


    def gen_c_enum(self, title: str, enums: List[str], objc=False):
        if objc:
            #enum_head = f"typedef enum {title}Events {{\n"
            enum_head = f"typedef NS_ENUM(NSUInteger, {title}Events) {{\n"
            
        else:
            enum_head = f"\tctypedef enum {title}Events:\n"
        enum_string = ",\n".join([f"\t\t{enum}" for enum in enums])
        if objc:
            #enum_string += f"\n\t\t}} {title}Events;"
            enum_string += "\n\t\t};"
        
        return enum_head + enum_string



    def gen_c_struct_custom(self,title:str, pointers:list,objc=False):
        if objc:
            cython_struct = "typedef struct %s {" % title
        else:
            cython_struct = "\tctypedef struct %s:" % title
        struct_strings = [cython_struct]
        func: Function
        for func in pointers:
            if objc:
                #string = "\t%s _Nonnull %s;" % (typedef_types_dict[func[0]],func[1])
                string = "\t%s %s;" % (typedef_types_dict[func[0]],func[1])
            else:
                string = "\t\t%s %s" % (ctypedef_types_dict[func[0]],func[1])
            struct_strings.append(string)
        if objc:
            struct_strings.append("};")
            #struct_strings.append("typedef struct %s %s;" % (title +"Struct",title.lower()+"struct"))
        else:
            pass
            #struct_strings.append("\tctypedef %s %s" % (title +"Struct",title.lower()+"struct"))
        return "\n".join(struct_strings)

    def gen_objc_struct(self, wrap:WrapClass):
        pointers = wrap.func_pointers
        cython_struct = "typedef struct %sCallback {" % wrap.calltitle
        struct_strings = [cython_struct]
        func: Function
        for func in pointers:
            if func.returns:
                rtns = func.returns
            else:
                rtns = "void"
            string = "\t%s _Nonnull %s;" % (func.func_ptr,func.name)
            struct_strings.append(string)
        struct_strings.append("} %sCallback;" % wrap.calltitle)
        return "\n".join(struct_strings)

    def fill_cstruct(self,wrap: WrapClass):
        pointers = wrap.func_pointers
        assign_struct = "\t\tcdef %sCallback callbacks = [" % wrap.calltitle

        assign_strings = [assign_struct]
        size = len(pointers) -1
        for i,func in enumerate(pointers):
            if i != size:
                string = f"\t\t{func.wrap_class.calltitle}_{func.name}," 
            else:
                string = f"\t\t{func.wrap_class.calltitle}_{func.name}"
            assign_strings.append(string)
        assign_strings.append("\t\t]")
        assign_export_struct = "\n\t".join(assign_strings)
        
        
        return assign_export_struct

    def gen_cython_class(self,wrap:WrapClass,call_var:str,fill_struct:str):
        title = wrap.calltitle
        #kivy_props = wrap.kivy_properties
        class_list = []
        if self.dispatch_mode:
            class_list.append(cython_class_dispatch.format(_class=title,call_var=call_var, events = wrap.enum_list[0][1]) )
        else:
            class_list.append(cython_class.format(_class=title,call_var=call_var) )
        class_list.append(fill_struct )
        class_list.append("\t\tset_%s_Callback(callbacks)" % title )
        #print(kivy_properties)
        for _prop in wrap.kivy_properties:
            prop_str = "{0}.bind({1}=self.on_{1})".format("callback_class",_prop)
            class_list.append("\t\t%s" % prop_str)
        return "\n".join(class_list)

    def gen_send_args(self, func_arg:Arg):
        #arg_type = func_arg.cy_type
        if func_arg.is_list:
            if func_arg.is_data:
                arg_size = 1
                arg_type = 'uint8'
            else:
                arg_size = arg_size_dict[func_arg.list_type]
                arg_type = func_arg.list_type
            if func_arg.list_type == "str":
                decode = "<bytes>"#".encode('utf-8')"
                array_line = strlist_2_array.format(
                    arg = func_arg.cy_name,
                    arg_type = ptr_type_dict[arg_type],
                    type_size = arg_size,
                    decode = decode
                )
            else:
                if func_arg.list_type == "object":
                    if func_arg.is_data:
                        decode = f"json.dumps({func_arg.cy_name}).encode('utf-8')"
                    else:
                        decode = "<const void*>"
                else:
                    decode = ""
                array_line = list_2_array.format(
                    arg = func_arg.cy_name,
                    arg_type = ptr_type_dict[arg_type],
                    type_size = arg_size,
                    decode = decode
                )
            return array_line
        if func_arg.is_data:
            lines = [f"cdef int {func_arg.python_name}_size = len({func_arg.python_name})"]
            if func_arg.is_json:
                lines.append(f"cdef bytes jbytes = json.dumps({func_arg.python_name}).encode('utf-8')")

            output = "\n\t\t".join(lines)
            return f"\t\t{output}"
        #else: 
            #return send_args_dict[func_arg.python_type].format(arg=func_arg.python_name)
        return None

    def gen_cyfunc_sends(self, func:Function,args,args2,rtn,has_args=False):
        title = func.name
        utitle = f"{func.wrap_class.calltitle}_{title}"
        if has_args:
            args2_list = []
            _arg: Arg
            for i,_arg in enumerate(func.args_):
                 
                #args2_list.append(call_args_dict[_type].format(arg=func.args[i]))
                if _arg.is_list:
                    args2_list.append(_arg.cy_name+"_array")
                else:
                    #print("gen_cyfunc_sends",_arg.python_type)
                    #args2_list.append(_arg.cy_name)
                    if _arg.is_json:
                        if _arg.is_data:
                            args2_list.append("jbytes")
                        else:
                            args2_list.append(send_args_dict["json"].format(arg=_arg.python_name) )
                    else:
                        #print("send_arg name:",send_args_dict[_arg.python_type].format(arg=_arg.python_name))
                        args2_list.append(send_args_dict[_arg.python_type].format(arg=_arg.python_name) )
                    
        if rtn:
            if rtn == 'str':
                if has_args:
                    call = "return {utitle}({args2}).decode('utf8')".format(utitle=utitle, args2= ", ".join(args2_list))
                else:
                    call = "return {utitle}().decode('utf8')".format(utitle=utitle)
            else:
                if has_args:
                    call = "return {utitle}({args2})".format(utitle=utitle, args2= ", ".join(args2_list))
                else:
                    call = "return {utitle}()".format(utitle=utitle)
        else:
            if has_args:
                #print("args2_list",args2_list)
                args2= ", ".join(args2_list)
                call = f"{utitle}({args2})"
            else:
                call = f"{utitle}()"


        ###### body #####
        body_list = []
        func:Function
        print(f"function {func.name} - args_: {func.args_}")
        for i, arg in enumerate(func.args_):
            if arg is not "PythonCallback":
                _arg = self.gen_send_args(arg)
                if _arg:
                    #type_size = arg_size_dict[_type]
                    body_list.append(_arg)
                    print("body",_arg)
               
        p_arg_list = []
        free_list = []
        _arg:Arg
        for i,_arg in enumerate(func.args_):
            if not _arg.is_counter:
                p_arg_list.append( ":".join([_arg.python_name,_arg.python_type]))
            

  
            if _arg.is_list:
        
                free_str = "free(%s_array)" % _arg.cy_name
                free_list.append(free_str)
        if func.returns == None:
            rtn_string = class_cyfunc_send_plain.format(title=title,args=", ".join(p_arg_list),call=call, body="\n".join(body_list))
        else:
            rtn_string = class_cyfunc_send_rtn.format(title=title,args=", ".join(p_arg_list),call=call, body="\n".join(body_list),rtn_arg=python_types_dict[func.returns])
        for free in free_list:
            rtn_string += "\n\t\t" + free
        
        return rtn_string + "\n"

    def gen_global_events(self):
        event_strings = ["######## Global Dispatch Events ########"]
        for event in self.global_events:
            s = global_event_function.format(
                title = event
            )
            event_strings.append(s)
        if self.dispatch_mode:
            return "\n".join(event_strings)
        else:
            return ""

    def gen_send_functions(self,wrap: WrapClass, objc=False, subtitle=None, header=False):
        pointers = wrap.send_functions
        
        # for i in range(len(pointers)):
        #     ptr:Function = pointers[i]
        #     calltitle = self.calltitle
        #     #print(ptr.name)
        calltitle = wrap.calltitle
        
        sfunctions = []
        if not header and objc:
            s1 = re.sub( r"([A-Z])", r" \1", calltitle).split()
            s2 = []
            for item in s1:
                s2.append(item.lower())
            s3 = "_".join(s2)
            sfunctions.append(ext_send_callback.format(title=calltitle,title_l=calltitle,subtitle=s3,returns="void"))
        if header and objc:
            sfunctions.append(ext_send_callback_h.format(title=calltitle,title_l=calltitle,returns="void"))
        for i,func in enumerate(pointers):
            utitle = f"{func.wrap_class.calltitle}_{func.name}"
            types_list = []
            types_list2 = []
            rtns = func.returns
            if rtns is not None:
                if objc:
                    _rtns = typedef_types_dict[rtns]
                else:
                    _rtns = ctypedef_types_dict[rtns]
            else:
                _rtns = "void"

            args2 = []
            func: Function
            _args: Arg
            for _args in func.args_:
                _types = []
                args2.append(_args.objc_type)
                if _args.python_name is "":
                    send_arg = _args.objc_name
                else:
                    send_arg = _args.python_name
                        
                str0 = " ".join((_args.objc_type,send_arg))
                types_list.append(str0)
            if objc:
                if subtitle:
                    s1 = re.sub( r"([A-Z])", r" \1", subtitle).split()
                    s2 = []
                    for item in s1:
                        s2.append(item.lower())
                    s3 = "_".join(s2)
                    subt = s3
                else:
                    subt = "delegate"
                types_str = ", ".join(types_list)
                objc_arg_tmp = []
                arg: Arg
                for ie, arg in enumerate(func.args_):
                    # if arg.python_name is "":
                    #     send_arg = arg.objc_name
                    # else:
                    #     send_arg = arg.python_name
                    # if ie != 0:
                    #     tmp_str = objc_arg.format(t=arg.objc_type, arg=send_arg)
                    # else:
                    #     tmp_str = objc_arg_first.format(t=arg.objc_type, arg=send_arg)
                    #objc_arg_tmp.append(tmp_str)
                    objc_arg_tmp.append(arg.gen_send(ie, objc, header))
                    #objc_arg_tmp.append(arg.objc_name)
                args2_str = " ".join(objc_arg_tmp)
                ######## objc ############
                if header:
                    if i != 0 and not func.init_func:
                        head_title = utitle
                    else:
                        head_title = func.name
                    sfunctions.append( ext_objcfunc_h.format(title=head_title, args=types_str, returns=_rtns) )
                else:
                    if func.init_func:
                        real_title = func.name
                    else:
                        real_title = utitle
                    if rtns is not None:
                        if len(func.args_) != 0:
                            sfunctions.append( ext_objcfunc_m_rtn.format(title=real_title, call=func.name, args=types_str, args2=args2_str ,subtitle = subt, returns=_rtns) )
                        else:
                            sfunctions.append( ext_objcfunc_m_rtn_noarg.format(title=real_title, call=func.name, args=types_str, subtitle = subt, returns=_rtns) )
                    else:
                        if len(func.args_) != 0:
                            sfunctions.append( ext_objcfunc_m.format(title=real_title, call=func.name, args=types_str, args2=args2_str ,subtitle = subt, returns=_rtns) )
                        else:
                            sfunctions.append( ext_objcfunc_m_noarg.format(title=real_title, call=func.name, args=types_str, subtitle = subt, returns=_rtns) )
            else:
                types_str = ", ".join(types_list)
                if header:
                    #for arg in func.args_:
                    
                    types_str = ", ".join([" ".join((arg.cy_type,arg.cy_name)) for arg in func.args_])
                    #sfunctions.append( ext_cyfunc.format(title=func.name, args=types_str ,returns=_rtns) )
                    if i != 0:
                        sfunctions.append( ext_cyfunc.format(title=utitle, args=types_str ,returns=_rtns) )
                    else:
                        sfunctions.append( ext_cyfunc.format(title=func.name, args=types_str ,returns=_rtns) )
                else:
                    #print("send_func",func.name)
                    # for _arg_ in func.args_:
                    #     #print(_arg_.__dict__)
                    sfunctions.append( self.gen_cyfunc_sends(func,types_list,", ".join(args2),func.returns,len(func.args_) != 0) )
                # pprint("".join(sfunctions)
            
        if not header and not objc:
            if len(sfunctions) != 0:
                del sfunctions[0]
        return "\n".join( sfunctions )

    def gen_cython_callbacks(self, pointers:list):
        cy_functions = []
        func: Function
        for i,func in enumerate(pointers):
            _title = func.name
            #args = func.real_args
            types_list = []
            args2 = []
            arg:Arg
            for arg in func.args_:
                
                _types = []
                _types.append(arg.cy_type)
                _types.append(arg.objc_name)
                args2.append(arg.cy_name)
                #print(func.name,"callback arg",arg.__dict__)
            # for types in func.real_args2:
            #     _types = []
            #     for i,_type in enumerate(types):
            #         if i%2:
            #             _types.append(_type)
            #             args2.append(_type)
            #         else:
            #             _types.append(ctypedef_types_dict[_type])
                        
                str0 = " ".join(_types)
                types_list.append(str0)
            args_str = ", ".join(types_list)
            call_args = []
            #call_arg: Arg
            _call_class = func.call_class
            for call_arg in func.args_:
                if _call_class != call_arg.python_name:
                    if call_arg.is_list:
                        call_args.append(call_list_dict[call_arg.list_type].format(arg=call_arg.objc_name))
                    else:
                        if not call_arg.is_counter:
                            if call_arg.custom_call:
                                arg_name = call_arg.call_code
                            else:
                                if call_arg.is_json:
                                    if call_arg.is_data:
                                        arg_name = call_args_dict["jsondata"].format(arg=call_arg.objc_name)
                                    else:
                                    #print("json arg:",call_arg.python_name)
                                        arg_name = call_args_dict["json"].format(arg=call_arg.objc_name)
                                elif call_arg.is_data:
                                    arg_name = call_args_dict["data"].format(arg=call_arg.objc_name)
                                else:
                                    arg_name = call_args_dict[call_arg.python_type].format(arg=call_arg.objc_name)
                            call_args.append(arg_name)

            callback = "(%s)" % ", ".join(call_args)#.split(".")[-1]
            rtns = func.returns
            if rtns:
                _rtns = ctypedef_types_dict[rtns]
            else:
                _rtns = "void"
            if len(func.call_args) != 0:
                callback = "(%s)" % ", ".join(func.call_args)
            if func.call_target != "":
                call = ".".join((func.call_target,_title))
            else:
                if func.global_dispatch:
                    call = ""
                else:
                    call = _title
            if func.code:
                code = func.code.replace("\n","\n\t") #+ callback
                
                s = cython_callback3.format(title=_title,
                                            call=call,callback=callback,
                                            args = args_str,
                                            call_class=func.call_class,
                                            _class=func.wrap_class.calltitle,
                                            returns=_rtns,code=code
                                            )
            else:
                if func.global_dispatch:

                    s = cython_global_dispatch.format(  title=_title,
                                                        callback=callback,
                                                        args = args_str,
                                                        _class=func.wrap_class.calltitle,
                                                        call_class=func.call_class,
                                                        returns=_rtns
                                                        )
            
                else:
                    s = cython_callback2.format(title=_title,
                                                call=call,callback=callback,
                                                args = args_str,
                                                call_class=func.call_class,
                                                _class=func.wrap_class.calltitle,
                                                returns=_rtns
                                                )
            cy_functions.append(s)
        
        return "".join(cy_functions)

    def gen_structtype_init_funct(self, title:str, objc=False):
        if objc:
            return objc_structinit_string.format(title=title,call=title)
        else:
            return c_structinit_string.format(title=title,call=title)

    def gen_objc_m_header(self, title):
        return m_header_string.format(title=title)

    def gen_objc_protocol(self, wrap:WrapClass):
        pointers = wrap.send_functions
        title = wrap.calltitle
        sfunctions = []
        sfunctions.append(protocol_start.format(title=title))
        for i,func in enumerate(pointers):
            
            types_list = []
            args2 = []
            arg_types = func.arg_types
            #args = func.args
            x:Arg
            for i, x in enumerate(func.args_):
                #print(func.name,x.cy_name,x.python_name)
                if x.python_name is "":
                    proto_arg = x.cy_name
                else:
                    proto_arg = x.python_name
                if i != 0:
                    types_list.append(protocol_arg.format(type=x.objc_type,arg=proto_arg))
                else:
                    types_list.append(protocol_first_arg.format(type=x.objc_type,arg=proto_arg))


            arg_string = " ".join(types_list)  
            name = func.name
            rtns = func.returns
            if rtns:
                _rtns = typedef_types_dict[rtns]
            else:
                _rtns = "void"
            if len(types_list) != 0:
                line = protocol_line_start.format(title=name,args=arg_string, returns= _rtns)
            else:
                line = protocol_line_noarg.format(title=name, returns= _rtns)
            sfunctions.append(line)
        
        sfunctions.append("@end\n")
        s1 = re.sub( r"([A-Z])", r" \1", title).split()
        s2 = []
        for item in s1:
            s2.append(item.lower())
        s3 = "_".join(s2)
        # pro_id = protocol_id.format(title=title)
        # sfunctions.append(pro_id)
        static = protocol_static.format(title=title,subtitle=s3)
        sfunctions.append(static)
        return "\n".join(sfunctions)
        
    
    def gen_module_file(self,class_name):
        
        _tmp = {
            "title": self.module_title,
            "depends": None,
            "classname": class_name,
            "dirname": class_name,
            "type": "",
            "build_path": os.path.dirname(__file__)

        }
        
        _mfile = {
            
            "#MODULE_NAME" : self.module_title,

            #"root_name" : "",

            "#MODULE_FOLDER" : None,

            #"module_name_as_root" : True ,

            #"#PYTHONLINKROOT" : os.path.dirname(__file__)
            #"#PYTHONLINKROOT" : self.root_path
            "#PYTHONLINKROOT" : "/"

        }


        # try:
        #with open("./builds/%s/module.ini" % class_name, 'w') as configfile:
        
        if not os.path.exists(join(self.app_dir,"builds",class_name)):
            os.mkdir(join(self.app_dir,"builds",class_name))
        with open(join(self.app_dir,"builds",class_name,"module.ini"), 'w') as configfile:
            configfile.write(json.dumps([class_name,_tmp],indent=4))
            #configfile.close()

        

        #json.dump(_mfile,join(root_path,"builds",class_name,"module_name.json"))
        #kivy_recipe_path = join("/Volumes/WorkSSD/kivy-ios-11.04.20_copy/recipes",calltitle)
        builds = join(self.app_dir,"builds",class_name)
        with open(join(builds,"kivy_recipe.py"),'w') as recipe:
            new_recipe = kivy_recipe

            new_recipe = new_recipe.replace("#MODULE_NAME","\"%s\"" % _mfile["#MODULE_NAME"])
            if _mfile["#MODULE_FOLDER"] != None:
                new_recipe = new_recipe.replace("#MODULE_FOLDER","\"%s\"" % _mfile["#MODULE_FOLDER"])
            else:
                new_recipe = new_recipe.replace("#MODULE_FOLDER","None")
            new_recipe = new_recipe.replace("#PYTHONLINKROOT","\"%s\"" % _mfile["#PYTHONLINKROOT"])
            #RECIPENAME_
            new_recipe = new_recipe.replace("#RECIPENAME_",self.module_title)
            recipe.write(new_recipe)
        # with open(join(root_path,"builds",class_name,"module_name.json"), 'w') as module_file:
        #     json.dump(_mfile,module_file)
        # shutil.copy(join(root_path,"builds",class_name,"module_name.json"),join(kivy_recipe_path))
        #     for key,value in _tmp.items():
        #         module_file.write("{0} = \"{1}\"\n".format(key,value))
        # except:
        #     pass

    ##############################################################
    ############# Builder ########################################
    ##############################################################

    def generate_pyx(self):
        classes = self.wrap_classes
        
        if self.dispatch_mode:
            dispatch_import = "from kivy._event cimport EventDispatcher"
        else:
            dispatch_import = ""
        
        cy_list = [
            "#cython: language_level=3",
            dispatch_import,
            "import json",
            "from libc.stdlib cimport malloc, free",
            "from libcpp cimport bool as bool_t",
            f"cdef extern from \"_{self.module_title}.h\":",
        ]
        
        
        enums_structs = []
        if len(self.cstruct_list):
            enums_structs.append("\t\n".join([self.gen_c_struct_custom(arg[0],arg[1]) for arg in self.cstruct_list]))
        for wrap in classes: 
            #cy_ext = []       
            if len(wrap.enum_list):
                enums_structs.append( "\t\n".join([self.gen_c_enum(arg[0],arg[1]) for arg in wrap.enum_list]) )
            
            #cy_list.extend(cy_ext)
        if len(enums_structs):
            cy_list.append("\t######## cdef extern custom enums/structs: ########\n")
            cy_list.extend(enums_structs)

        cy_list.append("\t######## cdef extern Callback Function Pointers: ########")
        for wrap in classes:
            c_pointers = wrap.gen_cyfunction_pointers(False)
            cy_ext = [
                "\t" + "\t".join(c_pointers ),
                #"",  
            ]
            cy_list.extend(cy_ext)
        
        cy_list.append("\t######## cdef extern Callback Struct: ########")
        for wrap in classes:
            cy_ext = [
                
                self.gen_c_struct(wrap),   
                "" 
            ]
            cy_list.extend(cy_ext)

        cy_list.append("\n\t######## cdef extern Send Functions: ########")
        for wrap in classes:
            cy_ext_functions = [
                self.gen_send_functions(wrap,False,None,True),
                ""
            ]

            cy_list.extend(cy_ext_functions)

        for wrap in classes:
            
            if len(wrap.enum_list) != 0:
                export_enum_list = f"cdef list {wrap.calltitle}_events = {wrap.enum_list[0][1]}"
            else:
                export_enum_list = ""

            cy_classes = [
                # "\t\n".join([self.gen_c_enum(arg[0],arg[1]) for arg in enum_list]),
                # "\t\n".join([self.gen_c_struct_custom(arg[0],arg[1]) for arg in self.cstruct_list]),
                # "",
                # "\t######## cdef extern Callback Function Pointers: ########",
                # "\t" + "\t".join(c_pointers ),
                # "",
                # "\t######## cdef extern Callback Struct: ########",
                # self.gen_c_struct(wrap),
                # "",
                # self.gen_structtype_init_funct(calltitle,False) ,
                # "\t######## cdef extern Send Functions: ########\n",
                # self.gen_send_functions(wrap,False,None,True),
                "",
                "######## Callbacks Functions: ########\n",
                self.gen_cython_callbacks(wrap.func_pointers),
                "######## Cython Class: ########",
                export_enum_list,
                self.gen_cython_class(wrap,wrap.calltitle + "_voidptr",self.fill_cstruct(wrap)) ,
                "",
                self.gen_global_events(),
                "######## Send Functions: ########",
                self.gen_send_functions(wrap,False)
            ]
            cy_list.extend(cy_classes)
        string = "\n".join(cy_list)
        return string
    
    def generate_objc_h(self):
        classes = self.wrap_classes

        objc_strings = [
            "#import <Foundation/Foundation.h>\n"
        ]
        for wrap in classes:
            
            calltitle = wrap.calltitle
            c_pointers = wrap.new_func_ptrs
            send_functions = wrap.send_functions
            func_pointers = wrap.func_pointers
            ptr_types = wrap.pointer_types
            enum_list = wrap.enum_list
            objc_pointers = self.gen_cyfunction_pointers(wrap,True)


            objc_hlist = [
            
            "\t\n".join([self.gen_c_enum(arg[0],arg[1], True) for arg in enum_list]),
            "\n".join([self.gen_c_struct_custom(arg[0],arg[1],True) for arg in self.cstruct_list]),
            "\n\n",
            "//######## cdef extern Callback Function Pointers: ########//\n",
            "".join(objc_pointers ) ,
            "\n",
            "//######## cdef extern Callback Struct: ########//\n",
            self.gen_objc_struct(wrap),
            "\n\n",
            # #objc_hlist.append(self.gen_structtype_init_funct(calltitle,True) )
            "\n",
            "//######## cdef extern Send Functions: ########//\n",
            self.gen_objc_protocol(wrap),
            "\n",
            "//######## Send Functions: ########//\n",
            self.gen_send_functions(wrap,True,None,True)
            ]
            objc_strings.extend(objc_hlist)

        return "".join(objc_strings)

    def generate_objc_m(self):
        classes = self.wrap_classes
        string_list = [self.gen_objc_m_header(self.module_title)]
        for wrap in classes:
            
            calltitle = wrap.calltitle
            c_pointers = wrap.new_func_ptrs
            send_functions = wrap.send_functions
            func_pointers = wrap.func_pointers
            ptr_types = wrap.pointer_types
            enum_list = wrap.enum_list

            #string_list.append(  )
            string_list.append( self.gen_send_functions(wrap,True,calltitle))
        return "\n".join(string_list)


    def build_py_files(self,script):
        global kivy_recipe
        #calltitle = self.calltitle
        file_title = os.path.basename(script)[:-3]
        with open(join(self.app_dir,"build_files","kivy_recipe.py")) as f:
            kivy_recipe = str(f.read())
        #global cstruct_list
        self.cstruct_list = []
        
        self.global_events = []
        #script = sys.argv[2]
        py3_compiler = "#cython: language_level=3\n"
        pyfile = open("{}".format(script), "r" )
        test = pyfile.read()

        wrap_classes: List[WrapClass] = WrapClass.new_from_parsed_code(test)
        self.wrap_classes = wrap_classes
        wrap_class = wrap_classes[0]
        #functions = self.parse_code(test)
        #self.calltitle = calltitle = wrap_class.calltitle
        self.module_title = module_title = file_title
        site_manager_path = join(root_path,"venv/lib/python3.8/site-packages")
        self.dispatch_mode = wrap_class.dispatch_mode
        # py_string = ""
        # with open(py_file, "r") as f:
        #     py_string = str( f.read().replace("@callback", "") )
        #     #py_string.splitlines()
        # with open(join(site_manager_path,"%s_cy.py" % calltitle), "w") as f:
        with open(join(site_manager_path,"%s.py" % module_title.lower()), "w") as f:
            f.write(self.parse_helper(test))
        pyfile.close()

        BUILD_DIR = join(self.app_dir,"builds")

        try:
            os.mkdir(BUILD_DIR)
            #os.mkdir("builds/%s" % calltitle.lower())
        except:
            print("builds exist")
        try:
            os.mkdir(join(BUILD_DIR,module_title))
        except:
            print("builds/%s exist" % module_title)
        pyx_script = self.generate_pyx()
        join(BUILD_DIR,module_title)
        with open(join(BUILD_DIR,module_title,f"{module_title}.pyx"), "w+") as pyx_file:
            pyx_file.write( pyx_script )

        objc_script = self.generate_objc_h()
        with open(join(BUILD_DIR,module_title,f"_{module_title}.h"), "w+") as objch_file:
            objch_file.write( objc_script )

        with open(join(BUILD_DIR,module_title,f"_{module_title}.m"), "w+") as objcm_file:
            objcm_file.write( self.generate_objc_m() )
        # f.write("\n")
        # f.write(self.gen_send_functions(send_functions,True,calltitle))
        # f.write(objc_hscript)
        # f = open(join(BUILD_DIR,calltitle.lower(),calltitle.lower()+"_cy.pyx"), "w+")
        # if self.dispatch_mode:
        #     dispatch_import = "from kivy._event cimport EventDispatcher"
        # else:
        #     dispatch_import = ""
        # if len(self.enum_list) != 0:
        #     export_enum_list = f"cdef list {calltitle}_events = {self.enum_list[0][1]}"
        # else:
        #     export_enum_list = ""
        # with open(join(BUILD_DIR,calltitle.lower(),calltitle.lower()+".pyx"), "w+") as f:
        #     cy_list = [
        #         "#cython: language_level=3",
        #         dispatch_import,
        #         "import json",
        #         "from libc.stdlib cimport malloc, free",
        #         "from libcpp cimport bool as bool_t",
        #         f"cdef extern from \"_{calltitle.lower()}.h\":",
        #         "\t\n".join([self.gen_c_enum(arg[0],arg[1]) for arg in self.enum_list]),
        #         "\t\n".join([self.gen_c_struct_custom(arg[0],arg[1]) for arg in self.cstruct_list]),
        #         "",
        #         "\t######## cdef extern Callback Function Pointers: ########",
        #         "\t" + "\t".join(c_pointers ),
        #         "",
        #         "\t######## cdef extern Callback Struct: ########",
        #         self.gen_c_struct(func_pointers),
        #         "",
        #         #self.gen_structtype_init_funct(calltitle,False) ,
        #         "\t######## cdef extern Send Functions: ########\n",
        #         self.gen_send_functions(send_functions,False,None,True),
        #         "",
        #         "######## Callbacks Functions: ########\n",
        #         self.gen_cython_callbacks(func_pointers),
        #         "######## Cython Class: ########",
        #         export_enum_list,
        #         self.gen_cython_class(calltitle,calltitle + "_voidptr",self.fill_cstruct(func_pointers)) ,
        #         "",
        #         self.gen_global_events(),
        #         "######## Send Functions: ########",
        #         self.gen_send_functions(send_functions,False)
        #     ]

        # #f.write(fill_cstruct(c_pointers))
        #     cy_script = "\n".join(cy_list)
        #     f.write(cy_script + "\n")

        # objc_hlist = []
        
        # objc_hlist.append("#import <Foundation/Foundation.h>\n")
        # objc_hlist.append("\t\n".join([self.gen_c_enum(arg[0],arg[1], True) for arg in self.enum_list]))
        # objc_hlist.append("\n".join([self.gen_c_struct_custom(arg[0],arg[1],True) for arg in self.cstruct_list]))
        # objc_hlist.append("\n\n")
        # objc_hlist.append("//######## cdef extern Callback Function Pointers: ########//\n")
        # objc_hlist.append("".join(objc_pointers ) )
        # objc_hlist.append("\n")
        # objc_hlist.append("//######## cdef extern Callback Struct: ########//\n")
        # objc_hlist.append(self.gen_objc_struct(func_pointers))
        # objc_hlist.append("\n\n")
        # #objc_hlist.append(self.gen_structtype_init_funct(calltitle,True) )
        # objc_hlist.append("\n")
        # objc_hlist.append("//######## cdef extern Send Functions: ########//\n")
        # objc_hlist.append(self.gen_objc_protocol(send_functions,calltitle))
        # objc_hlist.append("\n")
        # objc_hlist.append("//######## Send Functions: ########//\n")
        # objc_hlist.append(self.gen_send_functions(send_functions,True,None,True))

        # objc_hscript = "".join(objc_hlist)
        # f = open(join(BUILD_DIR,calltitle.lower(),"_%s.h" % calltitle.lower()), "w+")
        # f.write(objc_hscript)
        # f.close()

        # f = open(join(BUILD_DIR,calltitle.lower(),"_%s.m" % calltitle.lower()), "w+")
        # f.write(self.gen_objc_m_header(calltitle.lower()))
        # f.write("\n")
        # f.write(self.gen_send_functions(send_functions,True,calltitle))

        # f.close()

        self.gen_module_file(module_title.lower())

        return (pyx_script,objc_script)

#kivy_folder = "/Volumes/WorkSSD/kivy-ios-11.04.20_copy/"
kivy_folder = "/Volumes/WorkSSD/kivy_ios/"
def ProcessFiles(t,pack):
    p_build = PythonCallBuilder()
    t = sys.argv[1]
    pack = sys.argv[2]
    if t == "build":
        p_build.build_py_files()
        pack_all("PythonSwiftLink.zip",kivy_folder + ".cache/")
    elif t == "build_compile":
        p_build.build_py_files()
        pack_all("master.zip",calltitle)
        # subprocess.call(['python3.7',"%s/toolchain.py" % kivy_folder, "clean", calltitle])
        # subprocess.call(['python3.7',"%s/toolchain.py" % kivy_folder, "build", calltitle])
        subprocess.call(['',"toolchain" % kivy_folder, "clean", calltitle])
        subprocess.call(['',"toolchain" % kivy_folder, "build", calltitle])
        remove_cache_file(kivy_folder+".cache/"+calltitle+"-master.zip")

        

         
    elif t == "compile_all":
        pack_all("PythonSwiftLink-main.zip",kivy_folder + ".cache/")
        subprocess.call(['python3.7',"%s/toolchain.py" % kivy_folder, "clean", "PythonSwiftLink"])
        subprocess.call(['python3.7',"%s/toolchain.py" % kivy_folder, "build", "PythonSwiftLink"])
         
#(<object> classtest).func0(test.decode('utf-8'),test2)
#[test[x] for x in range(test_count)]