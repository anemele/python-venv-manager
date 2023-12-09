from venv import logger

import click

from .core import activate, create, list_envs, remove


# https://github.com/pallets/click/issues/513#issuecomment-504158316
# https://zhuanlan.zhihu.com/p/73426505
# requires v3.6+
class OrderedGroup(click.Group):
    def list_commands(self, _):
        return self.commands.keys()


@click.group(cls=OrderedGroup)
def cli():
    """Python Virtual env Manager"""


@cli.command(help=list_envs.__doc__)
def ls():
    list_envs()


@cli.command(help=create.__doc__)
@click.argument('name')
@click.option('-v', '--version', help='specify the Python version (preinstalled)')
@click.option('-f', '--force', is_flag=True, help='overwrite if exists')
def add(name: str, version: str | None, force: bool):
    logger.debug(f'{version=}')
    logger.debug(f'{force=}')
    create(name, version=version, overwrite=force)


@cli.command(help=remove.__doc__)
@click.argument('name')
def rm(name: str):
    remove(name)


@cli.command(help=activate.__doc__)
@click.argument('name')
def use(name: str):
    activate(name)
