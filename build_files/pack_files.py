
import os
import zipfile
import sys


def zipdir(path,src, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            if file != ".DS_Store":
                ziph.write(os.path.join(root, file))
                _file,ext = file.split(".")
                print(_file,ext)
        if len(dirs) != 0:
            src.append((root,dirs))

if __name__ == '__main__':
    builds = "./builds" 
    sources = []
    zipf = zipfile.ZipFile('Exports/Python.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir(builds,sources, zipf)
    zipf.close()
    print(sources)