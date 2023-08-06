from abc import ABC, abstractmethod
import logging
from typing import Mapping, Any
import os
import traceback

from .types import Param

__version__ = "0.1.0"

LOGGER = logging.getLogger(__name__)

ENV_ENTRYPOINT = "EP"


class Engine:
    """Base class for our Engine."""

    def get_next(self) -> Param:
        pass

    def done(self, param: Param):
        pass

    def skip(self, param: Param):
        pass


class Callback(ABC):
    """Base class for the (user defined) callbacks."""

    @abstractmethod
    def on_param_received(self, param: Mapping[Any, Any], engine: Engine):
        pass

    @abstractmethod
    def on_param_finished(
        self, param: Mapping[Any, Any], engine: Engine, exception: Exception
    ):
        pass


class PrintCallback(Callback):
    """Dummy callback for debug purpose."""

    def on_param_received(self, param, engine):
        print(f"received {param}")

    def on_param_finished(self, param, engine, exception):
        print(f"finished {param}")
        # everything gonna be alright
        engine.done(param)


class ProcessCallback(Callback):
    def to_cmd(self, param: Param):
        return f"echo {param}"

    def on_param_received(self, param, engine):
        import subprocess

        p = subprocess.run(self.to_cmd(param), shell=True, check=True)
        p.check_returncode()

    def on_param_finished(self, param, engine, exception):
        if exception is None:
            engine.done(param)
        else:
            engine.skip(param)


class EntryPoint:
    def __init__(self, callback: Callback, engine: Engine):
        self.cb = callback
        self.engine = engine

    def run(self):
        """Routine."""
        while True:
            LOGGER.debug("get next param")
            param = self.engine.get_next()
            exception = None
            if param is None:
                LOGGER.debug("No more params to handle, leaving")
                break
            LOGGER.debug(f"SWEEP {param}")
            try:
                self.cb.on_param_received(param, self.engine)
            except Exception as e:
                exception = e
                traceback.print_exc()
            self.cb.on_param_finished(param, self.engine, exception)


def minionizer(callback: Callback):
    # NOTE(msimonin): load dynamically from the name
    ep = os.getenv(ENV_ENTRYPOINT)
    if ep == "execo":
        from minionize.execo import Execo

        engine = Execo.from_env()
    elif ep == "google":
        from minionize.google import GooglePubSub

        engine = GooglePubSub.from_env()
    else:
        raise Exception(f"EntryPoint {ep} not supported")
    return EntryPoint(callback, engine)
