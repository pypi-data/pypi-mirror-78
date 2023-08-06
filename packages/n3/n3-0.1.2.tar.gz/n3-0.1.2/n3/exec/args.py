from pathlib import Path

from ..util import EnvVars, Vars


class GlobalVars(EnvVars):
    root = str(Path.home() / '.n3')
    _root_help = 'hehehehe'  # TODO: to be implemented

    devices = set()
    _devices_help = 'hehehehe'  # TODO: to be implemented


class ExecVars(Vars):
    mode: str = None
    _mode_type = str
    _mode_help = 'hehehehe'  # TODO: to be implemented
    _mode_is_keyword = False

    exec: str = None
    _exec_type = str
    _exec_help = 'hehehehe'  # TODO: to be implemented
    _exec_is_keyword = False

    _order = ['mode', 'exec']


class PublishVars(EnvVars):
    target = 'onnx'
    _target_shortcut = 't'
    _target_help = 'hehehehe'  # TODO: to be implemented

    output_path: str = None
    _output_path_type = str
    _output_path_shortcut = 'o'
    _output_path_help = 'hehehehe'  # TODO: to be implemented
