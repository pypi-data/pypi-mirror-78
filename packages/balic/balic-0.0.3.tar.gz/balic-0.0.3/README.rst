README
======

`Balič` (read `balitch`) is a command-line toolset for working with LXC containers.

| |license| |downloads|
| |status| |format| |wheel|
| |version| |pyversions| |implementation|
| |coverage|

.. |version| image:: https://img.shields.io/pypi/v/balic
   :target: https://pypi.org/project/balic/
   :alt: PyPI - Version

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/balic
   :target: https://pypi.org/project/balic/
   :alt: PyPI - Python Versions

.. |implementation| image:: https://img.shields.io/pypi/implementation/balic
   :target: https://pypi.org/project/balic/
   :alt: PyPI - Implementation

.. |downloads| image:: https://img.shields.io/pypi/dm/balic
   :target: https://pypi.org/project/balic/
   :alt: PyPI - Downloads

.. |license| image:: https://img.shields.io/pypi/l/balic
   :target: https://pypi.org/project/balic/
   :alt: PyPI - License

.. |format| image:: https://img.shields.io/pypi/format/balic
   :target: https://pypi.org/project/balic/
   :alt: PyPI - Format

.. |status| image:: https://img.shields.io/pypi/status/balic
   :target: https://pypi.org/project/balic/
   :alt: PyPI - Status

.. |wheel| image:: https://img.shields.io/pypi/wheel/balic
   :target: https://pypi.org/project/balic/
   :alt: PyPI - Wheel

.. |coverage| image:: https://codecov.io/gl/markuz/balic/branch/master/graph/badge.svg
   :target: https://codecov.io/gl/markuz/balic
   :alt: coverage.io report

Installation
------------

Install ``balic`` via ``pip``::

    pip install balic


``Balic`` requires the following packages installed::

    appdirs
    cliff


Usage
-----

::

    balic create -n test                 # creates lxc container names test
    balic build -n test -d build_dir     # builds test lxc container using content of build_dir*
    balic pack -n test -o rootfs.tar.gz  # packs test lxc container into rootfs.tar.gz
    balic destroy -n test                # destroy test lxc container



Documentation
-------------

Source of the documentaton is available in the `Balic` repository
https://gitlab.com/markuz/balic/tree/master/docs/source


Development
-----------

Pull requests welcomed.

``Balic`` git repository is available at https://gitlab.com/markuz/balic

For more information, see https://gitlab.com/markuz/balic/-/blob/master/docs/source/development.rst


License
-------

`BSD 3-clause Clear License <https://gitlab.com/markuz/balic/blob/master/LICENSE>`_
