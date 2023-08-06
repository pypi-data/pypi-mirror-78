from abc import ABC, abstractmethod
import logging
from typing import Mapping, Any
import os
import traceback

from .types import Param

LOGGER = logging.getLogger(__name__)

ENV_ENGINE = "MINION_ENGINE"


class Engine:
    """Base class for our Engine."""

    def get_next(self) -> Param:
        pass

    def done(self, param: Param):
        pass

    def skip(self, param: Param):
        pass


class Callback:
    """Base class for the (user defined) callbacks."""

    def setup(self, param: Param, engine: Engine):
        pass

    def process(self, param: Param, engine: Engine):
        pass

    def teardown(self, param: Param, engine: Engine, exception: Exception):
        pass

    def finalize(self, param: Param, engine: Engine, exception: Exception):
        pass

class PrintCallback(Callback):
    """Dummy callback for debug purpose."""

    def pre(self, param, engine):
        print(f"pre {param}")

    def process(self, param, engine):
        print(f"process {param}")
        engine.done(param)

    def teardown(self, param, engine, exception):
        print(f"finished {param}")
        # everything gonna be alright


class ProcessCallback(Callback):
    def to_cmd(self, param: Param):
        return f"echo {param}"

    def process(self, param: Param, engine: Engine):
        import subprocess

        p = subprocess.run(self.to_cmd(param), shell=True, check=True)
        p.check_returncode()

    def finalize(self, param: Param, engine: Engine, exception: Exception):
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
            self.cb.setup(param, self.engine)
            try:
                self.cb.process(param, self.engine)
            except Exception as e:
                exception = e
                traceback.print_exc()
            self.cb.finalize(param, self.engine, exception)
            self.cb.teardown(param, self.engine, exception)


def minionizer(callback: Callback):
    # NOTE(msimonin): load dynamically from the name
    ep = os.getenv(ENV_ENGINE)
    if ep == "execo":
        from minionize.execo import Execo

        engine = Execo.from_env()
    elif ep == "google":
        from minionize.google import GooglePubSub

        engine = GooglePubSub.from_env()
    else:
        raise Exception(f"EntryPoint {ep} not supported")
    return EntryPoint(callback, engine)
