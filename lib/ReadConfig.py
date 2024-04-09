import os,configparser

def readConfig():
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(parent_dir, '..', 'config.ini')
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file '{config_path}' not found.")
    config = configparser.ConfigParser()
    config.read(config_path)
    return config
