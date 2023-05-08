import psutil
from concurrent.futures import ThreadPoolExecutor


def cpu_cores():
    cpu_count = psutil.cpu_count(logical=False)
    return cpu_count


def cpu_usage():
    cpu_percent = psutil.cpu_percent(interval=1)
    return cpu_percent


def thread_count(args, cores, usage):
    num_threads = min(len(args), max(1, int(cores * (1 - usage / 100))))
    return num_threads


def thread_workers(func, args, cpu_count, cpu_percent, multiplier):
    # Determine the optimal number of threads based on CPU usage
    count = cpu_count
    usage = cpu_percent

    # Determine the number of threads to use based on CPU usage and number of arguments
    num_threads = thread_count(args, count, usage)
    num_threads = num_threads * multiplier

    # Create a thread pool with the determined number of threads
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit each argument to the thread pool for processing
        for arg in args:
            executor.submit(func, arg)
    executor.shutdown(wait=True)
