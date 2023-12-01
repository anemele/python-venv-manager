from typing import Optional
from venv import logger

import click

from .jobs import activate, create, list_envs, remove


@click.group()
def cli():
    '''Python Virtual env Manager'''


@cli.command(help=list_envs.__doc__)
def ls():
    list_envs()


@cli.command(help=activate.__doc__)
@click.argument('name')
def use(name: str):
    activate(name)


@cli.command(help=remove.__doc__)
@click.argument('name')
def rm(name: str):
    remove(name)


@cli.command(help=create.__doc__)
@click.argument('name')
@click.option('-v', '--version', help='specify the Python version (preinstalled)')
@click.option('-f', '--force', is_flag=True, help='overwrite if exists')
def add(name: str, version: Optional[str], force: bool):
    logger.debug(f'{version=}')
    logger.debug(f'{force=}')
    create(name, version=version, overwrite=force)
