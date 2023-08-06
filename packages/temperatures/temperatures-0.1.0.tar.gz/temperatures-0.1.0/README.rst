==============
 temperatures
==============

``temperatures`` is a Python program that gathers temperatures from hard
disks, CPU and GPU and presents them in a concise string suitable to be
fed to XFCE's Generic Monitor panel plugin or similar.

https://github.com/luismsgomes/temperatures

Copyright (c) 2020 Luís Gomes <luismsgomes@gmail.com>

Usage
-----

This program takes no input and no options.

It is assumed that `hddtempd` daemon is running and listening on port 7634.

Presently the program is not configurable and works for my particular hardware, which
includes and AMD Ryzen CPU, an AMD Radeon RX 590 GPU and some HDDs.  I'm not
particularly interested in SSDs temperatures, so I leave those out.

In the future I may extend the code to allow:

* configurable devices
* configurable output format
* continuous run, outputing a new line at regular intervals

