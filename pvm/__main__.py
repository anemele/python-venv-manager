import fire

from .jobs import activate, create, list_envs, remove

if __name__ == '__main__':
    fire.Fire(
        {'add': create, 'ls': list_envs, 'rm': remove, 'use': activate}, name=__package__
    )
