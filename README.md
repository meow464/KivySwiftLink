# PythonSwiftLink

 ## Installation

PythonSwiftLink requires [Kivy](https://kivy.org)(the GUI), [Cython](https://cython.readthedocs.io/en/latest/src/tutorial/cython_tutorial.html) and [Kivy-ios](https://github.com/kivy/kivy-ios) to run.

Create the root folder for the whole build: 
```sh
mkdir kivyios_swift
cd kivyios_swift
```
create a virtual env and activate it.
```sh
python3 -m venv venv
. venv/bin/activate
```

install kivy and kivy-ios
```sh
pip install kivy
pip install kivy-ios
```
build kivy in the toolchain
```sh
toolchain build kivy
```
install PythonSwiftLink
```sh
git clone https://github.com/psychowasp/PythonSwiftLink
```

[Writing first Python wrapper file](https://github.com/psychowasp/PythonSwiftLink/tree/main/examples/0%20Getting%20Started)