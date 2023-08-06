import re
import psutil
import subprocess

def pids_by_name(nm=None):
    rtn = []
    for proc in psutil.process_iter(['pid', 'name']):
        pinfo = proc.info
        pname = pinfo['name']
        if nm:
            _regex = re.compile(nm)
            iscontained = bool(_regex.search(pname))
            if iscontained:
                rtn.append(pinfo)
                continue
        else:
            rtn.append(pinfo)
    rtn = sorted(rtn, key=lambda o: o['name'])
    return rtn
