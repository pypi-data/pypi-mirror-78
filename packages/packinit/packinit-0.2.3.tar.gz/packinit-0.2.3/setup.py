# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['packinit', 'packinit.extra_files']

package_data = \
{'': ['*']}

install_requires = \
['packmaker==0.4.3']

entry_points = \
{'console_scripts': ['packinit = packinit:main']}

setup_kwargs = {
    'name': 'packinit',
    'version': '0.2.3',
    'description': 'A docker friendly startup routine for Minecraft servers.',
    'long_description': '===========\n packinit\n===========\n-------------------------------------------------------------\n A container friendly startup routine for Packmaker servers.\n-------------------------------------------------------------\n\n|build-status| |coverage| |docs| |matrix| |discord|\n\nMain Documentation\n==================\n\n**packinit** is a Python based startup routine for `Packmaker`_ based modded Minecraft servers. It can be run on any Linux system and in any container at present. It can be configured via environment variables, flags, and soon config files. (`ini`, `yaml` and `toml` formats are being considered)\n\nIt works by using `Packmaker`_ to download all mods based on a `Packmaker`_ yaml and lock file. It will download the latest mods, and sync the updated configuration and mods into the server directory in a stateful way that preserves runtime data, like the world.\n\nLike `Packmaker`_, **packinit** can be given multiple pack files, which it will merge from first to last provided. This allows pack developers to release a server with pack related mods, and for server administrators to add their own maintenance packs, with mods for backup; sleep voting; and maps for example.\n\n`Main Index`_\n\n.. |build-status| image:: https://gitlab.routh.io/minecraft/tools/packinit/badges/master/pipeline.svg\n    :target: https://gitlab.routh.io/minecraft/tools/packinit/pipelines\n\n.. |coverage| image:: https://gitlab.routh.io/minecraft/tools/packinit/badges/master/coverage.svg\n    :target: http://minecraft.pages.routh.io/tools/packinit/reports/\n    :alt: Coverage status\n\n.. |docs| image:: https://readthedocs.org/projects/packinit/badge/?version=stable\n    :target: https://packinit.readthedocs.io/en/latest/?badge=stable\n    :alt: Documentation Status\n\n.. |matrix| image:: https://img.shields.io/matrix/minecraft-dev:routh.io.svg?server_fqdn=matrix.routh.io&label=%23minecraft-dev:routh.io&logo=matrix\n    :target: https://matrix.to/#/#minecraft-dev:routh.io\n    :alt: Matrix Channel\n\n.. |discord| image:: https://img.shields.io/discord/236516692094615552?logo=discord\n    :target: https://discord.gg/aCMZMPt\n    :alt: Discord\n\n.. _Main Index: https://packinit.readthedocs.io/en/latest/\n\n.. _Packmaker: https://packmaker.readthedocs.io/\n',
    'author': 'Chris Routh',
    'author_email': 'chris@routh.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.routh.io/minecraft/tools/packinit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
