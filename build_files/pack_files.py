
import os
import zipfile
import sys


def zipdir(path,src, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
        if len(dirs) != 0:
            src.append((root,dirs))

if __name__ == '__main__':
    builds = "./builds" 
    sources = []
    zipf = zipfile.ZipFile('Exports/Python.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir(builds,sources, zipf)
    zipf.close()
    print(sources)