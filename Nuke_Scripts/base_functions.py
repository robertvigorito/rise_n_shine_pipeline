import os
import json
import nuke
from getpass import getuser


def json_write(file_path, data):
    with open(file_path, 'w') as open_write_file:
        json.dump(data, open_write_file, indent=4)


def json_read(file_path):
    with open(file_path, 'r') as open_read_file:
        data = json.load(open_read_file)
        return data


def json_read_write(value=None):
    json_file_path = os.path.dirname(__file__) + '/rise_n_shine.json'
    data = dict()

    if os.path.exists(json_file_path):
        data = json_read(json_file_path)

    data[getuser()] = value
    json_write(json_file_path, data)
    return data[getuser()]


def read_write_nuke_init(nuke_init_file, plugin_path):
    try:
        with open(nuke_init_file, 'r') as open_read_file:
            data = open_read_file.read()

        for path in plugin_path:
            for line in data.splitlines():
                if path == line:
                    pass
            data += '\nnuke.pluginAddPath("{}")'.format(path)

    except IOError:
        if isinstance(plugin_path, list):
            data = '\n'.join(['nuke.pluginAddPath("{}")'.format(path) for path in plugin_path])
        else:
            data = 'nuke.pluginAddPath("{}")'.format(plugin_path)

    with open(nuke_init_file, 'w') as open_write_file:
        open_write_file.write(data)

