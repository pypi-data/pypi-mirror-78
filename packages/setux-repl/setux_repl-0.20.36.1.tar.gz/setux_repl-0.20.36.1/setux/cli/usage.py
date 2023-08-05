from setux.main import banner

doc = f'''
{banner}

Command mode:
    setux CMD [ARG] [TARGET]

    CMD:
        - infos
        - ping

    Execute CMD ARG on TARGET


REPL mode:
    setux [TARGET]

    Enter repl on TARGET


Target:
    - May be passed on command line
    - Set in environement as "setux_target"
    - defaults to "Local"
'''

def usage(*args):
    print(doc)
