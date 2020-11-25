import parser
import ast
from ast import *
import astor
from pprint import pprint
import re
import sys
import os
import subprocess
from build_files.pack_files import pack_all,remove_cache_file
import configparser
import json
from os.path import join
import shutil

print(os.path.basename(sys.argv[0]))
print(os.path.dirname(sys.argv[0]))
root_path = os.path.dirname(sys.argv[0])

cstruct_list: list

calltitle = None 


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

ctypedef_types_dict = {
    "list(int)": "const int*",
    "list(long)": "const long*",
    "list(uint8)": "const unsigned char*",
    "list(float)": "const float*",
    "list(double)": "const double*",
    "list(str)": "const char* const*",

    "str": "const char*",
    "int": "int",
    "float": "float",
    "long": "long",
    "object": "void*",
    "json": "const char*",
    "bytes": "const char*",

    "bool": "bool_t",

    "PythonCallback": "PythonCallback"
}

ctypedef_list_dict = {
    "int": "const int*",
    "long": "const long*",
    "uint8": "const unsigned char*",
    "float": "const float*",
    "double": "const double*",
    "str": "const char* const*",
    
}

typedef_types_dict = {
    "list(int)": "const int* _Nonnull",
    "list(long)": "const long* _Nonnull",
    "list(uint8)": "const unsigned char* _Nonnull",
    "list(float)": "const float* _Nonnull",
    "list(double)": "const double* _Nonnull",
    "list(str)": "const char* _Nonnull const* _Nonnull",

    "str": "const char* _Nonnull",
    "int": "int",
    "float": "float",
    "long": "long",
    "object": "void* _Nonnull",
    "json": "const char* _Nonnull",
    "bytes": "const char*  _Nonnull",

    "bool": "BOOL",


    "PythonCallback": "PythonCallback"
}

typedef_list_dict = {
    "int": "const int* _Nonnull",
    "long": "const long* _Nonnull",
    "uint8": "const unsigned char* _Nonnull",
    "float": "const float* _Nonnull",
    "double": "const double* _Nonnull",
    "str": "const char* _Nonnull const* _Nonnull",
}

python_types_dict = {
    "list(int)": "list",
    "list(long)": "list",
    "list(uint8)": "list",
    "list(float)": "list",
    "list(double)": "list",
    "list(str)": "list",

    "str": "str",
    "int": "int",
    "float": "float",
    "long": "int",
    "object": "object",
    "json" : "object",
    "bytes": "bytes",

    "PythonCallback": "PythonCallback"
}

send_args_dict = {
    "list(int)": "[{arg} for x in range({arg}_count)]",
    "list(long)": "[{arg} for x in range({arg}_count)]",
    "list(uint8)": "[{arg} for x in range({arg}_count)]",
    "list(float)": "[{arg} for x in range({arg}_count)]",
    "list(double)": "[{arg} for x in range({arg}_count)]",
    "list(str)": "[{arg}.decode('utf8') for x in range({arg}_count)]",

    "str": "{arg}.encode('utf-8')",
    "int": "{arg}",
    "float": "{arg}",
    "long": "{arg}",
    "object": "<void*>{arg}",
    "json": "json.dumps({arg})",
    "bytes": "{arg}",

    "PythonCallback": "{arg}",
    "": "{arg}"
}

call_args_dict = {
    "list(int)": "[{arg} for x in range({arg}_count)]",
    "list(long)": "[{arg} for x in range({arg}_count)]",
    "list(uint8)": "[{arg} for x in range({arg}_count)]",
    "list(float)": "[{arg} for x in range({arg}_count)]",
    "list(double)": "[{arg} for x in range({arg}_count)]",
    "list(str)": "[{arg}.decode('utf8') for x in range({arg}_count)]",

    "str": "{arg}.decode('utf8')",
    "int": "{arg}",
    "float": "{arg}",
    "long": "{arg}",
    "object": "<object>{arg}",
    "json": "json.loads({arg})",
    "bytes": "{arg}",

    "PythonCallback": "PythonCallback"
}




call_list_dict = {
    "int": "[{arg}[x] for x in range({arg}_size)]",
    "long": "[{arg}[x] for x in range({arg}_size)]",
    "uint8": "[{arg}[x] for x in range({arg}_size)]",
    "float": "[{arg}[x] for x in range({arg}_size)]",
    "double": "[{arg}[x] for x in range({arg}_size)]",
    "str": "[{arg}[x].decode('utf8') for x in range({arg}_size)]",
    "PythonCallback": "PythonCallback"
}
arg_size_dict = {
        "list(int)": 4,
        "list(long)": 8,
        "list(uint8)": 1,
        "list(float)": 4,
        "list(double)": 8,
        "list(str)": 1,

        "str": 1,
        "int": 4,
        "float": 4,
        "long": 8,
    }
cython_class = """\
cdef public void* {_class}_voidptr
cdef class {_class}:
\tdef __init__(self,object _{call_var}):
\t\tglobal {call_var} 
\t\t{call_var} = <void*>_{call_var}
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

call_args_dict2 = {
    "list(int)": "[{arg} for x in range({arg}_count)]",
    "list(long)": "[{arg} for x in range({arg}_count)]",
    "list(uint8)": "[{arg} for x in range({arg}_count)]",
    "list(float)": "[{arg} for x in range({arg}_count)]",
    "list(double)": "[{arg} for x in range({arg}_count)]",
    "list(str)": "[{arg}.decode('utf8') for x in range({arg}_count)]",

    "str": "{arg}.decode('utf8')",
    "int": "{arg}",
    "float": "{arg}",
    "long": "{arg}",

    "PythonCallback": "PythonCallback"
}

arg_size_dict = {
        "list(int)": 4,
        "list(long)": 8,
        "list(uint8)": 1,
        "list(float)": 4,
        "list(double)": 8,
        "list(str)": 1,

        "str": 1,
        "uint8": 1,
        "int": 4,
        "float": 4,
        "long": 8,
        "double": 8,
    }

ptr_type_dict = {
        "list(int)": "int",
        "list(long)": "long",
        "list(uint8)": "unsigned char",
        "list(float)": "float",
        "list(double)": "double",
        "list(str)": "const char*",

        "str": "const char*",
        "int": "int",
        "float": "float",
        "long": "long",
        "double": "double",
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
    [{subtitle} {title}:{args2}];
}}
"""

ext_objcfunc_m_rtn = """\
{returns} {title}({args}){{
    return [{subtitle} {title}:{args2}];
}}
"""

ext_objcfunc_m_noarg = """\
{returns} {title}({args}){{
    [{subtitle} {title}];
}}
"""

ext_objcfunc_m_rtn_noarg = """\
{returns} {title}({args}){{
    return [{subtitle} {title}];
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
cdef void cy_{title}({args}) with gil:
\t(<object> {_class}).{title}{callback}

"""
cython_callback2 = """\
cdef {returns} cy_{title}({args}) with gil:
\t(<object> {_class}).{call}{callback}

"""

cython_callback3 = """\
cdef {returns} cy_{title}({args}) with gil:
\t{code}
\t(<object> {_class}).{call}{callback}

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
#import "{title}.h"
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
    counter_name: str
    list_type: str

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
        self.is_counter = False
        self.is_json = False
        self.counter_name = ""
        self.list_type = ""


class Function():
    args_: list
    args: list
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



    def __init__(self):
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
        self.call_class = calltitle + "_voidptr"
        self.call_target = ""

class PythonCallBuilder():

    def __init__(self):
        pass


    def get_calltitle(self):
        return calltitle

    def get_typedef_types(self,t):
        if t in ["list(int)","list(long)","list(uint8)","list(float)","list(double)"]:
            pass
        else: 
            return t
        
    def gen_send_start_function(self, pointers:list):
        typedef_types_dict['PythonCallback'] = calltitle.lower()
        ctypedef_types_dict['PythonCallback'] = calltitle.lower()
        # send = {
        #     'arg_types' : ['PythonCallback'],
        #     'args' : ['callback'],
        #     'name' : 'SendCallback',
        #     'real_args' : ((calltitle.lower(),'callback')),
        #     'returns' : None

        # }
        send = Function()
        send.arg_types = ['PythonCallback']
        send_arg = Arg()
        send_arg.objc_type = "struct " + calltitle + "Callback"
        send_arg.cy_type = calltitle + "Callback"
        send_arg.objc_name = 'callback'
        send_arg.cy_name = 'callback'
        send.args_.append(send_arg)
        send.name = 'Send%sCallback' % calltitle
        # send.real_args = ((calltitle.lower(),'callback')),

        pointers.append(send)

    def parse_code(self, string:str):
        module = ast.parse(string)
        func_pointers = []
        new_func_ptrs = []
        send_functions = []
        global calltitle
        for class_body in module.body:
            if isinstance(class_body,ast.Assign):
                pass

            if isinstance(class_body,ast.ClassDef):
                
                
                #self.gen_send_start_function(send_functions)
                _cdec = None
                #print(class_body.name)
                for cdec in class_body.decorator_list:
                    
                    _cdec = cdec.id
                if not _cdec:
                    calltitle = class_body.name
                    self.gen_send_start_function(send_functions)
                else:
                    if _cdec is "struct":
                        cstruct_args = []
                        for line in class_body.body:
                            cstruct_args.append((line.annotation.id,line.target.id))
                        #print(cstruct_args)
                        #print(self.gen_c_struct_custom(class_body.name,cstruct_args))
                        cstruct_list.append((class_body.name,cstruct_args))
                        python_types_dict.update({class_body.name:class_body.name})
                        #print(python_types_dict)
                        ctypedef_types_dict.update({class_body.name:class_body.name})
                        typedef_types_dict.update({class_body.name:class_body.name})
                        call_args_dict.update({class_body.name:"{arg}"})
                        send_args_dict.update({class_body.name:"{arg}"})
                #cbody: ast.FunctionDef().type_comment
                if not _cdec:
                    for cbody in class_body.body:
                        
                        if isinstance(cbody,ast.FunctionDef):
                            #print(ast.get_docstring(cbody))

                            temp = Function()
                            temp.code = ast.get_docstring(cbody)
                            new_func_ptrs.append(temp)
                            _dec = None
                            _call_class = ""


                            rtns = cbody.returns
                            if rtns:
                                temp.returns = rtns.id
                            else:
                                temp.returns = None
                    
                            for dec in cbody.decorator_list:
                                #print(dec.__dict__)
                                if isinstance(dec,ast.Call):
                                    _dec = dec.func.id
                                else:
                                    _dec = dec.id
                                if _dec:
                                    #print(_dec)
                                    temp.decs.append(_dec)
                                    if _dec == 'callback':
                                        func_pointers.append(temp)
                                    elif _dec == 'call_args':
                                        for arg in dec.args:
                                            #print(arg.id)
                                            temp.call_args.append(arg.id)
                                    elif _dec == "call_class":
                                        #print("call_class:",dec.args[0].id)
                                        temp.call_class = dec.args[0].id
                                        _call_class = dec.args[0].id
                                    elif _dec == "call_target":
                                        #print("call_target:",dec.args[0].id)
                                        temp.call_target = dec.args[0].id
                                        
                                    
                                
                            if not _dec:
                                send_functions.append(temp)
                            temp.name = cbody.name

                            func_arg_list = []

                            for i,_arg in enumerate(cbody.args.args):
                    
                                
                                func_arg = Arg()
                                temp.args_.append(func_arg)
                                func_arg.objc_name = "arg%d" % i
                                func_arg.call_name = _arg.arg

                                func_arg.python_name = _arg.arg
                                func_arg.cy_name = _arg.arg

                                if not isinstance(_arg.annotation,ast.Call):
                                    arg_type = _arg.annotation.id
                                    func_arg.is_list = False
                                    func_arg.python_type = python_types_dict[arg_type]
                                    func_arg.cy_type = ctypedef_types_dict[arg_type]

                                    func_arg.objc_type = typedef_types_dict[arg_type]

                                    func_arg_list.append(_arg.annotation.id)
                                    temp.arg_types.append(_arg.annotation.id)
                                    temp.python_args.append(python_types_dict[_arg.annotation.id])
                                    if arg_type == "json":
                                        func_arg.is_json = True
                                else:
                                    #### Call (list type)####
                                    arg_type = _arg.annotation.args[0].id
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
                                    list_counter.objc_type = "long"
                                    list_counter.objc_name = "arg%d_size" % i
                        
                                    if _dec == 'callback':
                                        
                                        func_arg_list.append("arg%d_size" % i)
                                        temp.args.append("arg%d_size" % i)
                                        temp.arg_names.append("%s_size" % _arg.arg)
                                        func_arg_list.append("long")
                                        temp.arg_types.append("long")
    
                            for child in cbody.body:

                                if isinstance(child,ast.Expr):
                                    item: Expr = child

                                    temp.callback = item.value.s

            if isinstance(class_body,ast.ClassDef):
                pass
        
        ptr_compare = []
        ptr_types2 = []
        for func in new_func_ptrs:
            rtns = func.returns
            if 'callback' in func.decs:

                _arg: Arg
                compare =  []
                for _arg in func.args_:
                    compare.append(_arg.cy_type)
                if len(compare) != 0:
                    if (compare,rtns) not in ptr_compare:
                        ptr_compare.append((compare,rtns))
                        zip_arg = tuple(zip(compare,func.args))
                        ptr_types2.append(func)
                else:
                    if ([],rtns) not in ptr_compare:
                        ptr_compare.append(([],rtns))
                        zip_arg = tuple(zip(compare,func.args))
                        ptr_types2.append(func)

            
        for func in send_functions:
            real_arg = tuple(zip(func.arg_types,func.args))
            name = func.name

            _real_arg = list(dict.fromkeys(real_arg))
            func.real_args = real_arg

        return (func_pointers,send_functions,ptr_types2)

    def gen_cyfunction_pointers(self, func_list,ptr_types,objc=True):
                
        #ptr_types = []
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
                obj_point = objc_func_pointer_string2.format(title="%s_ptr%d" % (calltitle.lower(),count), args=types_str, returns=_rtns)
            else:
                obj_point = func_pointer_string2.format(title="%s_ptr%d" % (calltitle.lower(),count), args=types_str, returns=_rtns)
            function_pointers.append(obj_point)

            for real_func in func_list:
                if [arg.cy_type for arg in real_func.args_ ] == [arg.cy_type for arg in func.args_ ]:
                    real_func.func_ptr = "%s_ptr%d" % (calltitle.lower(),count)

            count += 1
        return function_pointers

    def gen_c_struct(self, pointers:list):
        cython_struct = "\tctypedef struct %sCallback:" % calltitle
        struct_strings = [cython_struct]
        func: Function
        for func in pointers:
            string = "\t\t%s %s" % (func.func_ptr,func.name)
            struct_strings.append(string)

        return "\n".join(struct_strings)

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

    def gen_objc_struct(self, pointers:list):
        cython_struct = "typedef struct %sCallback {" % calltitle
        struct_strings = [cython_struct]
        func: Function
        for func in pointers:
            if func.returns:
                rtns = func.returns
            else:
                rtns = "void"
            string = "\t%s _Nonnull %s;" % (func.func_ptr,func.name)
            struct_strings.append(string)
        struct_strings.append("} %sCallback;" % calltitle)
        return "\n".join(struct_strings)

    def fill_cstruct(self, pointers:list):
        assign_struct = "\t\tcdef %sCallback callbacks = [" % calltitle

        assign_strings = [assign_struct]
        size = len(pointers) -1
        for i,func in enumerate(pointers):
            if i != size:
                string = "\t\tcy_%s," % (func.name)
            else:
                string = "\t\tcy_%s" % (func.name)
            assign_strings.append(string)
        assign_strings.append("\t\t]")
        assign_export_struct = "\n\t".join(assign_strings)
        
        
        return assign_export_struct

    def gen_cython_class(self, title:str,call_var:str,fill_struct:str):
        class_list = []
        class_list.append(cython_class.format(_class=title,call_var=call_var) )
        class_list.append(fill_struct )
        class_list.append("\t\tSend%sCallback(callbacks)" % calltitle )
        
        return "\n".join(class_list)

    def gen_send_args(self, func_arg:Arg):
        #arg_type = func_arg.cy_type
        if func_arg.is_list:
            arg_size = arg_size_dict[func_arg.list_type]
            if func_arg.list_type == "str":
                decode = "<bytes>"#".encode('utf-8')"
                array_line = strlist_2_array.format(
                    arg = func_arg.cy_name,
                    arg_type = ptr_type_dict[func_arg.list_type],
                    type_size = arg_size,
                    decode = decode
                )
            else:
                decode = ""
                array_line = list_2_array.format(
                    arg = func_arg.cy_name,
                    arg_type = ptr_type_dict[func_arg.list_type],
                    type_size = arg_size,
                    decode = decode
                )
            return array_line
        else: 
            #return send_args_dict[func_arg.python_type].format(arg=func_arg.python_name)
            return None

    def gen_cyfunc_sends(self, func:Function,args,args2,rtn,has_args=False):
        title = func.name

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
                        args2_list.append(send_args_dict["json"].format(arg=_arg.python_name) )
                    else:
                        args2_list.append(send_args_dict[_arg.python_type].format(arg=_arg.python_name) )
                    
        if rtn:
            if rtn == 'str':
                if has_args:
                    call = "return {title}({args2}).decode('utf8')".format(title=title, args2= ", ".join(args2_list))
                else:
                    call = "return {title}().decode('utf8')".format(title=title)
            else:
                if has_args:
                    call = "return {title}({args2})".format(title=title, args2= ", ".join(args2_list))
                else:
                    call = "return {title}()".format(title=title)
        else:
            if has_args:
                call = "{title}({args2})".format(title=title, args2= ", ".join(args2_list))
            else:
                call = "{title}()".format(title=title)


        ###### body #####
        body_list = []
        func:Function
        for i, arg in enumerate(func.args_):
            if arg is not "PythonCallback":
                _arg = self.gen_send_args(arg)
                if _arg:
                    #type_size = arg_size_dict[_type]
                    body_list.append(_arg)
               
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


    def gen_send_functions(self, pointers:list,objc=False,subtitle=None,header=False):
        for i in range(len(pointers)):
            ptr:Function = pointers[i]
            print(ptr.name)
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
                    if arg.python_name is "":
                        send_arg = arg.objc_name
                    else:
                        send_arg = arg.python_name
                    if ie != 0:
                        tmp_str = objc_arg.format(t=arg.objc_type, arg=send_arg)
                    else:
                        tmp_str = objc_arg_first.format(t=arg.objc_type, arg=send_arg)
                    objc_arg_tmp.append(tmp_str)
                    #objc_arg_tmp.append(arg.objc_name)

                args2_str = " ".join(objc_arg_tmp)
                
                if header:
                    sfunctions.append( ext_objcfunc_h.format(title=func.name, args=types_str, returns=_rtns) )
                else:
                    if rtns is not None:
                        if len(func.args_) != 0:
                            sfunctions.append( ext_objcfunc_m_rtn.format(title=func.name, args=types_str, args2=args2_str ,subtitle = subt, returns=_rtns) )
                        else:
                            sfunctions.append( ext_objcfunc_m_rtn_noarg.format(title=func.name, args=types_str, subtitle = subt, returns=_rtns) )
                    else:
                        if len(func.args_) != 0:
                            sfunctions.append( ext_objcfunc_m.format(title=func.name, args=types_str, args2=args2_str ,subtitle = subt, returns=_rtns) )
                        else:
                            sfunctions.append( ext_objcfunc_m_noarg.format(title=func.name, args=types_str, subtitle = subt, returns=_rtns) )
            else:
                types_str = ", ".join(types_list)
                if header:
                    #for arg in func.args_:
                    types_str = ", ".join([" ".join((arg.cy_type,arg.cy_name)) for arg in func.args_])
                    sfunctions.append( ext_cyfunc.format(title=func.name, args=types_str ,returns=_rtns) )
                else:
                    sfunctions.append( self.gen_cyfunc_sends(func,types_list,", ".join(args2),func.returns,len(func.args_) != 0) )

            
        if not header and not objc:
            del sfunctions[0]
        return "\n".join( sfunctions )

    def gen_cython_callbacks(self, pointers:list):
        cy_functions = []
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
            call_arg: Arg
            _call_class = func.call_class
            for call_arg in func.args_:
                if _call_class != call_arg.python_name:
                    if call_arg.is_list:
                        call_args.append(call_list_dict[call_arg.list_type].format(arg=call_arg.objc_name))
                    else:
                        if not call_arg.is_counter:
                            if call_arg.is_json:
                                #print("json arg:",call_arg.python_name)
                                arg_name = call_args_dict["json"].format(arg=call_arg.objc_name)
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
                call = _title
            if func.code:
                code = func.code.replace("\n","\n\t") #+ callback
                
                s = cython_callback3.format(title=_title,call=call,callback=callback,args = args_str,_class=func.call_class,returns=_rtns,code=code)
            else:
                s = cython_callback2.format(title=_title,call=call,callback=callback,args = args_str,_class=func.call_class,returns=_rtns)
            cy_functions.append(s)
        
        return "".join(cy_functions)

    def gen_structtype_init_funct(self, title:str, objc=False):
        if objc:
            return objc_structinit_string.format(title=title,call=title)
        else:
            return c_structinit_string.format(title=title,call=title)

    def gen_objc_m_header(self, title):
        return m_header_string.format(title=title)

    def gen_objc_protocol(self, pointers:list,title):
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
            "title": calltitle,
            "depends": None,
            "classname": class_name,
            "dirname": class_name,
            "type": "",
            "build_path": os.path.dirname(__file__)

        }
        
        _mfile = {
            
            "module_name" : "RealmDatabase",

            "root_name" : "",

            "module_folder" : None,

            "module_name_as_root" : True ,

            "pythonlinkroot" : os.path.dirname(__file__)


        }


        # try:
        #with open("./builds/%s/module.ini" % class_name, 'w') as configfile:
        
        if not os.path.exists(join(root_path,"builds",class_name)):
            os.mkdir(join(root_path,"builds",class_name))
        with open(join(root_path,"builds",class_name,"module.ini"), 'w') as configfile:
            configfile.write(json.dumps([class_name,_tmp],indent=4))
            #configfile.close()

        

        #json.dump(_mfile,join(root_path,"builds",class_name,"module_name.json"))
        kivy_recipe_path = "/Volumes/WorkSSD/kivy-ios-11.04.20_copy/recipes/kivytest"
        with open(join(root_path,"builds",class_name,"module_name.json"), 'w') as module_file:
            json.dump(_mfile,module_file)
        shutil.copy(join(root_path,"builds",class_name,"module_name.json"),join(kivy_recipe_path))
        #     for key,value in _tmp.items():
        #         module_file.write("{0} = \"{1}\"\n".format(key,value))
        # except:
        #     pass

    ##############################################################
    ############# Builder ########################################
    ##############################################################

    def build_py_files(self,script):
        global cstruct_list
        cstruct_list = []

        #script = sys.argv[2]
        pyfile = open("{}".format(script), "r" )
        test = pyfile.read()

        functions = self.parse_code(test)
        func_pointers,send_functions,ptr_types = functions

        pointer_types = []
        c_pointers = self.gen_cyfunction_pointers(func_pointers,ptr_types,False)

        objc_pointer_types = []
        objc_pointers = self.gen_cyfunction_pointers(func_pointers,ptr_types,True)
        BUILD_DIR = join(root_path,"builds")
        try:
            os.mkdir(BUILD_DIR)
            #os.mkdir("builds/%s" % calltitle.lower())
        except:
            print("builds exist")
        try:
            os.mkdir(join(BUILD_DIR,calltitle.lower()))
        except:
            print("builds/%s exist" % calltitle.lower())
        f = open(join(BUILD_DIR,calltitle.lower(),calltitle.lower()+"_cy.pyx"), "w+")
        cy_list = [
            "import json",
            "from libc.stdlib cimport malloc, free",
            "from libcpp cimport bool as bool_t",
            "cdef extern from \"%s.h\":" % calltitle.lower(),
            "\t\n".join([self.gen_c_struct_custom(arg[0],arg[1]) for arg in cstruct_list]),
            "",
            "\t######## cdef extern Callback Function Pointers: ########",
            "\t" + "\t".join(c_pointers ),
            "",
            "\t######## cdef extern Callback Struct: ########",
            self.gen_c_struct(func_pointers),
            "",
            #self.gen_structtype_init_funct(calltitle,False) ,
            "\t######## cdef extern Send Functions: ########\n",
            self.gen_send_functions(send_functions,False,None,True),
            "",
            "######## Callbacks Functions: ########\n",
            self.gen_cython_callbacks(func_pointers),
            "######## Cython Class: ########",
            self.gen_cython_class(calltitle,calltitle + "_voidptr",self.fill_cstruct(func_pointers)) ,
            "",
            "######## Send Functions: ########",
            self.gen_send_functions(send_functions,False)
        ]
        
        #f.write(fill_cstruct(c_pointers))
        cy_script = "\n".join(cy_list)
        f.write(cy_script)
        f.write("\n")
        f.close()

        objc_hlist = []
        
        objc_hlist.append("#import <Foundation/Foundation.h>\n")
        objc_hlist.append("\n".join([self.gen_c_struct_custom(arg[0],arg[1],True) for arg in cstruct_list]))
        objc_hlist.append("\n")
        objc_hlist.append("//######## cdef extern Callback Function Pointers: ########//\n")
        objc_hlist.append("".join(objc_pointers ) )
        objc_hlist.append("\n")
        objc_hlist.append("//######## cdef extern Callback Struct: ########//\n")
        objc_hlist.append(self.gen_objc_struct(func_pointers))
        objc_hlist.append("\n\n")
        #objc_hlist.append(self.gen_structtype_init_funct(calltitle,True) )
        objc_hlist.append("\n")
        objc_hlist.append("//######## cdef extern Send Functions: ########//\n")
        objc_hlist.append(self.gen_objc_protocol(send_functions,calltitle))
        objc_hlist.append("\n")
        objc_hlist.append("//######## Send Functions: ########//\n")
        objc_hlist.append(self.gen_send_functions(send_functions,True,None,True))

        objc_hscript = "".join(objc_hlist)
        f = open(join(BUILD_DIR,calltitle.lower(),calltitle.lower()+".h"), "w+")
        f.write(objc_hscript)
        f.close()

        f = open(join(BUILD_DIR,calltitle.lower(),calltitle.lower()+".m"), "w+")
        f.write(self.gen_objc_m_header(calltitle.lower()))
        f.write("\n")
        f.write(self.gen_send_functions(send_functions,True,calltitle))

        f.close()

        self.gen_module_file(calltitle.lower())

        return (cy_script,objc_hscript)

kivy_folder = "/Volumes/WorkSSD/kivy-ios-11.04.20_copy/"
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
        subprocess.call(['python3.7',"%s/toolchain.py" % kivy_folder, "clean", calltitle])
        subprocess.call(['python3.7',"%s/toolchain.py" % kivy_folder, "build", calltitle])
        remove_cache_file(kivy_folder+".cache/"+calltitle+"-master.zip")

        

         
    elif t == "compile_all":
        pack_all("PythonSwiftLink-main.zip",kivy_folder + ".cache/")
        subprocess.call(['python3.7',"%s/toolchain.py" % kivy_folder, "clean", "PythonSwiftLink"])
        subprocess.call(['python3.7',"%s/toolchain.py" % kivy_folder, "build", "PythonSwiftLink"])
         
#(<object> classtest).func0(test.decode('utf-8'),test2)
#[test[x] for x in range(test_count)]