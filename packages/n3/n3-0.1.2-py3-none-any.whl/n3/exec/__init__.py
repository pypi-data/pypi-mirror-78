import argparse
import sys
import types

from .args import *
from .root import ExecRoot


def _open(program, env):
    if program == 'tensorboard':
        from ..writer import spawn_daemon
        spawn_daemon(env)
    else:
        raise Exception(f'no such program: {program}')


def route():
    # get the enviroment variables
    env = GlobalVars()
    env.load_env()

    exec_args = ExecVars()

    # define parser
    parser = argparse.ArgumentParser('n3',
                                     add_help=False,
                                     description='Process some integers.')

    # parser can modify envs
    env.attach_parser(parser)
    exec_args.attach_parser(parser)

    # show help message
    args = sys.argv[1:]
    if not args or len(args) == 1 and args[0] == 'help':
        parser.print_help()
        return

    # parse
    args, _ = parser.parse_known_args()
    env.apply(args)
    exec_args.apply(args)

    # positional arguments
    if sys.argv[1] != exec_args.mode or sys.argv[2] != exec_args.exec:
        raise Exception('positional arguments should be first.')

    # open other program
    if exec_args.mode == 'run':
        _open(exec_args.exec, env)
        return

    exec = exec_args.exec.title().replace('-', '')

    # init root
    root = ExecRoot(env)

    # parse
    ir = root.get(exec)
    ir.load_env()
    ir.attach_parser(parser)

    if exec_args.mode == 'help':
        parser.print_help()
        return
    elif exec_args.mode == 'publish':
        extra_args = PublishVars()
        extra_args.load_env()
        extra_args.attach_parser(parser)
    else:
        extra_args = None

    args, _ = parser.parse_known_args()
    ir.apply(args)

    if extra_args:
        extra_args.apply(args)

    # build
    node = ir.build(root)

    # test the mode executable
    mode = exec_args.mode

    if hasattr(node, mode):
        mode_fn = getattr(node, mode)
        if isinstance(mode_fn, types.MethodType):
            # exec
            if extra_args is not None:
                mode_fn(extra_args)
            else:
                mode_fn()
            return

    raise Exception(f'no such mode: {mode} in {exec}')
