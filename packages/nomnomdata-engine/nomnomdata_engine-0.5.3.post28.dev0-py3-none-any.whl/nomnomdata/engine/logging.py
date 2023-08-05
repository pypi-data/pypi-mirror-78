import logging
import os
import traceback
import warnings
from concurrent.futures import ThreadPoolExecutor

from nomnomdata.engine.api import NominodeClient
from nomnomdata.engine.components.context import nominode_ctx


class NominodeLogHandler(logging.Handler):
    # Send log lines in a separate thread, log lines are 'non critical' so if we get a timeout we don't care too much
    # Using a thread pool to limit the number of threads spawned

    def __init__(
        self, *args, sync=False, **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.sync = sync
        self.nominode = NominodeClient()
        self.threadPool = ThreadPoolExecutor(1)

    def shutdown(self):
        self.threadPool.shutdown()

    def emit(self, record):
        if self.sync:
            self._emit(record)
        else:
            self.threadPool.submit(self._emit, record)

    def _emit(self, record):
        to_send = record.__dict__.copy()
        to_send["execution_uuid"] = nominode_ctx.execution_uuid
        to_send["log_version"] = "0.1.0"
        if to_send["exc_info"]:
            to_send["exception_lines"] = traceback.format_exception(*to_send["exc_info"])
            del to_send["exc_info"]
        to_send["msg"] = str(to_send["msg"])

        r_logger = logging.getLogger("requests")
        url_logger = logging.getLogger("urllib3")
        r_logger.propagate = False
        url_logger.propagate = False
        self.nominode.request(
            "put", f"execution/log/{nominode_ctx.execution_uuid}", data=to_send
        )
        r_logger.disabled = True
        url_logger.disabled = True


def getLogger(name):
    warnings.warn(
        f"nomnomdata.engine.logging.getLogger is deprecated, please use the python standard library logging instead for {name}",
        DeprecationWarning,
    )

    logger = logging.getLogger(name)
    if os.environ.get("token"):
        logger.setLevel(os.environ.get("log_level") or "INFO")
        handler = NominodeLogHandler(sync=True)
        logger.addHandler(handler)
    return logger
