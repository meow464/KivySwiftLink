from toolchain import CythonRecipe, shprint
from os.path import join
from distutils.dir_util import copy_tree
from .module_name import *
import fnmatch
import sh
import os
import urllib.parse

class KivySwiftLinkRecipe(CythonRecipe):
    version = "master"
    url = 'file://' + urllib.parse.quote(join(pythonlinkroot + "Exports" + module_name +"-master.zip"))
    library = "temp.a"
    depends = ["python3", "hostpython3"]
    pre_build_ext = True
    archs = ['x86_64','arm64','arm64e','armv7','armv7s']

    def install(self):
        pass
        arch = list(self.filtered_archs)[0]
        build_dir = join(self.get_build_dir(arch.arch), 'build', 'lib.macosx-10.14-x86_64-3.7')
        filename = '__init__.py'
        with open(os.path.join(build_dir, filename), 'wb'):
            pass
        #dist_dir  = join(self.ctx.dist_dir, 'root', 'python3', 'lib', 'python3.7', 'site-packages', 'noke')
        build_path = ['root', 'python3', 'lib', 'python3.7', 'site-packages']
        if module_folder != '' and module_folder != None:
            build_path.append(module_name)

        dist_dir  = join(self.ctx.dist_dir, *build_path)
        copy_tree(build_dir, dist_dir)

    def biglink(self):
        dirs = []
        for root, dirnames, filenames in os.walk(self.build_dir):
            if fnmatch.filter(filenames, "*.so.*"):
                dirs.append(root)
            if fnmatch.filter(filenames, "*.o.*"):
                dirs.append(root)
        cmd = sh.Command(join(self.ctx.root_dir, "tools", "biglink"))
        shprint(cmd, join(self.build_dir, "temp.a"), *dirs)

recipe = KivySwiftLinkRecipe()