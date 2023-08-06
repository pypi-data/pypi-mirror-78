__author__ = 'Gabriel Salgado and Moises Mendes'
__version__ = '0.7.1'
__description__ = 'This project build pipelines for resolution score for Take BLiP'

from .run import run
from .utils import load_params, load_pipelines, sparksql_ops
from .core import Pipeline
from .bot_flow import bot_flow
