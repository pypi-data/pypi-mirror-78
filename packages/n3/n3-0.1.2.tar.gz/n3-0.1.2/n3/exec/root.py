import os
from pathlib import Path

import click

from ..builder import NodeRoot
from ..std import trim_name
from ..util.dirs import *


class ExecRoot:
    def __init__(self, env):
        super().__init__()
        self.env = env
        self.node_root = NodeRoot()
        self.node_root.env = env

        self._create_root_dir()
        self._load_local_nodes()

    def get(self, name):
        return self.node_root.get(name)

    @property
    def root_dir(self):
        return self.env.root

    def _create_root_dir(self):
        path = Path(self.root_dir)

        if path.exists():
            if path.is_dir():
                return
            raise Exception(f'not directory: {path}')

        if not click.confirm(
            f'''It seems that there is no root directory on "{path}"
- Do you want to create one?''', default=False):
            raise Exception('user cancelled')

        path.mkdir(parents=True, exist_ok=True)
        for name in [DATA_DIR, MODELS_DIR, NODES_DIR, f'{NODES_DIR}/{NODES_USER_DIR}']:
            (path / name).mkdir(exist_ok=True)

    def _load_local_nodes(self):
        path = os.path.join(self.root_dir, 'nodes')
        for p in Path(path).glob('**/*.n3'):
            name = trim_name(p.name)
            self.node_root.add_source_path(name, str(p))

            extern_name = p.name[:-3].replace("-", "_")
            extern_path = os.path.join(p.parent, f'{extern_name}.py')
            if os.path.exists(extern_path):
                self.node_root.add_extern(name, extern_path)
