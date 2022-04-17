'''
Created on Apr 17, 2022

@author: tomblackshaw
'''


import time
import os
import sys
from pathlib import Path 


DEBUGGING = ('192.168.0.140', '192.168.0.113') # FIXME: remote, local. Deduce from ifconfig eth0 etc.; don't hardcode the values


def connect_to_pydev_remote_debugger(debug_ip):
    import pydevd
    plugins_dir = '/Applications/Eclipse.app/Contents/Eclipse/plugins'
    if os.path.exists(plugins_dir):
        sys.path.append([
            x[0] for x in os.walk(plugins_dir)
            if x[0].find('pydev_') >= 0 and x[0].endswith('/pysrc')
        ][0])
    sys.path.append(os.getcwd())
    pydevd.settrace(debug_ip, stdoutToServer=True, stderrToServer=True)


def debug_remotely():
    script_full = Path(__file__)
    script_path = script_full.parent
    if os.path.exists("/Applications"): # FIXME: Lousy way to find out if the computer is the dev PC or the remote device...
        s = f'''ssh -o StrictHostKeyChecking=accept-new root@{DEBUGGING[0]} "cd \\"{script_path}\\" && python3 \\"{script_full}\\""'''
        res = os.system(s)
        print(f"I, the dev PC, launched {script_full} on the remote device. A moment ago, the ssh instance ended, returning res={res}")
        sys.exit(res)
    else:
        print(f"{script_full} is running remotely on me, the remote device. Press <fn><F6> to step over & continue.")
        connect_to_pydev_remote_debugger(DEBUGGING[1])


if __name__ == '__main__':
    print(f"{Path(__file__)} --- starting")
    if DEBUGGING:
        debug_remotely()    
    print("Proceeding")
    print(os.environ)
    for i in range(3):
        print(f'i={i}')
        time.sleep(1)
        
    print('Done. I, the remotely running script, have run to completion. Yay.')
    print(f"{Path(__file__)} --- ending")


