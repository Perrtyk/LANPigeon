from assets.PigeonTool import PigeonTool
from assets.thread_worker import *
from assets.terminal_table import *
from assets.save_to_txt import *
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
    result = '----------STATS----------\n'
    result += f'Scan Duration: {duration_total}\n'
    result += f'CPU Count: {cores}\n'
    result += f'CPU %: {usage}\n'
    result += f'Thread Numbers: {threads}\n'

    result += '-------SCAN  STATS-------\n'
    result += f"scanned ips: {len(endpoints)}\n"
    result += f"endpoints found: {len([endpoint for endpoint in endpoints if endpoint['alive_status'] != 'N/A'])}\n"
    result += f'endpoints: {endpoints}\n\n'

    result += f'PRINTING DATA TEST (Expect index 0 given endpoint 1):\n'
    result += f'{get_data(endpoints, 1)}\n\n'

    result += f'PRINTING TABLE TEST:\n'
    table = create_table(endpoints)
    result += f'{table}\n\n'

    print(result)
    prompt_save(result)
    input('Press enter to Exit . . .')

if __name__ == "__main__":
    main()

