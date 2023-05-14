import time
from PigeonTool import *
from endpoint import *

tool = PigeonTool()
start_time = time.time()

def scan(ip):
    # Execute the three functions in sequence for the given IP address
    start_time = time.time()
    alive = tool.connect(ip)
    duration_alive = time.time() - start_time
    duration_alive = round(duration_alive, 2)

    if alive == 'Yes':
        t_start_time = time.time()
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
        print(f"Device Found (IP): {ip}")
        print(f" Thread Time: {round(time.time() - t_start_time, 2)}")
        print(f'Connect Time: {duration_alive}     {alive}\n   Ping Time: {duration_ping}     {ping}\n'
              f'   Host Time: {duration_host}     {host}\n    MAC Time: {duration_mac}     {mac}\n')
        endpoint = Endpoint(ip, alive, host, ping, mac)
        #endpoint = {
        #    "ip_address": ip,
        #    "alive_status": alive,
        #    "ping_status": ping,
        #    "hostname_status": host,
        #    "mac_address": mac
        #}
    else:
        endpoint = Endpoint(ip, 'No', 'N/A', 'N/A', 'N/A')
        #endpoint = {
        #    "ip_address": ip,
        #    "alive_status": 'No',
        #    "ping_status": 'N/A',
        #    "hostname_status": 'N/A',
        #    "mac_address": 'N/A'}

    return endpoint