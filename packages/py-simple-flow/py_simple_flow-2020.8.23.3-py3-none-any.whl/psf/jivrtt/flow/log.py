import logging
import logging.handlers
import os


def setup_logger(log_dir=None, level=logging.INFO):
    """
    Sets up the logger for the process
    :param log_dir: the log directory
    :param level: the logging level
    """
    root = logging.getLogger()
    formatter = logging.Formatter("%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s")
    if log_dir:
        log_parts = [log_dir, 'psf.log'] if log_dir else ['psf.log']
        log_path = os.path.join(*log_parts)
        file_handler = logging.handlers.TimedRotatingFileHandler(log_path, when='h', interval=6)
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)
    # Console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root.addHandler(console_handler)
    root.setLevel(level=level)
