#!/bin/bash
# Ask the user for login details
echo """
Options:
#################################
w   -   create working folder and run setup
p   -   create project
"""
read -p 'command: ' command_var

if [ $command_var == "p" ]
    then
        echo "building"
elif [ $command_var == "w" ]; then
    read -p 'Folder name: ' folder_var
    echo
    echo Creating Dir $folder_var 
    mkdir ./$folder_var
    cd $folder_var

    python3.8 -m venv venv
    . venv/bin/activate

    pip install kivy
    pip install kivy-ios
    pip install astor

    #rsync -av --delete --exclude '.git' /Users/macdaw/kivyios_swift/PythonSwiftLink/* ./PythonSwiftLink
    git clone https://github.com/psychowasp/PythonSwiftLink
    #cp /Users/macdaw/kivyios_swift/PythonSwiftLink ./
    cp ./PythonSwiftLink/main.py ./wrapper_tool.py
    cp ./PythonSwiftLink/wrapper_tool.sh ./wrapper_tool.sh

    chmod +x wrapper_tool.sh
    toolchain build kivy

    echo
    echo "Working folder <$folder_var> is now ready"
    echo
    # read -p 'Project name: ' pro_var

    #toolchain create $pro_var 
else
    echo "no option selected"
fi
echo "Done"