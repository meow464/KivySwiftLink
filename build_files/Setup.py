#!/usr/bin/env python
# -*- coding: utf-8 -*-
#cython: language_level=3
import os
from setuptools import setup, find_packages, Extension
from files_list import open_config
from copy import deepcopy
from os.path import dirname, join, sep
from os import environ
import json

src_path = build_path = dirname(__file__)

def read(file_path):
    with open(file_path) as fp:
        return fp.read()

def determine_base_flags():
    flags = {
        'include_dirs': [],
        'library_dirs': [],
        'extra_link_args': [],
        'extra_compile_args': []}

    sysroot = environ.get('IOSSDKROOT', environ.get('SDKROOT'))
    if not sysroot:
        raise Exception('IOSSDKROOT is not set')
    flags['include_dirs'] += [sysroot]
    flags['extra_compile_args'] += ['-isysroot', sysroot]
    flags['extra_link_args'] += ['-isysroot', sysroot]

    return flags

def merge(d1, *args):
    d1 = deepcopy(d1)
    for d2 in args:
        for key, value in d2.items():
            value = deepcopy(value)
            if key in d1:
                d1[key].extend(value)
            else:
                d1[key] = value
    return d1

def expand(root, *args):
    return join(root, *args)

class CythonExtension(Extension):

    def __init__(self, *args, **kwargs):
        Extension.__init__(self, *args, **kwargs)
        self.cython_directives = {
            'c_string_encoding': 'utf-8',
            'profile': 'USE_PROFILE' in environ,
            'embedsignature': 'USE_EMBEDSIGNATURE' in environ}
        # XXX with pip, setuptools is imported before distutils, and change
        # our pyx to c, then, cythonize doesn't happen. So force again our
        # sources
        self.sources = args[1]

def get_extensions_from_sources(sources):
    _ext_modules = []
    for pyx, flags in sources.items():
        module_name = flags.pop('module_name')
        pyx = expand(src_path,pyx)
        depends = [expand(src_path, x) for x in flags.pop('depends', [])]
        f_depends = [x for x in depends if x.rsplit('.', 1)[-1] in ('m')]
        c_depends = [expand(src_path, x) for x in flags.pop('c_depends', [])]
        #module_name = 'PythonSwiftLink'
        #module_name = m_name
        flags_clean = {'depends': depends}
        for key, value in flags.items():
            if len(value):
                flags_clean[key] = value
        _ext_modules.append(CythonExtension(
            module_name, [pyx] + f_depends + c_depends, **flags_clean))
    return _ext_modules

sources = {}
ext_modules = []
src_path = build_path = dirname(__file__)
base_flags = determine_base_flags()

modules_path = dirname(os.path.abspath(__file__))
cfg = open_config(modules_path)
file_list = cfg.items()
for key,_file in file_list: 
    if key != "DEFAULT":
        print("_deps",_file['depends'])
        _deps = _file['depends']

        _t = _file['type']
        _classname = _file['classname']
        _filename = _file['dirname']

        if _t != "custom":
            osx_flags = {
                'extra_link_args': [],
                'extra_compile_args': ['-ObjC','-w'],
                # 'depends': ['%s.m' % _filename,'%s.h' % _filename]}
                'depends': ['_%s.m' % _filename,'_%s.h' % _filename]}
            sources['%s.pyx' % _filename] = merge(base_flags, osx_flags)
            sources['%s.pyx' % _filename]['module_name'] = '%s' % _filename
        else:
            osx_flags = {
                'extra_link_args': [],
                'extra_compile_args': ['-ObjC','-w'],
                'depends': _deps}
            print('%s.pyx' % (_filename))
            sources['%s.pyx' % _filename] = merge(base_flags, osx_flags)
            sources['%s.pyx' % _filename]['module_name'] = _classname

ext_modules.extend(get_extensions_from_sources(sources))

setup(
      name='PythonSwiftLink',
      version='0.1',
      description="A Cython wrapper for Objc/Swift",
      classifiers=[
                   'Development Status :: 1 - Development',
                   'Intended Audience :: Developers',
                   'Natural Language :: English',
                   'Operating System :: iOS',
                   'Programming Language :: Cython / Objective-C / Swift',
                   'Programming Language :: Python :: 3.8',
                   'Topic :: Payment Processing',
                   ],
      keywords=['PythonSwiftLink'],
      author='PsycHoWasP / GoBig87 ',
      author_email='add_later@add)later.com',
      url='',
      license='BSD',
      packages=find_packages(where='.', exclude=['docs', 'tests']),
      ext_modules=ext_modules,
      include_package_data=True,
      zip_safe=False,
      setup_requires=[
                      'setuptools',
                      ],

      )