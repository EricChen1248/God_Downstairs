''' Handles config file read write '''
import json
from os import path
import settings
import keys
from filepath import File_Path


def load_config():
    ''' Load in config data '''
    if path.isfile(File_Path.config):
        with open(File_Path.config, "r") as config_file:
            config = json.loads(config_file.read())
    else:
        with open(File_Path.config, "w+") as config_file:
            config = json.loads(default_config())
            config_file.write(json_to_str(config))

    settings.hiscore = int(config["hiscore"])
    settings.player_count = int(config["default_player_count"])
    settings.godmode = bool(config["godmode"])

    for key in config['keys']:
        keys.add_keys(key[0], key[1])

def json_to_str(json_data):
    ''' Convert json to string '''
    return json.dumps(json_data, sort_keys=True, indent=4)

def default_config():
    ''' Generates default config file '''
    return '{"hiscore":0,"default_player_count":1,"godmode":false,"keys":[["Left", "Right"], ["A", "D"]]}'

def update_config(score):
    ''' Update config file with new hiscore '''
    if path.isfile(File_Path.config):
        with open(File_Path.config, "r") as config_file:
            config = json.loads(config_file.read())
    else:
        config = json.loads(default_config())

    config["hiscore"] = score
    with open(File_Path.config, "w+") as config_file:
        config_file.write(json_to_str(config))
