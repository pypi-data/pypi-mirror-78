import multiprocessing
import time
from logging import info


def apply(target_func, tasks, args=None, kwargs=None, num_of_buckets=1, bucket_size=1, wait_for_completion=True):
    run_local = num_of_buckets == 1
    args = args or list()
    kwargs = kwargs or dict()
    info(f"{target_func.__name__}: Starting execution of task. Run Local: {run_local}")
    if run_local:
        target_func(tasks, *args, **kwargs)
    else:
        _run_multi_process(
            target_func,
            tasks,
            args=args,
            kwargs=kwargs,
            num_of_buckets=num_of_buckets,
            bucket_size=bucket_size,
            wait_for_completion=wait_for_completion,
        )


def _run_multi_process(
        target_func,
        tasks,
        args=None,
        kwargs=None,
        num_of_buckets=5,
        bucket_size=1,
        wait_for_completion=True
):
    buckets = map(lambda idx: tasks[idx:idx + bucket_size], range(0, len(tasks), bucket_size))
    processes = []
    for bucket_idx, bucket in enumerate(buckets, 1):
        _limit_processes(bucket_idx, processes, num_of_buckets)
        args_to_pass = tuple([bucket] + list(args))
        process = _start_processes(target_func, args=args_to_pass, kwargs=kwargs)
        processes.append(process)
    list(map(lambda prc: prc.join() if wait_for_completion else None, processes))
    total_complete = sum(map(lambda prc: 1 if prc.exitcode is not None else 0, processes))
    info(f'Total buckets processed: {len(processes)}. Total completed: {total_complete}')


def _start_processes(
        target_func,
        args=None,
        kwargs=None,
):
    info(f"Spawning a new process.")
    process = multiprocessing.Process(target=target_func, args=args, kwargs=kwargs, daemon=True)
    process.start()
    return process


def _limit_processes(bucket_idx, processes, num_of_buckets):
    total_complete = _get_total_processes(processes)
    while (bucket_idx - total_complete) >= num_of_buckets:
        info(f"Next task held. Process Limit: {num_of_buckets}. Currently running: {bucket_idx - total_complete}")
        total_complete = _get_total_processes(processes)
        time.sleep(0.1)
    info(f"Total processes started: {len(processes)}, Total complete: {total_complete}")


def _get_total_processes(processes):
    return sum(map(lambda prc: 1 if prc.exitcode is not None else 0, processes))
