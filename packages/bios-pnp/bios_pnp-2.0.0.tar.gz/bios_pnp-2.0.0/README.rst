========
bios_pnp
========

Very simple module that enumerates Legacy Plug and Play devices.

Currently only Linux is supported. The data is sourced from the sysfs
file system.

Example::

  >>> from bios_pnp import pnp
  >>> print(list(pnp.get_all_pnp_devices_from_sysfs()))
  [Device(ids=[DeviceId(vendor=PNP, product=0x0b0, revision=0x0)])]


License
=======

Apache 2.0
