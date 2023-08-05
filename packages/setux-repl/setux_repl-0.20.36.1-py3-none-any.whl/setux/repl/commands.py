def run(target, arg):
    target(arg)

def infos(target, arg):
    target.deploy('infos')

def module(target, arg):
    mod = target.modules.items.get(arg)
    if mod:
        title = f'module {arg}'
        print(title)
        print('-'*len(title))
        print(mod.help())
    else:
        print(f' ! unkown module ! {arg}')

def modules(target, arg):
    modules = target.modules.items
    print('modules')
    print('-------')
    width = len(max(modules.keys(), key=len))+4
    for name, mod in sorted(modules.items()):
        hlp = mod.help()
        first = hlp.split('\n')[0]
        if (
            not arg
            or arg in name
            or arg in first.lower()
        ): print(f'{name:>{width}} {first}')

def deploy(target, arg):
    target.deploy(arg)

def remote(target, arg):
    target.remote(arg)

def update(target, arg):
    target.Package.update()

def upgrade(target, arg):
    target.Package.upgrade()

def installed(target, arg):
    pkg = list(target.Package.installed(arg))
    print('\n'.join(f'{n} {v}' for n, v in pkg))

def available(target, arg):
    pkg = list(target.Package.available(arg))
    print('\n'.join(f'{n} {v}' for n, v in pkg))

def bigs(target, arg):
    pkg = list(target.Package.bigs())
    print('\n'.join(pkg))

def upgradable(target, arg):
    pkg = list(target.Package.upgradable())
    print('\n'.join(n for n, v in pkg))

def install(target, arg):
    target.Package.install(arg)

def remove(target, arg):
    target.Package.remove(arg)

def cleanup(target, arg):
    target.Package.cleanup()

def status(target, arg):
    target.Service.status(arg)

def start(target, arg):
    target.Service.start(arg)

def stop(target, arg):
    target.Service.stop(arg)

def restart(target, arg):
    target.Service.restart(arg)

def enable(target, arg):
    target.Service.enable(arg)

def disable(target, arg):
    target.Service.disable(arg)

def download(target, arg):
    url, dst = arg.split(' ') if ' ' in arg else arg, None
    target.deploy('download', url=url, dst=dst)

def outrun(target, arg):
    log = target.outrun
    if log:
        print(open(log).read())
    else:
        print('target outrun not defined')

def outlog(target, arg):
    log = target.outlog
    if log:
        print(open(log).read())
    else:
        print('target outlog not defined')
