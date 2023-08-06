===========
 packinit
===========
-------------------------------------------------------------
 A container friendly startup routine for Packmaker servers.
-------------------------------------------------------------

|build-status| |coverage| |docs| |matrix| |discord|

Main Documentation
==================

**packinit** is a Python based startup routine for `Packmaker`_ based modded Minecraft servers. It can be run on any Linux system and in any container at present. It can be configured via environment variables, flags, and soon config files. (`ini`, `yaml` and `toml` formats are being considered)

It works by using `Packmaker`_ to download all mods based on a `Packmaker`_ yaml and lock file. It will download the latest mods, and sync the updated configuration and mods into the server directory in a stateful way that preserves runtime data, like the world.

Like `Packmaker`_, **packinit** can be given multiple pack files, which it will merge from first to last provided. This allows pack developers to release a server with pack related mods, and for server administrators to add their own maintenance packs, with mods for backup; sleep voting; and maps for example.

`Main Index`_

.. |build-status| image:: https://gitlab.routh.io/minecraft/tools/packinit/badges/main/pipeline.svg
    :target: https://gitlab.routh.io/minecraft/tools/packinit/pipelines

.. |coverage| image:: https://gitlab.routh.io/minecraft/tools/packinit/badges/main/coverage.svg
    :target: http://minecraft.pages.routh.io/tools/packinit/reports/
    :alt: Coverage status

.. |docs| image:: https://readthedocs.org/projects/packinit/badge/?version=stable
    :target: https://packinit.readthedocs.io/en/latest/?badge=stable
    :alt: Documentation Status

.. |matrix| image:: https://img.shields.io/matrix/minecraft-dev:routh.io.svg?server_fqdn=matrix.routh.io&label=%23minecraft-dev:routh.io&logo=matrix
    :target: https://matrix.to/#/#minecraft-dev:routh.io
    :alt: Matrix Channel

.. |discord| image:: https://img.shields.io/discord/236516692094615552?logo=discord
    :target: https://discord.gg/aCMZMPt
    :alt: Discord

.. _Main Index: https://packinit.readthedocs.io/en/latest/

.. _Packmaker: https://packmaker.readthedocs.io/
