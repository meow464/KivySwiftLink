#!/bin/bash
#cd /Volumes/WorkSSD/cython_stuff/PythonCallback/
mkdir ./temprecipefiles
rm /Volumes/WorkSSD/kivy-ios-11.04.20_copy/.cache/kivy_swift_link-master.zip
cp /Volumes/WorkSSD/cython_stuff/PythonCallback/* ./temprecipefiles/
zip -r ./kivy_swift_link-master.zip ./temprecipefiles/*
mv -v ./kivy_swift_link-master.zip /Volumes/WorkSSD/kivy-ios-11.04.20_copy/.cache
#cd ..
python3.7 /Volumes/WorkSSD/kivy-ios-11.04.20_copy/toolchain.py clean kivy_swift_link
python3.7 /Volumes/WorkSSD/kivy-ios-11.04.20_copy/toolchain.py build kivy_swift_link
#python3.7 toolchain.py update touchbay-ios
