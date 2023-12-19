import click

from .core import activate, create, list_envs, remove
from .log import logger


# https://github.com/pallets/click/issues/513#issuecomment-504158316
# https://zhuanlan.zhihu.com/p/73426505
# requires v3.6+
class OrderedGroup(click.Group):
    def list_commands(self, _):  # type: ignore
        return self.commands.keys()


@click.group(cls=OrderedGroup)
def cli():
    """Python Virtual env Manager"""


@cli.command(help=list_envs.__doc__)
def ls():
    list_envs()


@cli.command(help=create.__doc__)
@click.argument("name", nargs=-1, required=True)
@click.option("-v", "--version", help="specify the Python version (preinstalled)")
@click.option("-f", "--force", is_flag=True, default=False, help="overwrite if exists")
def add(name: tuple[str], version: str | None, force: bool):
    logger.debug(f"{name=}")
    logger.debug(f"{version=}")
    logger.debug(f"{force=}")
    for it in name:
        create(it, version=version, overwrite=force)


@cli.command(help=remove.__doc__)
@click.argument("name", nargs=-1, required=True)
def rm(name: tuple[str]):
    logger.debug(f"{name=}")
    for it in name:
        remove(it)


@cli.command(help=activate.__doc__)
@click.argument("name", nargs=-1, required=True)
@click.option("--pwsh", is_flag=True, default=False, help="use pwsh activator")
def use(name: tuple[str], pwsh: bool):
    logger.debug(f"{name=}")
    logger.debug(f"{pwsh=}")
    for it in name:
        activate(it, pwsh)
