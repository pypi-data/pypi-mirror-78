from os import environ
from os.path import expanduser
from sys import argv

from setux.targets import Local, SSH
from setux.logger import debug
from setux.repl import commands
from setux.repl.repl import repl, prompt
from .usage import usage


def get_target(name=None, dest=None):
    name = name or environ.get('setux_target')
    dest = dest or environ.get('setux_outdir', expanduser('~/setux'))
    if name:
        try:
            target = SSH(name=name, host=name, outdir=dest)
        except:
            target = None
    else:
        target = Local(outdir=dest)
    return target


def main():
    if len(argv)>1:
        name = argv[1]
        if name in ('usage', 'help', '?'): return usage()
        if name.startswith('-'): return usage()
        cmd = commands.get(name)
    else:
        cmd = None

    if cmd:
        target, args = None, argv[2:]
        if args:
            target = get_target(args[-1])
            if target:
                args = args[:-1]
        if not target:
            target = get_target()
        args = ' '.join(args)
        debug(f'{name} {target} {args}')
        print(f'{prompt(target)}{args}')
        cmd(target, args)
    else:
        target = get_target(argv[1] if len(argv)>1 else None)
        debug(f'repl {target}')
        repl(target)
