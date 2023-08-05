import time
from logging import info

from psf.jivrtt.flow.base import BaseSource, BaseIngress, BaseTransformer, BaseEgress
from psf.jivrtt.flow.dist import apply
from psf.jivrtt.flow.flow import run_flow
from psf.jivrtt.flow.log import setup_logger


class Source(BaseSource):

    def read(self, source_ids=None):
        info(f"Source: Yay!! Got the what needs to be fetched - {source_ids}")
        return source_ids


class Ingress(BaseIngress):

    def ingress(self, input_to_process):
        info("Ingress: Yay!! Got the input")


class Transformer(BaseTransformer):

    def transform(self, input_to_transform):
        info(f"Transform: Yay!! Got the input - {input_to_transform}")
        return input_to_transform


class Egress(BaseEgress):

    def egress(self, transform_output):
        info(f"Egress: Yay!! Got the output - {transform_output}")


def hello_world(num_of_tasks, *args, **kwargs):
    time.sleep(2)
    for _ in range(len(num_of_tasks)):
        time.sleep(1)
    info(f"Hello world - {num_of_tasks} - {args} - {kwargs}")


if __name__ == '__main__':
    import logging

    setup_logger(log_dir='D:/Tools/projects/py-simple-flow', level=logging.INFO)
    start = time.time()
    apply(
        hello_world,
        list(range(10)),
        ["Pass_Arg"],
        {"key": "value"},
        num_of_buckets=10,
        bucket_size=5,
        wait_for_completion=True
    )
    end = time.time()
    print(end - start)
    start = time.time()
    run_flow(
        list(range(50)),
        Source(),
        Ingress(),
        Transformer(),
        Egress(),
        bucket_size=3,
        max_buckets=5,
        log_dir='D:/Tools/projects/py-simple-flow',
    )
    end = time.time()
    print(end - start)
