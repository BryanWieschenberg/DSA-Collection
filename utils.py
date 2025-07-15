import inspect
import sys as s

e = lambda: s.exit(0)

def p(s):
    frame = inspect.currentframe().f_back
    print(eval(f'f"""{s}"""', frame.f_globals, frame.f_locals))
