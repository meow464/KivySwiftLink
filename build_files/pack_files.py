
import os
import zipfile
import sys
import shutil

def zipdir(path,src, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            if file != ".DS_Store":
                print(root)
                ziph.write(os.path.join(root, file))
                _file,ext = file.split(".")
                print(_file,ext)
        if len(dirs) != 0:
            src.append((root,dirs))

def clear_temp():
    src = "./tmp"
    if os.path.exists(src):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            if os.path.isdir(s):
                shutil.rmtree(s)

def create_temp_copy_files(src,dst):
    if not os.path.exists(dst):
        os.makedirs("./tmp")
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, False, None)
    shutil.copy("./build_files/Setup.py","./tmp/Setup.py")
    shutil.copy("./builds/compile_modules.ini","./tmp/compile_modules.txt")
    shutil.copy("./build_files/files_list.py","./tmp/files_list.py")

def pack_all(src,dst):
    clear_temp()
    create_temp_copy_files("./builds","./tmp")
    builds = "./tmp/" 
    sources = []
    zipf = zipfile.ZipFile('./Exports/'+src, 'w', zipfile.ZIP_DEFLATED)
    zipdir(builds,sources, zipf)
    #zipf.write("build_files/Setup.py")
    zipf.close()
    shutil.move('Exports/' + src,dst + src)
    

if __name__ == '__main__':
    pack_all("Python.zip","Exports/cache/")
    