from ctypes import c_double, c_int, c_int16, c_long, c_longdouble, c_longlong, c_short, c_uint16, c_ulong, c_ulonglong
from ctypes import c_uint8
from ctypes import c_uint8
from ctypes import c_int8 
from ctypes import c_uint
from ctypes import c_long
from typing import List,Tuple
#from ctypes import c_int8 as
long = c_long
ulong = c_ulong
longlong = c_longlong
ulonglong = c_ulonglong
uint8 = c_uint8
short = c_int16
int16 = c_int16
ushort = c_uint16
uint16 = c_uint16
data = c_uint8
json = c_int8
uint = c_uint
double = c_double
longdouble = c_longdouble

__all__ = [
    "long",
    "ulong",
    "longlong",
    "ulonglong",
    "uint8",
    "short",
    "int16",
    "ushort",
    "uint16",
    "data",
    "json",
    "uint",
    ## other types
    "List",
    "Tuple",
    "callback",
    "EventDispatcher"
    ]

def callback(*args):
    pass

def EventDispatcher(events: dict):
    pass