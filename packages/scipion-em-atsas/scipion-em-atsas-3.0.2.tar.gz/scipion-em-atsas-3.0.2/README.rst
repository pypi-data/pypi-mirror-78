============
ATSAS plugin
============

This plugin is wrapping ATSAS programs from http://www.embl-hamburg.de/biosaxs/software.html

Installation
------------

You will need to use `3.0 <https://github.com/I2PC/scipion/releases/tag/V3.0.0>`_ version of Scipion to be able to run these protocols. To install the plugin, you have two options:

a) Stable version

.. code-block::

    scipion installp -p scipion-em-atsas

b) Developer's version

    * download repository

    .. code-block::

        git clone https://github.com/scipion-em/scipion-em-atsas.git

    * install

    .. code-block::

        scipion installp -p path_to_scipion-em-atsas --devel

Supported versions
------------------

2.8.2, 3.0.1

Protocols
---------

    * convert PDB to SAXS curve
