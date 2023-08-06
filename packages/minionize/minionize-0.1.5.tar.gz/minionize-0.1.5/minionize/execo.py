import logging
from pathlib import Path
import os

from execo_engine.sweep import ParamSweeper

from . import Engine
from .types import Param

LOGGER = logging.getLogger(__name__)

ENV_PERSISTENCE_DIR = "EXECO_PERSISTENCE_DIR"
DEFAULT_PERSISTENCE_DIR = Path("sweeps")


class Execo(Engine):
    def __init__(self, persistence_dir: Path):
        self.sweeper = ParamSweeper(str(persistence_dir))

    def next(self) -> Param:
        return self.sweeper.get_next()

    def ack(self, param: Param):
        self.sweeper.done(param)

    def nack(self, param: Param):
        self.sweeper.skip(param)

    @classmethod
    def from_env(cls):
        persistence_dir = os.environ.get(ENV_PERSISTENCE_DIR, DEFAULT_PERSISTENCE_DIR)
        return cls(persistence_dir)
