from concurrent.futures import ThreadPoolExecutor
from PigeonTool import PigeonTool
from thread_worker import *
from terminal_table import *
import time

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
              f'time {duration_host}     {host}\ntime {duration_mac}     {mac}')
        endpoint = {
            "ip_address": ip,
            "alive_status": alive,
            "ping_status": ping,
            "hostname_status": host,
            "mac_address": mac
        }
    else:
        endpoint = {
            "ip_address": 'N/A',
            "alive_status": 'N/A',
            "ping_status": 'N/A',
            "hostname_status": 'N/A',
            "mac_address": 'N/A'}

    return endpoint

def main():
    ips = [f"192.168.1.{i}" for i in range(1, 255)]
    cores = cpu_cores()                         # amount of cores in CPU
    usage = cpu_usage()                         # maps current usage of CPU in %
    x = 3                                       # thread multiplier, default 3
    threads = thread_count(ips, cores, usage) * x

    endpoints = thread_workers(scan, ips, cores, usage, x)  # runs function with set amount of threads

    duration_total = time.time() - start_time
    duration_total = round(duration_total, 2)

    print('----------STATS----------')
    print(f'Scan Duration: {duration_total}')
    print(f'CPU Count: {cores}')
    print(f'CPU %: {usage}')
    print(f'Thread Numbers: {threads}')
    print()

    print(f'number of results: {len(endpoints)}')
    print(f'endpoints: {endpoints}')
    print()

    print(f'PRINTING DATA TEST (Expect index 0 given endpoint 1):')
    print(get_data(endpoints, 1))
    print()

    print(f'PRINTING TABLE TEST:')
    table = create_table(endpoints)
    print(table)
    print()

    input('Press enter to Exit . . .')

if __name__ == "__main__":
    main()
