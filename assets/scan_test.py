from thread_worker import *
from terminal_table import *
from save_to_txt import *
from scan import *
import time

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
    result += f'Scan Duration: {duration_total} seconds\n'
    result += f'CPU Count: {cores}\n'
    result += f'CPU %: {usage}\n'
    result += f'Thread Numbers: {threads}\n\n'

    result += '-------SCAN  STATS-------\n'
    result += f"scanned ips: {len(endpoints)}\n"
    result += f"endpoints found: {len([endpoint for endpoint in endpoints if endpoint['alive_status'] != 'No'])}\n"
    result += f'scan array:\n'
    for endpoint in endpoints:
        result += f'{str(endpoint)}\n'

    result += f'\nPRINTING GETTER(Expect index 0 given endpoint 1):\n'
    result += f'{get_data(endpoints, 1)}\n\n'

    result += f'PRINTING TABLE TEST:\n'
    table = create_table(endpoints)
    result += f'{table}\n\n'

    print(result)

    prompt_save(result)
    input('Press enter to Exit . . .')

if __name__ == "__main__":
    main()
