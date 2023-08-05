=================================================================================================
A simple CLI toolbox to use the `European Nucleotide Archive (ENA) <https://www.ebi.ac.uk/ena/>`_
=================================================================================================

.. image:: https://img.shields.io/badge/license-apache2-brightgreen.svg
   :target: https://github.com/auwerxlab/ena-utils/blob/master/LICENSE

.. image:: https://img.shields.io/github/v/release/auwerxlab/ena-utils
   :target: https://github.com/auwerxlab/ena-utils/releases

.. image:: https://img.shields.io/pypi/v/ena-utils
   :target: https://pypi.python.org/pypi/ena-utils

.. image:: https://readthedocs.org/projects/ena-utils/badge/?version=latest
   :target: https://ena-utils.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


**ena-utils** is a small python package that provides a CLI to submit nucleotides sequences to the `European Nucleotide Archive (ENA) <https://www.ebi.ac.uk/ena/>`_.

Supported submission types
==========================

- Reads

Features
========

- File upload
- Study registration
- Experiment registration
- Run registration
- Sample registration

Requirements
============

- Python3
- Webin account

Installation
============

The latest release is available on PyPI and can be installed using ``pip``:

::

    $ pip install ena-utils

Isolated environments using ``pipx``
------------------------------------

Install and execute ena-utils in an isolated environment using ``pipx``.

`Install pipx <https://github.com/pipxproject/pipx#install-pipx>`_
and make sure that the ``$PATH`` is correctly configured.

::

    $ python3 -m pip install --user pipx
    $ pipx ensurepath

Once ``pipx`` is installed use following command to install ``ena-utils``.

::

    $ pipx install ena-utils
    $ which ena-utils
    ~/.local/bin/ena-utils

Usage
=====

The latest documentation is available at `https://readthedocs.org <https://ena-utils.readthedocs.io/en/latest/>`_.
