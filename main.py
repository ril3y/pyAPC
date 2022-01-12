import time

import pyHive
from pyAPC import PyAPC, OutletCommand
from pyHive import PyHive

UPDATE_CHECK_PERIOD = 300
WORKSHOP1_OUTLET_PAIR = [1, 9]

if __name__ == "__main__":
    apc = PyAPC("http://192.168.1.218", "apc", "apc")
    apc.login()

    with open("hive_api_key.txt", "r") as f:
        api_key = f.read()
    hive = PyHive(api_key)
    workers_offline = []
    print("Starting Rig Monitor")
    _run = True
    while _run:
        workers_offline = hive.check_workers_offline()
        print(f'Time: {time.ctime()}')
        hive.print_data()
        for w in workers_offline:
            print(f'WORKER OFFLINE: {w.name}')
            if w.name == "WORKSHOP#1":
                print(f'REBOOTING OUTLETS!')
                apc.apply_outlet_command(OutletCommand.REBOOT_IMMEDIATE, WORKSHOP1_OUTLET_PAIR)
        time.sleep(UPDATE_CHECK_PERIOD)
