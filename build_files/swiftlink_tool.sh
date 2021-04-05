#!/bin/bash
# Ask the user for login details
BASEDIR=$(dirname $0)
INPUT_STRING=none
folder_var=kivyswift
# while [ "$INPUT_STRING" != "x" ]
# do
    echo $BASEDIR
    echo """
    Options:
    #############################################
    w   -   create working folder and run setup
    x   -   exit
    #############################################
    """
    read -p 'command: ' INPUT_STRING
    if [ $INPUT_STRING == "p" ]; then
        echo "Not working yet :-P"
    elif [ $INPUT_STRING == "r" ]; then
        ""
        # cd $folder_var
        # . venv/bin/activate
        # python wrapper_tool.py
        # cd ..
    elif [ $INPUT_STRING == "w" ]; then
        echo "type folder name - default is:"
        echo
        echo "  kivyswift"
        echo
        read -p 'Folder name: ' folder_var
        if [ $folder_var = ""] ; then
            folder_var=kivyswift
        fi
        echo
        echo Creating Dir $folder_var 
        mkdir ./$folder_var
        cd $folder_var
        echo $(dirname $0)

        python3.8 -m venv venv
        . venv/bin/activate
        pip install cython
        pip install kivy
        pip install kivy-ios
        pip install astor

#        rsync -av --delete --exclude '.git' /Users/macdaw/kivyios_swift/PythonSwiftLink/* ./PythonSwiftLink
        git clone https://github.com/psychowasp/PythonSwiftLink
        #cp /Users/macdaw/kivyios_swift/PythonSwiftLink ./
        cp ./PythonSwiftLink/main.py ./wrapper_tool.py
        cp ./PythonSwiftLink/wrapper_tool.sh ./wrapper_tool.sh

        chmod +x wrapper_tool.sh
        toolchain build kivy

        echo
        echo "Working folder <$folder_var> is now ready"
        echo
        cd $BASEDIR
        # read -p 'Project name: ' pro_var

        #toolchain create $pro_var 
    else
        echo "no option selected"
    fi
# done
echo "Done"
