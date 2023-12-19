import os
from pathlib import Path

from .log import logger

KEY = 'PYTHON_VENV_PATH'
PYTHON_VENV_PATH = os.environ.get(KEY)

if PYTHON_VENV_PATH is None:
    logger.error(f'no environment variable `{KEY}` set, exit')
    exit(1)

ROOT_PATH = Path(PYTHON_VENV_PATH)
if not ROOT_PATH.exists():
    logger.warning(f'not exists, mkdir: {ROOT_PATH}')
    ROOT_PATH.mkdir(parents=True)
