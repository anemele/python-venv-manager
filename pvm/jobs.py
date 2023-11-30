import subprocess
from pathlib import Path

from .consts import ROOT_PATH
from .log import logger


def is_venv(path: Path) -> bool:
    return (path / 'pyvenv.cfg').exists() and (path / 'Scripts').exists()


def list_envs():
    """list all envs"""
    logger.info(f'List {ROOT_PATH}')

    items = (f'  {it.name}' for it in ROOT_PATH.glob('*') if it.is_dir() and is_venv(it))
    print('Available envs:')
    print('\n'.join(items))


def activate(name: str):
    """activate an existing env"""
    venv_path = ROOT_PATH / name
    if not venv_path.exists():
        logger.error(f'not found: {name}')
    else:
        bat = venv_path / 'Scripts/activate.bat'
        subprocess.run(f'start cmd /k {bat}', shell=True)


# ** NOTICE ** #
# If you want to pass a numerical str, you should obey Python syntax.
# e.g. '3.10' instead of 3.10, where the latter will be interpreted as
# a float value 3.1
def create(name: str, *, version: str = '', overwrite: bool = False):
    """create a new env"""
    venv_path = ROOT_PATH / name

    if venv_path.exists() and not overwrite:
        logger.error(f'existing env: {name}')
        exit(1)

    config = [
        '--activators batch,powershell',
        '--no-setuptools',
        '--no-wheel',
        # '--system-site-packages'
    ]
    if version != '':
        config.append(f'--python {version}')
    config = ' '.join(config)

    cmd = f"virtualenv {venv_path} {config}"
    ret = subprocess.run(cmd).returncode
    if ret != 0:
        logger.error(f'failed to create: {name}')
        exit(ret)

    (venv_path / 'Scripts/idle.bat').write_text('@call %~dp0python.exe -m idlelib %*')


def remove(name: str):
    """remove an existing env"""
    venv_path = ROOT_PATH / name

    if not venv_path.exists():
        logger.error(f'not found: {name}')
        exit(1)
    if not is_venv(venv_path):
        logger.error(f'invalid env: {name}')
        exit(1)

    try:
        cp = subprocess.run(f'rd /s /q {venv_path}', shell=True)
        if cp.returncode == 0:
            logger.info(f'removed env: {name}')
        else:
            logger.error(f'failed to remove: {name}')
    except Exception as e:
        logger.error(e)
