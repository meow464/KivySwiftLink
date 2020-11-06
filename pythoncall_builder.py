import parser
import ast
from ast import *
import astor
from pprint import pprint
import re
import sys
import os
import subprocess
from build_files.pack_files import pack_all
import configparser
import json

print(os.path.basename(sys.argv[0]))
print(os.path.dirname(sys.argv[0]))
root_path = os.path.dirname(sys.argv[0])



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
    "int_list": "const int*",
    "long_list": "const long*",
    "uint8_list": "const unsigned char*",
    "float_list": "const float*",
    "double_list": "const double*",
    "str_list": "const char* const*",

    "str": "const char*",
    "int": "int",
    "float": "float",
    "long": "long",

    "PythonCallback": "PythonCallback"
}

typedef_types_dict = {
    "int_list": "const int* _Nonnull",
    "long_list": "const long* _Nonnull",
    "uint8_list": "const unsigned char* _Nonnull",
    "float_list": "const float* _Nonnull",
    "double_list": "const double* _Nonnull",
    "str_list": "const char* _Nonnull const* _Nonnull",

    "str": "const char* _Nonnull",
    "int": "int",
    "float": "float",
    "long": "long",

    "PythonCallback": "PythonCallback"
}

python_types_dict = {
    "int_list": "list",
    "long_list": "list",
    "uint8_list": "list",
    "float_list": "list",
    "double_list": "list",
    "str_list": "list",

    "str": "str",
    "int": "int",
    "float": "float",
    "long": "int",

    "PythonCallback": "PythonCallback"
}

call_args_dict = {
    "int_list": "[{arg} for x in range({arg}_count)]",
    "long_list": "[{arg} for x in range({arg}_count)]",
    "uint8_list": "[{arg} for x in range({arg}_count)]",
    "float_list": "[{arg} for x in range({arg}_count)]",
    "double_list": "[{arg} for x in range({arg}_count)]",
    "str_list": "[{arg}.decode('utf8') for x in range({arg}_count)]",

    "str": "{arg}.decode('utf8')",
    "int": "{arg}",
    "float": "{arg}",
    "long": "{arg}",

    "PythonCallback": "PythonCallback"
}

arg_size_dict = {
        "int_list": 4,
        "long_list": 8,
        "uint8_list": 1,
        "float_list": 4,
        "double_list": 8,
        "str_list": 1,

        "str": 1,
        "int": 4,
        "float": 4,
        "long": 8,
    }
cython_class = """\
cdef public void* classtest
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
\tdef {title}(self,{args}):
\t\treturn {title}({args2})
"""

class_cyfunc_send_rtn_noargs = """\
\tdef {title}(self,{args}):
\t\treturn {title}()
"""

class_cyfunc_send_plain = """\
\tdef {title}(self,{args}):
{body}
\t\t{call}
"""

call_args_dict = {
    "int_list": "[{arg} for x in range({arg}_count)]",
    "long_list": "[{arg} for x in range({arg}_count)]",
    "uint8_list": "[{arg} for x in range({arg}_count)]",
    "float_list": "[{arg} for x in range({arg}_count)]",
    "double_list": "[{arg} for x in range({arg}_count)]",
    "str_list": "[{arg}.decode('utf8') for x in range({arg}_count)]",

    "str": "{arg}.decode('utf8')",
    "int": "{arg}",
    "float": "{arg}",
    "long": "{arg}",

    "PythonCallback": "PythonCallback"
}

arg_size_dict = {
        "int_list": 4,
        "long_list": 8,
        "uint8_list": 1,
        "float_list": 4,
        "double_list": 8,
        "str_list": 1,

        "str": 1,
        "int": 4,
        "float": 4,
        "long": 8,
    }

ptr_type_dict = {
        "int_list": "int",
        "long_list": "long",
        "uint8_list": "unsigned char",
        "float_list": "float",
        "double_list": "double",
        "str_list": "const char",

        "str": "str",
        "int": "int",
        "float": "float",
        "long": "long",
    }

list_2_array =  """\
\t\tcdef int {arg}_size = len({arg})
\t\tcdef {arg_type} *{arg}_array = <{arg_type} *> malloc({arg}_size  * {type_size})
\t\tcdef int {arg}_i
\t\tfor {arg}_i in range({arg}_size):
\t\t\t{arg}_array[{arg}_i] = {arg}[{arg}_i]
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
\t(<object> {_class}).{title}{callback}

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


class Function():
    args: list
    args2: list
    arg_types: list
    arg_names: list
    real_args: list
    real_args2: list
    python_args: list
    python_arg_names: list
    returns: str
    name: str
    callback: str
    func_ptr: str


    def __init__(self):
        self.args = []
        self.args2 = []
        self.arg_types = []
        self.real_args = []
        self.real_args2 = []
        self.arg_names = []
        self.python_args = []
        self.python_arg_names = []
        self.returns = None
        self.name = ""
        self.callback = ""
        self.func_ptr = ""

class PythonCallBuilder():

    def get_typedef_types(self,t):
        if t in ["int_list","long_list","uint8_list","float_list","double_list"]:
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
        send.args =  ['callback']
        send.name = 'SendCallback'
        send.real_args = ((calltitle.lower(),'callback')),

        pointers.append(send)

    def parse_code(self, string:str):
        module = ast.parse(string)
        func_pointers = []
        send_functions = []
        
        for _body in module.body:
            if isinstance(_body,ast.Assign):
                pass

            if isinstance(_body,ast.ClassDef):
                global calltitle
                calltitle = _body.name
                self.gen_send_start_function(send_functions)
                for cbody in _body.body:
                    
                    if isinstance(cbody,ast.FunctionDef):
                        temp = Function()
                        _dec = None

                        rtns = cbody.returns
                        if rtns:
                            temp.returns = rtns.id
                        else:
                            temp.returns = None
                
                        for dec in cbody.decorator_list:
                            _dec = dec.id
                        if _dec:
                            if _dec == 'callback':
                                func_pointers.append(temp)
                        else:
                            send_functions.append(temp)
                        temp.name = cbody.name

                        func_arg_list = []
                        # temp.args = []
                        # temp.arg_types = []
                        # temp['arg_names'] = []
                        for i,_arg in enumerate(cbody.args.args):
                            func_arg_list.append("arg%d" % i)
                            temp.args.append("arg%d" % i)
                            temp.arg_names.append(_arg.arg)

                            func_arg_list.append(_arg.annotation.id)
                            temp.arg_types.append(_arg.annotation.id)
                            temp.python_args.append(python_types_dict[_arg.annotation.id])
                            if _arg.annotation.id in ["int_list","long_list","uint8_list","float_list","double_list","str_list"] and _dec == 'callback':
                                func_arg_list.append("arg%d_count" % i)
                                temp.args.append("arg%d_count" % i)
                                temp.arg_names.append("%s_count" % _arg.arg)
                                func_arg_list.append("long")
                                temp.arg_types.append("long")

                        for child in cbody.body:

                            if isinstance(child,ast.Expr):
                                item: Expr = child

                                temp.callback = item.value.s

            if isinstance(_body,ast.ClassDef):
                pass
        
        ptr_types = []
        for func in func_pointers:
            real_arg = tuple(zip(func.arg_types,func.args))
            name = func.name

            _real_arg = list(dict.fromkeys(real_arg))
            rtns = func.returns
            func.real_args = _real_arg

            if (_real_arg,rtns) not in ptr_types:
                ptr_types.append((_real_arg,rtns))
        
            real_arg2 = tuple(zip(func.arg_types,func.arg_names))
            _real_arg2 = list(dict.fromkeys(real_arg2))
            func.real_args2 = _real_arg2

            
        for func in send_functions:
            real_arg = tuple(zip(func.arg_types,func.args))
            name = func.name

            _real_arg = list(dict.fromkeys(real_arg))
            func.real_args = real_arg

        return (func_pointers,send_functions,ptr_types)

    def gen_cyfunction_pointers(self, func_list,ptr_types,objc=True):
                
        #ptr_types = []

        count = 0
        function_pointers = []
        function_pointers2 = []
        for func,rtns in ptr_types:
            print(func)
            point_dict = {"p_args":func}

            types_list = []
            for types in func:
                _types = []
                for i,_type in enumerate(types):
                    if i%2:
                        _types.append(_type)
                    else:
                        if objc:
                            _types.append(typedef_types_dict[_type])
                        else:
                            _types.append(ctypedef_types_dict[_type])
                        
                str0 = " ".join(_types)
                types_list.append(str0)
            types_str = ", ".join(types_list)
            if rtns:
                if objc:
                    _rtns = typedef_types_dict[rtns]
                else:
                    _rtns = ctypedef_types_dict[rtns]
            else:
                _rtns = "void"
            if objc:
                obj_point = objc_func_pointer_string2.format(title="cfunc_ptr%d" % count, args=types_str, returns=_rtns)
            else:
                obj_point = func_pointer_string2.format(title="cfunc_ptr%d" % count, args=types_str, returns=_rtns)
            function_pointers.append(obj_point)
            

            for real_func in func_list:
                #args = real_func[]
                
                real_arg = real_func.real_args
                if real_arg == func:
                    real_func.func_ptr = "cfunc_ptr%d" % count
                
            
            count += 1
        return function_pointers

    def gen_c_struct(self, pointers:list):
        cython_struct = "\tstruct %sStruct:" % calltitle
        struct_strings = [cython_struct]
        func: Function
        for func in pointers:
            string = "\t\t%s %s" % (func.func_ptr,func.name)
            struct_strings.append(string)

        return "\n".join(struct_strings)

    def gen_objc_struct(self, pointers:list):
        cython_struct = "struct %sStruct {" % calltitle
        struct_strings = [cython_struct]
        func: Function
        for func in pointers:
            string = "\t%s _Nonnull %s;" % (func.func_ptr,func.name)
            struct_strings.append(string)
        struct_strings.append("};")
        return "\n".join(struct_strings)

    def fill_cstruct(self, pointers:list):
        assign_struct = "\t\tcdef %sStruct callbacks = [" % calltitle

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
        class_list.append("\t\tSendCallback(callbacks)" )
        
        return "\n".join(class_list)

    def gen_send_args(self, arg,arg_type):
        print("gen_send_args",arg_type)
        if arg_type in ("int_list","int_list","long_list","float_list","double_list","uint8_list"):
            arg_size = arg_size_dict[arg_type]
            array_line = list_2_array.format(
                arg = arg,
                arg_type = ptr_type_dict[arg_type],
                type_size = arg_size,
            )
            return array_line
        else: 
            return None

    def gen_cyfunc_sends(self, func:Function,args,args2,rtn,has_args=False):
        title = func.name
        print("gen_cyfunc_sends",func.arg_types)
        if has_args:
            args2_list = []
            print(func.python_args)
            for i,_type in enumerate(func.python_args):
                #print(func.python_args)
                #args2_list.append(call_args_dict[_type].format(arg=func.args[i]))
                if _type in ("list"):
                    args2_list.append(func.arg_names[i]+"_array")
                else:
                    args2_list.append(func.arg_names[i])
        if rtn:
            if rtn == 'str':
                if has_args:
                    call = "return {title}({args2}).decode('utf8')".format(title=title, args2= args2)
                else:
                    call = "return {title}().decode('utf8')".format(title=title)
            else:
                if has_args:
                    call = "return {title}({args2})".format(title=title, args2= args2)
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
        for i, _type in enumerate(func.arg_types):
            if _type is not "PythonCallback":
                _arg = self.gen_send_args(func.arg_names[i],_type)
                if _arg:
                    #type_size = arg_size_dict[_type]
                    body_list.append(_arg)
                    print(_type)
        p_arg_list = []
        for i,_arg in enumerate(func.python_args):
            print("args",""+_arg,func.arg_names[i])
            p_arg_list.append( ":".join([func.arg_names[i],_arg]))
        
        return class_cyfunc_send_plain.format(title=title,args=", ".join(p_arg_list),call=call, body="\n".join(body_list))


    def gen_send_functions(self, pointers:list,objc=False,subtitle=None,header=False):
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
            for types in func.real_args:
                _types = []
                for i,_type in enumerate(types):

                    if i%2:
                        _types.append(_type)
                        args2.append(_type)
                        types_list2.append(_type)
                    else:
                        if objc:
                            _types.append(typedef_types_dict[_type])
                            types_list2.append(typedef_types_dict[_type])
                            
                        else:
                            _types.append(ctypedef_types_dict[_type])
                        
                str0 = " ".join(_types)
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
                for ie in range(0,len(types_list2),2):
                    if ie != 0:
                        tmp_str = objc_arg.format(t=types_list2[ie], arg=types_list2[ie+1])
                    else:
                        tmp_str = objc_arg_first.format(t=types_list2[ie], arg=types_list2[ie+1])
                    objc_arg_tmp.append(tmp_str)
                args2_str = " ".join(objc_arg_tmp)
                if header:
                    sfunctions.append( ext_objcfunc_h.format(title=func.name, args=types_str, returns=_rtns) )
                else:
                    if rtns is not None:
                        if len(types_list2) != 0:
                            sfunctions.append( ext_objcfunc_m_rtn.format(title=func.name, args=types_str, args2=args2_str ,subtitle = subt, returns=_rtns) )
                        else:
                            sfunctions.append( ext_objcfunc_m_rtn_noarg.format(title=func.name, args=types_str, subtitle = subt, returns=_rtns) )
                    else:    
                        if len(types_list2) != 0:
                            sfunctions.append( ext_objcfunc_m.format(title=func.name, args=types_str, args2=args2_str ,subtitle = subt, returns=_rtns) )
                        else:
                            sfunctions.append( ext_objcfunc_m_noarg.format(title=func.name, args=types_str, subtitle = subt, returns=_rtns) )
            else:
                types_str = ", ".join(types_list)
                if header:
                    sfunctions.append( ext_cyfunc.format(title=func.name, args=types_str ,returns=_rtns) )
                else:
                    sfunctions.append( self.gen_cyfunc_sends(func,types_list,", ".join(args2),func.returns,len(types_list2) != 0) )
                    # if rtns is not None:
                    #     if len(types_list2) != 0:
                    #         sfunctions.append(class_cyfunc_send_rtn.format(title=func.name, args=types_str,args2=args2_str ) )
                    #     else:
                    #         sfunctions.append(class_cyfunc_send_rtn_noargs.format(title=func.name, args=types_str ) )
                    # else:
                    #     if len(types_list2) != 0:
                    #         sfunctions.append( class_cyfunc_send.format(title=func.name, args=types_str ) )
                    #     else:
                    #         sfunctions.append( class_cyfunc_send.format(title=func.name, args=types_str ) )
            
        if not header and not objc:
            del sfunctions[0]
        return "\n".join( sfunctions )

    def gen_cython_callbacks(self, pointers:list):
        cy_functions = []
        for i,func in enumerate(pointers):
            _title = func.name
            args = func.real_args
            types_list = []
            args2 = []
            for types in func.real_args2:
                _types = []
                for i,_type in enumerate(types):
                    if i%2:
                        _types.append(_type)
                        args2.append(_type)
                    else:
                        _types.append(ctypedef_types_dict[_type])
                        
                str0 = " ".join(_types)
                types_list.append(str0)
            args_str = ", ".join(types_list)
            callback = func.callback#.split(".")[-1]
            rtns = func.returns
            if rtns:
                _rtns = ctypedef_types_dict[rtns]
            else:
                _rtns = "void"
            s = cython_callback2.format(title=_title,callback=callback,args = args_str,_class="classtest",returns=_rtns)
            cy_functions.append(s)
        
        return "".join(cy_functions)

    def gen_structtype_init_funct(self, title:str, objc=False):
        if objc:
            return objc_structinit_string.format(title=title,call=title.lower())
        else:
            return c_structinit_string.format(title=title,call=title.lower())

    def gen_objc_m_header(self, title):
        return m_header_string.format(title=title)

    def gen_objc_protocol(self, pointers:list,title):
        sfunctions = []
        sfunctions.append(protocol_start.format(title=title))
        for i,func in enumerate(pointers):
            
            types_list = []
            args2 = []
            arg_types = func.arg_types
            args = func.args
            for x in range(len(arg_types)):
                if x != 0:
                    types_list.append(protocol_arg.format(type=typedef_types_dict[arg_types[x]],arg=args[x]))
                else:
                    types_list.append(protocol_first_arg.format(type=typedef_types_dict[arg_types[x]],arg=args[x]))


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
            "depends": None,
            "classname": class_name,
            "dirname": class_name,
            "type": ""
        }
        
        # try:
        with open("./builds/%s/module.ini" % class_name, 'w') as configfile:
            configfile.write(json.dumps([class_name,_tmp],indent=4))
            configfile.close()
        # except:
        #     pass

    ##############################################################
    ############# Builder ########################################
    ##############################################################

    def build_py_files(self):
        script = sys.argv[2]
        pyfile = open("{}".format(script), "r" )
        test = pyfile.read()

        functions = self.parse_code(test)
        func_pointers,send_functions,ptr_types = functions

        pointer_types = []
        c_pointers = self.gen_cyfunction_pointers(func_pointers,ptr_types,False)

        objc_pointer_types = []
        objc_pointers = self.gen_cyfunction_pointers(func_pointers,ptr_types,True)

        try:
            os.mkdir("builds")
            #os.mkdir("builds/%s" % calltitle.lower())
        except:
            print("builds exist")
        try:
            os.mkdir("builds/%s" % calltitle.lower())
        except:
            print("builds/%s exist" % calltitle.lower())
        f = open("builds/{0}/{0}_cy.pyx".format(calltitle.lower()), "w+")

        f.write("import json\n")
        f.write("from libc.stdlib cimport malloc, free\n")

        f.write("cdef extern from \"%s.h\":\n\t" % calltitle.lower())
        f.write("\t".join(c_pointers ) ) 
        f.write("\n")
        f.write(self.gen_c_struct(func_pointers))
        f.write("\n\n")
        f.write(self.gen_structtype_init_funct(calltitle,False) )
        f.write("\n")
        f.write(self.gen_send_functions(send_functions,False,None,True))
        f.write("\n\n")
        f.write(self.gen_cython_callbacks(func_pointers))
        f.write(self.gen_cython_class(calltitle,"classtest",self.fill_cstruct(func_pointers)) )
        f.write("\n\n")
        f.write(self.gen_send_functions(send_functions,False))
        
        #f.write(fill_cstruct(c_pointers))

        f.write("\n")
        f.close()


        f = open("builds/{0}/{0}.h".format(calltitle.lower()), "w+")
        f.write("#import <Foundation/Foundation.h>\n")
        f.write("".join(objc_pointers ) )
        f.write("\n")
        f.write(self.gen_objc_struct(func_pointers))
        f.write("\n\n")
        f.write(self.gen_structtype_init_funct(calltitle,True) )
        f.write("\n")
        f.write(self.gen_objc_protocol(send_functions,calltitle))
        f.write("\n")
        f.write(self.gen_send_functions(send_functions,True,None,True))

        #f.write("Now the file has more content!")
        f.close()

        f = open("builds/{0}/{0}.m".format(calltitle.lower()), "w+")
        f.write(self.gen_objc_m_header(calltitle.lower()))
        f.write("\n")
        f.write(self.gen_send_functions(send_functions,True,calltitle))

        f.close()

        self.gen_module_file(calltitle.lower())

kivy_folder = "/Volumes/WorkSSD/kivy-ios-11.04.20_copy/"
if __name__ == '__main__':
    p_build = PythonCallBuilder()
    t = sys.argv[1]
    if t == "build":
        p_build.build_py_files()
    elif t == "compile_all":
        pack_all("PythonSwiftLink-main.zip",kivy_folder + ".cache/")
        subprocess.call(['python3.7',"%s/toolchain.py" % kivy_folder, "clean", "PythonSwiftLink"])
        subprocess.call(['python3.7',"%s/toolchain.py" % kivy_folder, "build", "PythonSwiftLink"])
         
#(<object> classtest).func0(test.decode('utf-8'),test2)
#[test[x] for x in range(test_count)]