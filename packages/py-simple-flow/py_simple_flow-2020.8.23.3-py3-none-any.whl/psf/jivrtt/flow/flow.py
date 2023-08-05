from logging import INFO

from psf.jivrtt.flow.base import BaseFlow
from psf.jivrtt.flow.dist import apply
from psf.jivrtt.flow.log import setup_logger


def run_flow(tasks, source, ingress, transformer, egress, bucket_size=1, max_buckets=1, log_level=INFO, log_dir=None):
    """
    Runs the flow either in one process or multiple processes depending on the inputs
    :param tasks: list of tasks to be processed
    :param source: the source instance to fetch the required data
    :param ingress: ingress instance extended from BaseIngress
    :param transformer: transformer instance extended from BaseTransformer
    :param egress: egress instance extended from BaseEgress
    :param bucket_size: the number of tasks per bucket
    :param max_buckets: the maximum buckets to run at any point
    :param log_level: the logging level to be used
    :param log_dir: the directory to place the logs
    """
    apply(
        _run_flow,
        tasks,
        args=(source, ingress, transformer, egress),
        kwargs={
            "log_level": log_level,
            "log_dir": log_dir,
        },
        num_of_buckets=max_buckets,
        bucket_size=bucket_size
    )


def _run_flow(tasks, source, ingress, transformer, egress, log_level=INFO, log_dir=None):
    setup_logger(log_dir=log_dir, level=log_level)
    flow = BaseFlow(source, ingress, transformer, egress)
    flow.process(tasks)
