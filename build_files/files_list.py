import configparser




config = configparser.ConfigParser()

def open_config()->config:
    try:
        with open('compile_modules.ini', 'w') as configfile:
            config.read_file(configfile)
            configfile.close()
        return config
    except:
        d = {}
        d2 = {}
        d3 = {}
        d['Test'] = d2
        d['test2'] = d3
        d2['depends'] = {'hallo':1}
        d2['classname'] = ['']
        d2['dirname'] = "None"
        d2['classname'] = "None"
        config.read_dict(d)

        with open('compile_modules.ini', 'w') as configfile:
            config.write(configfile)
            configfile.close()
        return config







if __name__ == "__main__":
    open_config()