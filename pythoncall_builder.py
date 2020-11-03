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

def get_typedef_types(t):
    if t in ["int_list","long_list","uint8_list","float_list","double_list"]:
        pass
    else: 
        return i 


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





def gen_send_start_function(pointers:list):
    typedef_types_dict['PythonCallback'] = calltitle.lower()
    ctypedef_types_dict['PythonCallback'] = calltitle.lower()
    send = {
        'arg_types' : ['PythonCallback'],
        'args' : ['callback'],
        'name' : 'SendCallback',
        'real_args' : ((calltitle.lower(),'callback')),
        'returns' : None

    }
    pointers.append(send)

def parse_code(string:str):
    module = ast.parse(string)
    func_pointers = []
    send_functions = []
    

    for _body in module.body:

        if isinstance(_body,ast.Assign):
            pass

        if isinstance(_body,ast.ClassDef):
  
            global calltitle
            calltitle = _body.name
            gen_send_start_function(send_functions)
            for cbody in _body.body:
                
                if isinstance(cbody,ast.FunctionDef):
                    temp = {}
                    _dec = None

                    rtns = cbody.returns
                    if rtns:
                        temp['returns'] = rtns.id
                    else:
                        temp['returns'] = None
               
                    for dec in cbody.decorator_list:
                        _dec = dec.id
                    if _dec:
                        if _dec == 'callback':
                            func_pointers.append(temp)
                    else:
                        send_functions.append(temp)
                    temp['name'] = cbody.name

                    func_arg_list = []
                    temp['args'] = []
                    temp['arg_types'] = []
                    temp['arg_names'] = []
                    for i,_arg in enumerate(cbody.args.args):
                        func_arg_list.append("arg%d" % i)
                        temp['args'].append("arg%d" % i)
                        temp['arg_names'].append(_arg.arg)
                        func_arg_list.append(_arg.annotation.id)
                        temp['arg_types'].append(_arg.annotation.id)
                        if _arg.annotation.id in ["int_list","long_list","uint8_list","float_list","double_list","str_list"]:
                            func_arg_list.append("arg%d_count" % i)
                            temp['args'].append("arg%d_count" % i)
                            temp['arg_names'].append("%s_count" % _arg.arg)
                            func_arg_list.append("long")
                            temp['arg_types'].append("long")

                    for child in cbody.body:

                        if isinstance(child,ast.Expr):
                            item: Expr = child

                            temp['callback'] = item.value.s

        if isinstance(_body,ast.ClassDef):
            pass
    
    ptr_types = []
    for func in func_pointers:
        real_arg = tuple(zip(func['arg_types'],func['args']))
        name = func['name']

        _real_arg = list(dict.fromkeys(real_arg))
        rtns = func['returns']
        func['real_args'] = _real_arg

        if not (_real_arg,rtns) in ptr_types:
            ptr_types.append((_real_arg,rtns))
    
        real_arg2 = tuple(zip(func['arg_types'],func['arg_names']))
        _real_arg2 = list(dict.fromkeys(real_arg2))
        func['real_args2'] = _real_arg2

        
    for func in send_functions:
        real_arg = tuple(zip(func['arg_types'],func['args']))
        name = func['name']

        _real_arg = list(dict.fromkeys(real_arg))
        func['real_args'] = real_arg

    return (func_pointers,send_functions,ptr_types)





#########################################################

def gen_cyfunction_pointers(func_list,ptr_types,objc=True):
            
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
            
            real_arg = real_func['real_args']
            if real_arg == func:
                real_func['func_ptr'] = "cfunc_ptr%d" % count
            
        
        count += 1
    return function_pointers

#####################################################


######################################################
def gen_c_struct(pointers:list):
    cython_struct = "\tstruct %sStruct:" % calltitle
    struct_strings = [cython_struct]

    for func in pointers:
        string = "\t\t%s %s" % (func['func_ptr'],func['name'])
        struct_strings.append(string)

    return "\n".join(struct_strings)

def gen_objc_struct(pointers:list):
    cython_struct = "struct %sStruct {" % calltitle
    struct_strings = [cython_struct]

    for func in pointers:
        string = "\t%s _Nonnull %s;" % (func['func_ptr'],func['name'])
        struct_strings.append(string)
    struct_strings.append("};")
    return "\n".join(struct_strings)



def fill_cstruct(pointers:list):
    assign_struct = "\t\tcdef %sStruct callbacks = [" % calltitle

    assign_strings = [assign_struct]
    size = len(pointers) -1
    for i,func in enumerate(pointers):
        if i != size:
            string = "\t\tcy_%s," % (func['name'])
        else:
            string = "\t\tcy_%s" % (func['name'])
        assign_strings.append(string)
    assign_strings.append("\t\t]")
    assign_export_struct = "\n\t".join(assign_strings)
    
    
    return assign_export_struct
cython_class = """\
cdef public void* classtest
cdef class {_class}:
\tdef __init__(self,object _{call_var}):
\t\tglobal {call_var} 
\t\t{call_var} = <void*>_{call_var}
\t\tprint("{call_var} init:", (<object>{call_var}))
"""
def gen_cython_class(title:str,call_var:str,fill_struct:str):
    class_list = []
    class_list.append(cython_class.format(_class=title,call_var=call_var) )
    class_list.append(fill_struct )
    class_list.append("\t\tSendCallback(callbacks)" )
    
    return "\n".join(class_list)

ext_cyfunc = "\t{returns} {title}({args})"

ext_objcfunc_m = """\
{returns} {title}({args}){{
    [{subtitle} {title}:{args2}];
}}
"""
ext_objcfunc_h = """\
{returns} {title}({args});
"""

ext_send_callback = """\
{returns} Init{title}Delegate(<{title_l}Delegate> _Nonnull callback){{
    {subtitle} = callback;
    NSLog(@"setting {title} delegate %@",{subtitle});
}}
"""
ext_send_callback_h = """\
{returns} Init{title}Delegate(<{title_l}Delegate> _Nonnull callback);
"""

def gen_send_functions(pointers:list,objc=False,subtitle=None,header=False):
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
        rtns = func['returns']
        if rtns:
            if objc:
                _rtns = typedef_types_dict[rtns]
            else:
                _rtns = ctypedef_types_dict[rtns]
        else:
            _rtns = "void"

        args2 = []
        for types in func['real_args']:
            _types = []
            for i,_type in enumerate(types):

                if i%2:
                    _types.append(_type)
                    args2.append(_type)
                else:
                    if objc:
                        _types.append(typedef_types_dict[_type])
                        
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
            args2_str = ":".join(args2)
            if header:
                sfunctions.append( ext_objcfunc_h.format(title=func['name'], args=types_str, returns=_rtns) )
            else:
                sfunctions.append( ext_objcfunc_m.format(title=func['name'], args=types_str, args2=args2_str ,subtitle = subt, returns=_rtns) )
        else:
            types_str = ", ".join(types_list)
            if header:
                sfunctions.append( ext_cyfunc.format(title=func['name'], args=types_str ,returns=_rtns) )
            else:
                sfunctions.append( ext_cyfunc.format(title=func['name'], args=types_str ,returns=_rtns) )

    return "\n".join( sfunctions )


cython_callback = """\
cdef void cy_{title}({args}) with gil:
\t(<object> {_class}).{title}{callback}

"""
cython_callback2 = """\
cdef {returns} cy_{title}({args}) with gil:
\t(<object> {_class}).{title}{callback}

"""

def gen_cython_callbacks(pointers:list):
    cy_functions = []
    for i,func in enumerate(pointers):
        _title = func['name']
        args = func['real_args']
        types_list = []
        args2 = []
        for types in func['real_args2']:
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
        callback = func['callback']#.split(".")[-1]
        rtns = func['returns']
        if rtns:
            _rtns = ctypedef_types_dict[rtns]
        else:
            _rtns = "void"
        s = cython_callback2.format(title=_title,callback=callback,args = args_str,_class="classtest",returns=_rtns)
        cy_functions.append(s)
    
    return "".join(cy_functions)





objc_structinit_string = """\
typedef struct {title}Struct {call};

"""

c_structinit_string = """\
\tctypedef {title}Struct {call}

"""


def gen_structtype_init_funct(title:str, objc=False):
    if objc:
        return objc_structinit_string.format(title=title,call=title.lower())
    else:
        return c_structinit_string.format(title=title,call=title.lower())



protocol_start = "@protocol {title}Delegate <NSObject>"
protocol_line_start = "- ({returns}){title}:{args};"
protocol_arg = "{arg}:({type}){arg}"
protocol_first_arg = "({type}){arg}"
protocol_id = "typedef id<{title}Delegate> {title}Delegate;"
protocol_static = "\nstatic <{title}Delegate> _Nonnull {subtitle};"

def gen_objc_protocol(pointers:list,title):
    sfunctions = []
    sfunctions.append(protocol_start.format(title=title))
    for i,func in enumerate(pointers):
        
        types_list = []
        args2 = []
        arg_types = func['arg_types']
        args = func['args']
        for x in range(len(arg_types)):
            if x != 0:
                types_list.append(protocol_arg.format(type=typedef_types_dict[arg_types[x]],arg=args[x]))
            else:
                types_list.append(protocol_first_arg.format(type=typedef_types_dict[arg_types[x]],arg=args[x]))


        arg_string = " ".join(types_list)  
        name = func['name']
        rtns = func['returns']
        if rtns:
            _rtns = typedef_types_dict[rtns]
        else:
            _rtns = "void"
        line = protocol_line_start.format(title=name,args=arg_string, returns= _rtns)
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
    
m_header_string = """\
#import <Foundation/Foundation.h>
#import "{title}.h"
"""
def gen_objc_m_header(title):
    return m_header_string.format(title=title)



##############################################################
############# Builder ########################################
##############################################################

def build_py_files():
    script = sys.argv[2]
    pyfile = open("{}".format(script), "r" )
    test = pyfile.read()

    functions = parse_code(test)
    func_pointers,send_functions,ptr_types = functions

    pointer_types = []
    c_pointers = gen_cyfunction_pointers(func_pointers,ptr_types,False)

    objc_pointer_types = []
    objc_pointers = gen_cyfunction_pointers(func_pointers,ptr_types,True)

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

    f.write("cdef extern from \"%s.h\":\n\t" % calltitle.lower())
    f.write("\t".join(c_pointers ) ) 
    f.write("\n")
    f.write(gen_c_struct(func_pointers))
    f.write("\n\n")
    f.write(gen_structtype_init_funct(calltitle,False) )
    f.write("\n")
    f.write(gen_send_functions(send_functions,False))
    f.write("\n\n")
    f.write(gen_cython_callbacks(func_pointers))
    f.write( gen_cython_class(calltitle,"classtest",fill_cstruct(func_pointers)) )
    #f.write(fill_cstruct(c_pointers))

    f.write("\n")
    f.close()


    f = open("builds/{0}/{0}.h".format(calltitle.lower()), "w+")
    f.write("#import <Foundation/Foundation.h>\n")
    f.write("".join(objc_pointers ) )
    f.write("\n")
    f.write(gen_objc_struct(func_pointers))
    f.write("\n\n")
    f.write(gen_structtype_init_funct(calltitle,True) )
    f.write("\n")
    f.write(gen_objc_protocol(send_functions,calltitle))
    f.write("\n")
    f.write(gen_send_functions(send_functions,True,None,True))

    #f.write("Now the file has more content!")
    f.close()

    f = open("builds/{0}/{0}.m".format(calltitle.lower()), "w+")
    f.write(gen_objc_m_header(calltitle.lower()))
    f.write("\n")
    f.write(gen_send_functions(send_functions,True,calltitle))

    f.close()


kivy_folder = "/Volumes/WorkSSD/kivy-ios-11.04.20_copy/"
if __name__ == '__main__':
    t = sys.argv[1]
    if t == "build":
        build_py_files()
    elif t == "compile_all":
        pack_all("PythonSwiftLink-main.zip",kivy_folder + ".cache/")
        subprocess.call(['python3.7',"%s/toolchain.py" % kivy_folder, "clean", "PythonSwiftLink"])
        subprocess.call(['python3.7',"%s/toolchain.py" % kivy_folder, "build", "PythonSwiftLink"])
         
#(<object> classtest).func0(test.decode('utf-8'),test2)
#[test[x] for x in range(test_count)]