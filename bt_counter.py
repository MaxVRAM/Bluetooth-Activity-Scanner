from time import sleep
from datetime import datetime as dt
from bleson import get_provider, Observer, logger
from logging import INFO, DEBUG, WARN, WARNING, ERROR

import statistics

# Silencing the bleson module because of all the logged warnings
logger.set_level(ERROR)

scan = {}

avg_sig_previous = 0
st_dev_previous = 0

def process_scan():
    global avg_sig_previous
    global st_dev_previous
    
    avg_sig_current = 0

    for d in scan:
        avg_sig_current += scan[d]

    avg_sig_current = avg_sig_current / len(scan)
    st_dev = statistics.stdev(scan.values())

    # Print Bluetooth presence values
    print()
    print()
    print('----------------------------------------------------')
    print(str(dt.now()))
    print()
    print(f'CURRENT:        {avg_sig_current}')
    print(f'PREVIOUS:       {avg_sig_previous}')
    print(f'DIFFERENCE:     {avg_sig_current - avg_sig_previous}')
    print()
    print(f'STND DEV:       {st_dev}')
    print(f'STND DEV DIFF:  {st_dev - st_dev_previous}')
    print()
    
    avg_sig_previous = avg_sig_current
    st_dev_previous = st_dev

def got_blip(device):
    mac = device.address.address
    sig = device.rssi

    if mac not in scan:
        scan[mac] = sig
    else:
        scan[mac] = sig
        
def timed_ble_scan(duration = 2):
    adapter = get_provider().get_adapter()
    observer = Observer(adapter)
    observer.on_advertising_data = got_blip
    observer.start()
    sleep(2)
    observer.stop()

while True:
    timed_ble_scan(2)
    process_scan()
    sleep(2)