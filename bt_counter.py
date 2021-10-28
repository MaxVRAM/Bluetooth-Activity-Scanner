import time, random, statistics
from time import sleep
from datetime import datetime as dt
from bleson import get_provider, Observer, logger
from logging import INFO, DEBUG, WARN, WARNING, ERROR

### TODO uncomment when testing Prom metrics server
#from prometheus_client import start_http_server, Gauge


# Silencing the bleson module because of all the logged warnings
logger.set_level(ERROR)

# Prep some persistents
scan = {}
device_count_previous = 0
sig_total_previous = 0

# Will need to be adjusted in real-time, socket/api/env var or something similar
SIG_THRESHOLD = 0.001

# Convert dB to amplitude
def db_to_amp(db: float) -> float:
    return pow(10, float(db)/20)

# Iterate over BLE signals
def process_scan():
    global device_count_previous, sig_total_previous
    
    # Ignore weak signals
    filtered_sigs = list(filter(lambda sig: sig >= SIG_THRESHOLD, scan.values()))
    print(str(filtered_sigs))

    # Generate some basic stats
    device_count = len(filtered_sigs)
    device_count_diff = device_count - device_count_previous
    sig_total = sum(filtered_sigs)
    sig_total_diff = sig_total - sig_total_previous

    # Print Bluetooth presence values for testing
    print()
    print()
    print('----------------------------------------------------')
    print(str(dt.now()))
    print()
    print(f'NUM DEVICES:    {device_count} | DIFF: {device_count_diff}')
    print(f'TOTAL POWER:    {sig_total:.6f} | DIFF: {sig_total_diff:.6f}')
    print()

    # Store values for next poll
    device_count_previous = device_count
    sig_total_previous = sig_total


# (Callback) On each BLE device signal report
def got_blip(device):
    mac = device.address.address
    sig = device.rssi
    scan[mac] = db_to_amp(sig)

# Scan period        
def timed_ble_scan(duration = 2):
    observer.start()
    sleep(duration)
    observer.stop()


# Assign the Bluetooth device and assign an observer with callback function
adapter = get_provider().get_adapter()
observer = Observer(adapter)
observer.on_advertising_data = got_blip

while True:
    timed_ble_scan(5)
    process_scan()
    sleep(2)





### TODO pop in a Prom metrics server

# # Decorate function with metric.
# @REQUEST_TIME.time()
# def process_request(t):
#     """A dummy function that takes some time."""
#     time.sleep(t)

# if __name__ == '__main__':
#     # Start up the server to expose the metrics.
#     start_http_server(8000)
#     # Generate some requests.
#     while True:
#         process_request(random.random())
