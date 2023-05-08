import time
from assets.PigeonTool import PigeonTool

tool = PigeonTool()
start_time = time.time()

def scan(ip):
    # Execute the three functions in sequence for the given IP address
    start_time = time.time()
    alive = tool.connect(ip)
    duration_alive = time.time() - start_time
    duration_alive = round(duration_alive, 2)

    if alive == 'Yes':
        start_time = time.time()
        ping = tool.ping(ip)
        duration_ping = time.time() - start_time
        duration_ping = round(duration_ping, 2)

        start_time = time.time()
        host = tool.hostname(ip)
        duration_host = time.time() - start_time
        duration_host = round(duration_host, 2)

        start_time = time.time()
        mac = tool.mac_address(ip)
        duration_mac = time.time() - start_time
        duration_mac = round(duration_mac, 2)
        print(ip)
        print(f'time {duration_alive}     {alive}\ntime {duration_ping}     {ping}\n'
              f'time {duration_host}     {host}\ntime {duration_mac}     {mac}\n')
        endpoint = {
            "ip_address": ip,
            "alive_status": alive,
            "ping_status": ping,
            "hostname_status": host,
            "mac_address": mac
        }
    else:
        endpoint = {
            "ip_address": ip,
            "alive_status": 'No',
            "ping_status": 'N/A',
            "hostname_status": 'N/A',
            "mac_address": 'N/A'}

    return endpoint