import subprocess
def mcwd_id():
    """ machine id for window """
    return subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
