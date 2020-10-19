import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, 'src/')


import app
server = app.server 