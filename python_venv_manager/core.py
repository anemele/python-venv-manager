import subprocess as sbp
from pathlib import Path

from .consts import ROOT_PATH
from .log import logger


def is_venv(path: Path) -> bool:
    return (path / "pyvenv.cfg").exists() and (path / "Scripts").exists()


def list_envs():
    """list all envs"""
    root = str(ROOT_PATH).replace(str(Path.home()), "~", 1)
    logger.info(f"list {root}")

    items = (f"  {it.name}" for it in ROOT_PATH.glob("*") if is_venv(it))
    print("Available envs:")
    print("\n".join(items))


def activate(name: str, use_pwsh: bool):
    """activate an existing env"""
    if not isinstance(name, str):
        name = str(name)

    venv_path = ROOT_PATH / name

    if not venv_path.exists():
        logger.error(f"not found: {name}")
    elif use_pwsh:
        act = venv_path / "Scripts/activate.ps1"
        sbp.run(f"start pwsh -NoExit -Command {act}", shell=True)
    else:
        act = venv_path / "Scripts/activate.bat"
        sbp.run(f"start cmd /k {act}", shell=True)


def create(name: str, *, version: str | None = None, overwrite: bool = False):
    """create a new env"""
    if not isinstance(name, str):
        name = str(name)

    venv_path = ROOT_PATH / name

    if venv_path.exists() and not overwrite:
        logger.error(f"existing env: {name}")
        exit(1)

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
    ret = sbp.run(cmd).returncode
    if ret != 0:
        logger.error(f"failed to create: {name}")
        exit(ret)

    (venv_path / "Scripts/idle.bat").write_text("@call %~dp0python.exe -m idlelib %*")


def remove(name: str):
    """remove an existing env"""
    if not isinstance(name, str):
        name = str(name)

    venv_path = ROOT_PATH / name

    if not venv_path.exists():
        logger.error(f"not found: {name}")
        exit(1)
    if not is_venv(venv_path):
        logger.error(f"invalid env: {name}")
        exit(1)

    try:
        cp = sbp.run(f"rd /s /q {venv_path}", shell=True)
        if cp.returncode == 0:
            logger.info(f"removed env: {name}")
        else:
            logger.error(f"failed to remove: {name}")
    except Exception as e:
        logger.error(e)
