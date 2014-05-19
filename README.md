repository.libretro
===================

This repository contains libretro game add-ons for XBMC.

Root directories
---------------
* /addons - Auxiliary files for add-ons (icon.png, etc)
* /libretro-extract - A program to extract information from libretro shared libraries
* /libretro-super - Created by create_release.py. Cloned from [libretro-super](https://github.com/libretro/libretro-super)
* /release - Release archives
* /src - Python scripts to create release archives (see create_release.py)

Status
-----
create_release.py copies compiled libretro libraries and partially-generated addon.xml files into /addons

TODO
----
* Save .md5 and changelog files next to generated archives

