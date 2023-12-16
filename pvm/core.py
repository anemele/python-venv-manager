import shutil
import subprocess as sbp
from pathlib import Path

from .consts import ROOT_PATH
from .log import logger

BIN_DIR = "Scripts"


def is_venv(path: Path) -> bool:
    return (path / "pyvenv.cfg").exists() and (path / BIN_DIR).exists()


def list_envs():
    """list all envs"""
    root = str(ROOT_PATH).replace(str(Path.home()), "~", 1)
    logger.info(f"list {root}")

    items = "".join(f"  {it.name:<10s}" for it in ROOT_PATH.glob("*") if is_venv(it))
    print("Available envs:")
    print(items)


def activate(name: str, use_pwsh: bool):
    """activate an existing env"""
    venv_path = ROOT_PATH / name

    if not is_venv(venv_path):
        logger.error(f"not found: {name}")
    elif use_pwsh:
        act = venv_path / BIN_DIR / "activate.ps1"
        sbp.run(f"start pwsh -NoExit -Command {act}", shell=True)
    else:
        act = venv_path / BIN_DIR / "activate.bat"
        sbp.run(f"start cmd /k {act}", shell=True)


def create(name: str, *, version: str | None = None, overwrite: bool = False):
    """create a new env"""
    venv_path = ROOT_PATH / name

    if venv_path.exists() and not overwrite:
        logger.error(f"existing env: {name}")
        return

    config = [
        "--activators batch,powershell",
        "--no-setuptools",
        "--no-wheel",
        # '--system-site-packages',
        "--no-vcs-ignore",
        # '--no-pip',
    ]
    if version is not None:
        config.append(f"--python {version}")
    config = " ".join(config)

    cmd = f"virtualenv {venv_path} {config}"
    if sbp.run(cmd).returncode != 0:
        logger.error(f"failed to create: {name}")
        return

    # idle for Windows
    (venv_path / BIN_DIR / "idle.bat").write_text("@call %~dp0python.exe -m idlelib %*")


def remove(name: str):
    """remove an existing env"""
    venv_path = ROOT_PATH / name

    if not is_venv(venv_path):
        logger.error(f"not an env: {name}")
        return

    try:
        shutil.rmtree(venv_path)
        logger.info(f"removed env: {name}")
    except Exception as e:
        logger.error(e)
