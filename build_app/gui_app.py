from logging import root
from re import search
from kivy.app import App
from kivy.storage import jsonstore
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.lang import *
from kivy.core.window import Window
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.treeview import TreeView,TreeViewLabel,TreeViewNode
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.codeinput import CodeInput
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.storage.dictstore import DictStore
from kivy.storage.jsonstore import JsonStore
from kivy.config import ConfigParser
from kivy.uix.settings import Settings
from kivy.uix.settings import SettingsWithTabbedPanel

from kivy.clock import Clock, mainthread
import json

import sys
import os
from os.path import getmtime, isdir, join,dirname
import subprocess
import shutil
from PythonSwiftLink.pythoncall_builder import PythonCallBuilder
from PythonSwiftLink.build_files.pack_files import pack_all,remove_cache_file
from threading import Thread

from pygments.lexers.objective import ObjectiveCLexer
from pygments.lexers import CythonLexer

from filecmp import cmp,cmpfiles
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler

from pbxproj import XcodeProject,PBXKey
from pbxproj.pbxextensions.ProjectFiles import FileOptions


Window.size = (1920, 1080)
Window.left = 0

dir_path = dirname(__file__)


Builder.load_string("""
<ProjectBuilder>:
    orientation: 'vertical'
    BoxLayout:
        size_hint_y: None
        height: 48
        Button:
            text: "step0"
            on_release:
                project_screen.current = "step0"
        Button:
            text: "step1"
            on_release:
                project_screen.current = "step1"
        Button:
            text: "step2"
            on_release:
                project_screen.current = "step2"
        Button:
            text: "step3"
            on_release:
                project_screen.current = "step3"
        Button:
            text: "step4"
            on_release:
                project_screen.current = "step4"
        Button:
            text: "step5"
            on_release:
                project_screen.current = "step5"
        Button:
            text: "step6"
            on_release:
                project_screen.current = "step6"
        
            
    ScreenManager:
        id: project_screen
        Screen:
            name: "step0"
            FloatLayout:
                BoxLayout:
                    pos_hint: {'center_x': 0.5 , 'center_y': 0.5}
                    size_hint: 0.4, 0.3
                    Label:
                        text: "Add standard files"
                    Button:
                        on_release:
                            app.update_classes_group()

                Button:
                    size_hint: None,None
                    pos_hint: {'right': 1, 'y': 0}
            
        Screen:
            name: "step1"
        Screen:
            name: "step2"
        Screen:
            name: "step3"
        Screen:
            name: "step4"
        Screen:
            name: "step5"
        Screen:
            name: "step6"
""")

class ProjectBuilder(BoxLayout):
    pass

Builder.load_string("""
<MainWindow>:
    orientation: 'vertical'
    BoxLayout:
        size_hint_y: None
        height: 36
        Button:
            text: "Swift/OBJ-C Wrapper Generator"
            on_release:
                screens.current = "screen0"
        Button:
            text: "Settings"
            on_release:
                screens.current = "screen1"
        Button:
            text: "Settings2"
            on_release:
                screens.current = "screen2"
    ScreenManager:
        id: screens
        Screen:
            name: "screen0"
            BoxLayout:
                orientation: 'vertical'
                BoxLayout:
                    id: TopMenu
                    size_hint_y: 0.4
                    BoxLayout:
                        orientation: 'vertical'
                        #BoxLayout:
                            
                        Label:
                            text: "Imported py's"
                            size_hint_y:None
                            height: 24
                        ScrollView:
                            GridLayout:
                                cols: 1
                                #default_row_height: 48
                                id: imports
                                size_hint_y: None
                                height: self.minimum_height
                    BoxLayout:
                        orientation: 'vertical'
                        Label:
                            text: "Builds"
                            size_hint_y:None
                            height: 24
                        ScrollView:
                            GridLayout:
                                id: builds
                                cols: 1
                                size_hint_y: None
                                height: self.minimum_height
                    BoxLayout:
                        orientation: 'vertical'
                        Label:
                            text: "Commands"
                            size_hint_y:None
                            height: 24
                        Button:
                            id: command0
                            text: "-"
                            
                        Button:
                            id: command1
                            text: "-"
                            
                        Button:
                            id: command2
                            text: "-"
                            on_press:
                                print("Building % Compiling All")
                    
                CodeViews:
                    id: codeviews
        Screen:
            name: "screen1"
            ProjectBuilder:

        Screen:
            name: "screen2"
            BoxLayout:
                id: settings_box

""")



class MainWindow(BoxLayout):
    pass

class FileItem():
    type: str
    name: str
    
    def __init__(self,name,type):
        self.type = type
        self.name = name


Builder.load_string("""
<FileTreeViewer>:

""")

class FileTreeViewer(TreeView):
    def __init__(self, **kwargs):
        super(FileTreeViewer,self).__init__(**kwargs)


Builder.load_string("""
<CodeView>:
    orientation: 'vertical'
    Label:
        id:label
        size_hint_y:None
        height: 24
    CodeInput:
        id:code
""")
Builder.load_string("""
<CodeViewPy>:
    orientation: 'vertical'
    BoxLayout:
        size_hint_y:None
        height: 24
        Label:
            id:label
        Button:
        
            text: "Save"
            size_hint_x: None
            width: 48
    CodeInput:
        id:code
""")
class CodeView(BoxLayout):
    def __init__(self, **kwargs):
        super(CodeView,self).__init__(**kwargs)

class CodeViewPy(BoxLayout):
    def __init__(self, **kwargs):
        super(CodeViewPy,self).__init__(**kwargs)

Builder.load_string("""
<CodeViews>:
    
    CodeViewPy:
        id: view1
    CodeView:
        id: view2
    CodeView:
        id: view3

""")
class CodeViews(BoxLayout):
    
    def __init__(self, **kwargs):
        super(CodeViews,self).__init__(**kwargs)

print(dirname(__file__))

#toolchain = join(kivy_folder,"toolchain.py")
toolchain = "toolchain"
root_path = os.path.dirname(sys.argv[0])

# class EventHandler(FileSystemEventHandler):
#     app = None
#     def __init__(self,app, **kwargs):
#         super(EventHandler,self).__init__(**kwargs)
#         self.app = app

#     def on_any_event(self, event):
#         app:KivySwiftLink = self.app
#         #event.is
#         file_str = event.src_path
#         filetype = file_str.split('.')
#         if filetype[-1] == 'py':
#             #src = path + event.src_path
            
#             print (event.src_path)
#             app.build_wdog_event(event.src_path)







class KivySwiftLink(App):
    main: MainWindow
    imports: GridLayout
    group = "builders"
    selected_py: ToggleButton
    calltitle: str = ""
    mode = -1
    root_path: str
    kivy_folder:str
    kivy_recipes: str
    def __init__(self,root_path, **kwargs):
        super(KivySwiftLink,self).__init__(**kwargs)
        #self.wdog_thread()
        self.root_path = root_path
        self.app_dir = join(root_path,"PythonSwiftLink")
        print(root_path)
        # config_str = ""
        # with open(join(self.app_dir,"config.json"),"r") as f:
        #     config_str = f.read()
        # config = json.loads(config_str)
        # self.kivy_folder = config['kivy_ios_folder']
        self.kivy_folder = root_path
        #self.kivy_recipes = config['kivy_ios_recipes']
        self.kivy_recipes = join(root_path,"venv/lib/python3.8/site-packages/kivy_ios/recipes")
        # global _json
        # global _json_store
        # _json_store = JsonStore(join(root_path,"build_config.json"))
        # _json = {**_json_store}
        
        
        # if "build_info" in _json:
        #     self.build_info = _json.get("build_info")
        # else:
        #     self.build_info = {}
        #     _json_store["build_info"] = self.build_info
        # self.test_dict = {}

        # if "builds" not in _json_store["build_info"]:
        #     _json_store["build_info"]["builds"] = {}
        # if "project_target" in _json_store["build_info"]:

        #     self.project_target = _json_store["build_info"]["project_target"]
        # else:
        #     self.project_target = None
        self.project_target = None
        # self.test_dict["test2"] = {}
        # _json_store["test2"] = self.test_dict
        #self.build_info["root_path"] = root_path
        #self.storage["build_info"] = self.build_info
        #print(self.storage.__dict__)
    #"/Users/macdaw/kivyios_swift/venv/lib/python3.8/site-packages/kivy_ios/recipes"
    def build_selected(self,py_sel):
        p_build = PythonCallBuilder(self.app_dir)
        root_path = os.path.dirname(sys.argv[0])
        print("build_selected",self.app_dir)
        py_file = os.path.join(self.app_dir,"imported_pys",py_sel.text)
        #print(os.path.join(self.app_dir,"imported_pys",py_sel.text))
        if py_sel.type == "imports":
            cy_string,objc_h_script = p_build.build_py_files(os.path.join(self.app_dir,"imported_pys",py_sel.text))
            calltitle = p_build.get_calltitle()
            self.calltitle = calltitle
            self.view2.text = cy_string
            self.view2.scroll_y = 0
            self.view3.text = objc_h_script
            self.view3.scroll_y = 0
        else:
            calltitle = py_sel.title
            self.calltitle = calltitle
        
        #shutil.copy(py_file, )
        pack_all(self.app_dir,"master.zip",calltitle)
        file_time = getmtime(join(self.app_dir,"cython_headers","_%s.h" % calltitle))
        self.update_header_group()
        
        self.show_builds()
        print("show_builds")
        #
    # def set_project_folder(self,paths):
    #     d = _json_store["build_info"]
    #     try:
    #         print(paths)
    #         path = paths[0]
    #         print(path,isdir(path))
    #         if isdir(path):
    #             d["project_target"] = path
    #             self.project_target = path
    #         _json_store["build_info"] = d
    #     except:
    #         print("Setproject error")

    #remember
    # def update_build_dict(self,file):
    #     d = _json_store["build_info"]
    #     builds = d["builds"]
    #     if file in builds:
    #         pass
    #     else:
    #         header = "_%s.h" % file
    #         hpath = join(self.app_dir,"cython_headers",header)
    #         builds[file] = {
    #             "header": header,
    #             "path": hpath,
    #             "source_time": getmtime(hpath),
    #             "build_time": getmtime(hpath)
    #         }
    #     print(d)
    #     _json_store["build_info"] = d

    def update_classes_group(self):
        if self.project_target:
            target = self.project_target
            target_name = os.path.basename(target)[:-4]
            print("target_name: ",target_name)
            path = "%s/%s.xcodeproj/project.pbxproj" % (target, target_name)
            project = XcodeProject.load(path)
            project.remove_group_by_name("Classes",)
            classes = project.get_or_create_group("Classes")
            classes_list = set([child._get_comment() for child in classes.children])
            
            for item in ("runMain.h","runMain.m"):
                if item not in classes_list and item != ".DS_Store":
                    project.add_file(join(self.app_dir,item), parent=classes)
                    project_updated = True

            sources = project.get_or_create_group("Sources")
            sources_list = set([child._get_comment() for child in sources.children])
            print("sources_list",sources_list)
            if os.path.exists(join(self.project_target,"main.m")):
                os.remove(join(self.project_target,"main.m"))
            if "main.m" in sources_list:
                for src in sources.children:
                    if src._get_comment() == "main.m":
                        sources.children.remove(src)
                        break
            for (dirpath, dirnames, filenames) in os.walk(join(self.app_dir, "project_build_files")):
                for item in filenames:
                    if item not in sources_list and item != ".DS_Store":
                        dst = join(self.project_target,item)
                        shutil.copy(join(dirpath,item),dst)
                        print(dirpath,item)
                        project.add_file(dst, parent=sources)
                        project_updated = True
            pro_file = ""
            with open(path, "r") as f:
                pro_file = f.read()
            update_bridge = False
            pro_lines = pro_file.splitlines()
            for i, line in enumerate(pro_lines):
                if search("SWIFT_OBJC_BRIDGING_HEADER",line):
                    print(line,line.count("\t"))
                    if not search(".*\$\{PRODUCT_NAME\}-Bridging-Header.h",line):
                        print("editing line")
                        string = "".join(["\t" * line.count("\t"), "SWIFT_OBJC_BRIDGING_HEADER = \"${PRODUCT_NAME}-Bridging-Header.h\";"] )
                        print(string)
                        pro_lines[i] = string
                        update_bridge = True
            for i, line in enumerate(pro_lines):
                if search("SWIFT_OBJC_BRIDGING_HEADER",line):
                    print(line,line.count("\t"))
            
                # SWIFT_OBJC_BRIDGING_HEADER = "";
            if project_updated:
                project.backup()
                project.save()

            if update_bridge:
                project.backup()
                with open(path, "w") as f:
                    f.write("\n".join(pro_lines))
    
    def update_header_group(self):
        if self.project_target:
            target = self.project_target
            target_name = os.path.basename(target)[:-4]
            print("target_name: ",target_name)
            path = "%s/%s.xcodeproj/project.pbxproj" % (target, target_name)
            project = XcodeProject.load(path)
            header_classes = project.get_or_create_group("Headers")
            #print(header_classes.children[0]._get_comment())
            header_list = set([child._get_comment() for child in header_classes.children])
            header_dir = join(self.app_dir,"cython_headers")
            print(header_dir)
            project_updated = False
            for (dirpath, dirnames, filenames) in os.walk(header_dir):
                for file in filenames:
                    _file = join(header_dir,file)
                    if file not in header_list and file != ".DS_Store":
                        project.add_file(_file, parent=header_classes)
                        project_updated = True
            if project_updated:
                project.backup()
                project.save()
            print(header_classes)

    # def build_wdog_event(self,filename):
    #     p_build = PythonCallBuilder(self.app_dir)
        
    #     p_build.build_py_files(filename)
    #     calltitle = p_build.get_calltitle()

    #     pack_all("master.zip",calltitle)
    #     thread = Thread(target=self.compiler,args=[calltitle])
    #     thread.start()

    # def wdog_thread(self):
    #     event_handler = EventHandler(self)
    #     observer = Observer()
    #     observer.schedule(event_handler, join(self.root_path,"imported_pys"), recursive=True,)
    #     observer.start()

    def compile_selected(self,btn):
        self.build_log.text = "Compiling:\n"
        #self.build_log.text.__add__("Compiling:\n")
        self.build_popup.open()
        thread = Thread(target=self.compiler,args=[btn.title])
        thread.start()
     
    def show_imports(self):
        imports:GridLayout = self.imports
        imports.clear_widgets()
        for item in os.listdir(join(self.app_dir,"imported_pys")):
            if item.endswith("py"):
                t = ToggleButton(
                    text= item,
                    group=self.group,
                    size_hint_y=None,
                    height=48
                )
                t.type = "imports"
                t.bind(on_press=self.btn_action)
                # with open(join(root_path,"imported_pys",item)) as f:
                t.title = item
                imports.add_widget(t)
    
    def show_builds(self,*args):
        builds:GridLayout = self.builds
        builds.clear_widgets()
        
        for item in os.listdir(join(self.app_dir,"builds")):
            print(item)
            try:
                if os.path.isdir(join(self.app_dir,"builds",item)):
                    if os.path.exists(join(self.app_dir,"builds",item,"module.ini")):
                        with open(join(self.app_dir,"builds",item,"module.ini")) as f:
                            key,module = json.loads(f.read())
                            t = ToggleButton(
                                group=self.group,
                                size_hint_y=None,
                                height=48
                            )
                            t.type = "builds"
                            if module['type'] != "custom":
                                t.title = module['title']
                                t.text= module["title"]
                            else:
                                t.title = module['classname']
                                t.text= module["classname"]
                            t.bind(on_press=self.btn_action)
                            builds.add_widget(t)
            except Exception as E:
                print(E)
    #     s = os.path.join(src, item)
    #     d = os.path.join(dst, item)
    #     if os.path.isdir(s):
    #         shutil.copytree(s, d, False, None)

    def btn_action(self,btn:ToggleButton):
        if btn.state is 'normal':
            btn.state = 'down'
            print(btn.text)
        path = join(self.app_dir,"imported_pys",btn.text)
        #if btn.state is 'down':
        self.selected_py = btn
        if btn.type == "imports":
            self.command0.text = "Build Selected"
            self.command1.text = "Build All"
            self.mode = 0
            with open(path, 'r') as pyfile:
                print(path)
                self.view1.text = pyfile.read()
                self.view2.text = ""
                self.view3.text = ""
                self.view1.scroll_y = 0
        else:
            self.command0.text = "Compile Selected"
            self.command1.text = "Compile All"
            self.mode = 1

    def compiler(self,calltitle):
        #build_file = join(root_path,"builds",calltitle,"module_name.json")

        build_file = join(self.app_dir,"builds",calltitle.lower(),"kivy_recipe.py")

        target_path = join(self.kivy_recipes,calltitle)
        if not os.path.exists( target_path ):
            os.makedirs(target_path)
        recipe_path = join(target_path,"__init__.py")
        if os.path.exists( recipe_path ):
            print("__init__.py Exists")
            if not cmp(build_file,recipe_path):
                print("Updating __init__.py")
                shutil.copy(build_file,recipe_path)
        else:
            shutil.copy(build_file,recipe_path)
        try:
            remove_cache_file( join(self.root_path,".cache",calltitle+"-master.zip") )
        except:
            pass
        print(calltitle)
        command = " ".join([toolchain, "clean", calltitle])  # the shell command
        self.execute(command)
        command = " ".join([toolchain, "build", calltitle])  # the shell command
        self.execute(command)
        if self.project_target:
            command = " ".join([toolchain, "update", self.project_target])  # the shell command
            self.execute(command)
        #remember
        #self.update_build_dict(calltitle.lower())

        # command = " ".join(['python3.7',toolchain, "clean", calltitle])  # the shell command
        # self.execute(command)
        # command = " ".join(['python3.7',toolchain, "build", calltitle])  # the shell command
        # self.execute(command)
        # command = " ".join(['python3.7',toolchain, "clean", calltitle])  # the shell command
        # self.execute(command)
        try:
            remove_cache_file( join(self.root_path,".cache",calltitle+"-master.zip") )
        except:
            print("remove cache faled")


    def execute(self,command):
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        # Poll process for new output until finished
        while True:
            nextline = process.stdout.readline()
            if nextline == b'' and process.poll() is not None:
                break
            #sys.stdout.write(nextline.decode('utf-8'))
            line = nextline.decode('utf-8')
            sys.stdout.flush()
            self.update_log(line)

    @mainthread
    def update_log(self,text:str):
        
        self.build_log.text += text
        #self.build_log.insert_text(text)
    def command_actions(self,btn:Button):
        print("command_actions",btn.text)
        if self.mode == 1:
            if btn.idx == 0:
                self.compile_selected(self.selected_py)
            elif btn.idx == 1:
                pass
            elif btn.idx == 2:
                pass
        else:
            if btn.idx == 0:
                self.build_selected(self.selected_py)





    def build(self):
        self.main = MainWindow()
        ids = self.main.ids
        #print(self.main.ids)
        self.codeviews: CodeViews = self.main.ids.codeviews
        #print(self.codeviews.ids)
        print("working dir:",self.app_dir)
        self.imports = ids.imports
        self.builds = ids.builds
        self.sm:ScreenManager = ids.screens
        self.command0: Button = ids.command0
        self.command0.bind(on_press=self.command_actions)
        self.command0.idx = 0
        self.command1: Button = ids.command1
        self.command1.bind(on_press=self.command_actions)
        self.command1.idx = 1
        self.command2: Button = ids.command2
        self.command2.bind(on_press=self.command_actions)
        self.command2.idx = 2

        codes = self.codeviews
        codes.ids.view1.ids.label.text = "Python Code"
        codes.ids.view2.ids.label.text = "Cython .pyx"
        codes.ids.view3.ids.label.text = "OBJ-C .h"
        self.view1: CodeInput = codes.ids.view1.ids.code
        self.view2: CodeInput = codes.ids.view2.ids.code
        self.view2.lexer = CythonLexer()
        self.view3: CodeInput = codes.ids.view3.ids.code
        self.view3.lexer = ObjectiveCLexer()
        self.show_imports()
        self.show_builds(None)
        self.build_log = TextInput(
        )
        self.build_log.background_color = [0, 0, 0, 1]
        self.build_log.foreground_color = [0, 1, 0, 1]
        self.build_log.readonly = True
        self.build_popup = ModalView()
        self.build_popup.size_hint = (0.8,0.8)
        self.build_popup.add_widget(self.build_log)
        from kivy.config import ConfigParser

        config = ConfigParser()
        config.read('myconfig.ini')
        config.setdefaults('BuildInfo', {'text': 'Hello', 'font_size': 20, 'project_target':None})
        self.conf = config
        if config["BuildInfo"]["project_target"] == "":
            self.project_target = None
        else:
            self.project_target = config["BuildInfo"]["project_target"]
        #self.settings_cls = SettingsWithTabbedPanel
        s = Settings()
        s.add_json_panel('BuildInfo', config, join(self.app_dir,'app_config.json'))
        ids.settings_box.add_widget(s)
        s.bind(on_config_change=print)
        #s.add_json_panel('Another panel', config, 'settings_test2.json')
        # if self.project_target:
        #     ids.file_man.path = self.project_target
        return self.main

    def on_config_change(self, config, section, key, value):
        if section == "BuildInfo":
            if key == "project_target":
                self.project_target = value
if __name__ == '__main__':
    KivySwiftLink().run()
    #_json_store.update(_json)