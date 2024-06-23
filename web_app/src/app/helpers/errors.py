import logging
import traceback


def log_error(exc, print_traceback: bool = False):
    logging.error(f"Exception: {exc.__class__.__name__} {exc}")
    if print_traceback:
        traceback.print_exc()
