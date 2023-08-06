from abc import ABC, abstractmethod
import logging
import os
import traceback

from dotenv import load_dotenv

from .types import Param

# first thing first ... load dotenv file if any
load_dotenv()

LOGGER = logging.getLogger(__name__)

ENV_ENGINE = "MINION_ENGINE"
ENV_DRY_MODE = "DRY"


class Engine(ABC):
    """Base class for our Engines.

    An engine is responsible for getting data(param) from a queue.
    It acknowleges (positively or negatively) the data back to the queue.
    The exact semantic of ack/nack is still under intense discussion. Please
    refer to the concrete implementation for further information.
    """

    @abstractmethod
    def next(self) -> Param:
        pass

    @abstractmethod
    def ack(self, param: Param):
        pass

    @abstractmethod
    def nack(self, param: Param):
        pass


class Callback(ABC):
    """Base class for the (user defined) callbacks.

    A Callback modelizes the behaviour of the application inputs/outputs.
    """

    @abstractmethod
    def setup(self, param: Param, engine: Engine):
        """Called right after a new param is fetched from the queue."""
        pass

    @abstractmethod
    def process(self, param: Param, engine: Engine):
        """This is where process will happen."""
        pass

    @abstractmethod
    def teardown(self, param: Param, engine: Engine, exception: Exception):
        """Called at the before a new iteration."""
        pass

    def dry_mode(self):
        return os.getenv(ENV_DRY_MODE) is not None


class PrintCallback(Callback):
    """Dummy callback for debug purpose.

    Acknowledges right after printing. It never uses nack.
    """

    def setup(self, param, engine):
        print(f"setup {param}")

    def process(self, param, engine):
        print(f"process {param}")
        engine.done(param)

    def teardown(self, param, engine, exception):
        print(f"finished {param}")


class ProcessCallback(Callback):
    """A callback that spawn a process upon reception.

    It's designed to be a good enough callback for most use cases. User must
    subclass it and define how the actual shell command is built from the
    incoming param.
    - Acknowlege if the sub process return code is 0
    - Nack otherwise
    """

    def to_cmd(self, param: Param):
        return f"echo {param}"

    def setup(self, param, engine):
        return super().setup(param, engine)

    def process(self, param: Param, engine: Engine):
        import subprocess

        if self.dry_mode():
            print(f"[dry mode] {self.to_cmd(param)}")
        else:
            try:
                subprocess.run(self.to_cmd(param), shell=True, check=True)
                engine.ack(param)
            except Exception as e:
                engine.nack(param)
                raise e

    def teardown(self, param, engine, exception):
        return super().teardown(param, engine, exception)


class EntryPoint:
    """This is the framework.

    It's mainly a loop that continuously fetch the next param and call the
    callback methods.
    """

    def __init__(self, callback: Callback, engine: Engine):
        self.cb = callback
        self.engine = engine

    def run(self):
        """Routine."""
        while True:
            LOGGER.debug("get next param")
            param = self.engine.next()
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
            self.cb.teardown(param, self.engine, exception)


def minionizer(callback: Callback):
    """Take a user callback and minionize it !"""
    # NOTE(msimonin): use dotenv
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
