from thread_worker import *
from terminal_table import *
from save_to_txt import *
from scan import *
from PigeonTool import *
from endpoint import *
from endpoint_list import *
import time

def menu():
    print('LAN Pigeon Lite\n')
    print(f'Current IP: {PigeonTool.current_ip()}')
    options = {1: "Scan IP Range", 2: "Save Results", 3: "Print Data"}
    print("Please select an option:")
    for key, value in options.items():
        print(f"{key} - {value}")
    selection = input("> ")
    return int(selection)

def menu_action(select):
    if select == 1:
        scan_app()

def scan_input():
    print()
    start_ip = input("       Start IP (192.168.1.1): ")
    end_ip =   input("End IP address (192.168.1.25): ")
    print()
    return start_ip, end_ip

def scan_app():
    start_ip, end_ip = scan_input()

    start = list(map(int, start_ip.split('.')))
    end = list(map(int, end_ip.split('.')))

    ips = []
    for i in range(start[3], end[3] + 1):
        ip = f"{start[0]}.{start[1]}.{start[2]}.{i}"
        ips.append(ip)
    cores = cpu_cores()  # amount of cores in CPU
    usage = cpu_usage()  # maps current usage of CPU in %
    x = 3  # thread multiplier, default 3
    threads = thread_count(ips, cores, usage) * x

    duration_start = time.time()
    endpoints = EndpointArray(thread_workers(scan, ips, cores, usage, x))  # runs function with set amount of threads
    duration_total = time.time() - duration_start
    duration_total = round(duration_total, 2)
    result = '----------STATS----------\n'
    result += f'Scan Duration: {duration_total} seconds\n'
    result += f'CPU Count: {cores}\n'
    result += f'CPU %: {usage}\n'
    result += f'Thread Numbers: {threads}\n\n'

    result += '-------SCAN  STATS-------\n'
    result += f"scanned ips: {endpoints.count}\n"
    result += f"endpoints found: {len([endpoint for endpoint in endpoints if endpoint.alive != 'No'])}\n"
    result += f'scan array: {endpoints}\n'
    for endpoint in endpoints:
        result += f'{str(endpoint)}\n'

    result += f'\nPRINTING GETTER(Expect index 0 given endpoint 1):\n'
    result += f'{endpoints[1]}\n\n'

    result += f'PRINTING TABLE TEST:\n'
    table = create_table(endpoints)
    result += f'{table}\n\n'

    print(result)
    prompt_save(result)
    input('Press enter to Exit . . .')

def main():
    menu_action(menu())


if __name__ == "__main__":
    main()

