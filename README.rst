==========
EFS Parser
==========

.. image:: https://readthedocs.org/projects/efs-parser/badge/?version=latest
    :target: https://efs-parser.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://github.com/epiviz/epivizFileParser/workflows/epivizFileParser/badge.svg
    :alt: epivizFileParser

Parse and Query Genomic File Formats

Description
===========
EFS parser provides parsers and utility methods to read and query commonly used genomic file formats. 
The results of the query are transformed into a Pandas DataFrame. This allows users to take 
advantage of many of the visual and analysis packages in the pandas/numpy ecosystem.

`Explore the docs 
<https://efs-parser.readthedocs.io>`_

Class information
=================

A new parser for a file format can be added to the package. The minimum skeleton 
is available in the `skeleton` directory


Developer Notes
===============

This project has been set up using PyScaffold 4. For details and usage
information on PyScaffold see https://pyscaffold.org/.

use a virtualenv for testing & development. 
To setup run the following commands from the project directory

.. code-block:: python

    virtualenv env --python=python3
    source env/bin/activate # (activate.fish if using the fish-shell)
    pip install -r requirements.txt

    # to deactivate virtualenv
    deactivate

1. Test - ```python setup.py test```
2. Docs - ```python setup.py docs```
3. Build
    - source distribution  ```python setup.py sdist```
    - binary distribution  ```python setup.py bdist```
    - wheel  distribution  ```python setup.py bdist_wheel```