import configparser
import os



config = configparser.ConfigParser()

def open_config(path:str)->config:
    print(os.path.join(path,"compile_modules.txt"))
    try:
        with open(os.path.join(path,"compile_modules.txt"), 'r') as configfile:
            config.read_file(configfile)
            configfile.close()
        return config
    except:
        return config







if __name__ == "__main__":
    open_config()