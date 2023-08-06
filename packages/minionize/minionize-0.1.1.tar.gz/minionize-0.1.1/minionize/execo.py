import logging
from pathlib import Path
import traceback
import os

from execo_engine.sweep import ParamSweeper

from . import Callback

LOGGER = logging.getLogger(__name__)

from . import Engine
from .types import Param

ENV_PERSISTENCE_DIR = "EXECO_PERSISTENCE_DIR"
DEFAULT_PERSISTENCE_DIR = Path("sweeps")


class Execo(Engine):
    def __init__(self, persistence_dir: Path):
        self.sweeper = ParamSweeper(str(persistence_dir))

    def get_next(self) -> Param:
        return self.sweeper.get_next()

    def done(self, param: Param):
        self.sweeper.done(param)

    def skip(self, param: Param):
        self.sweeper.skip(param)

    @classmethod
    def from_env(cls):
        persistence_dir = os.environ.get(ENV_PERSISTENCE_DIR, DEFAULT_PERSISTENCE_DIR)
        return cls(persistence_dir)
