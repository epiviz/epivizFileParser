==========================================
Efs Parser - Read and Query genomic files.
===========================================

The package providies utilties to parse and query commonly used genomic file formats. 
Genomic files are usually indexed (BigWig, BigBed, Tabix etc) and the library will only
read the necessary bytes of the file to query data. In addition, The library also works with
remotely hosted files. This requires the remotely hosted file to support HTTP Byte-Range requests 

.. note::

    - package is open source and is available on `GitHub <https://github.com/epiviz/epivizFileParser>`_


Installation
============

Using PyPI
=========

will be on PyPI soon.. but for now install from GitHub below


From GitHub (devel version)
===========================

To install the devel version from `GitHub
<https://github.com/epiviz/epivizFileParser>`__: Install using pip

.. code-block:: console

    pip install git@github.com:epiviz/epivizFileParser.git

or clone the repository and install from local directory using `pip`

.. note::

    Depending on how python was setup, installing packages
    may sometime require sudo permission, in this case, add 
    the --user option 

    .. code-block:: console

        pip install --user git@github.com:epiviz/epivizFileParser.git

Usage
=====

For example, to read a BigWig file, 

.. code-block:: python

    from epivizFileParser import BigWig
    
    # initialize a file
    bw = BigWig("tests/test.bw")

    # extract header and zoom levels from the file
    print(bw.header, bw.zooms)

    # query the file
    res, err = bw.getRange(chr="chr1", start=10000000, end=10020000)
    print(res)

    # summarize data into equals windows/bins
    sres = bw.bin_rows(res, chr="chr1", start=10000000, end=10020000, columns=['score'], bins=10)
    print(sres)


Contents
========

.. toctree::
   :maxdepth: 2

   Installation <installation>
   Usage <usage>
   License <license>
   Authors <authors>
   Changelog <changelog>
   Module Reference <api/modules>


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _toctree: http://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html
.. _reStructuredText: http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
.. _references: http://www.sphinx-doc.org/en/stable/markup/inline.html
.. _Python domain syntax: http://sphinx-doc.org/domains.html#the-python-domain
.. _Sphinx: http://www.sphinx-doc.org/
.. _Python: http://docs.python.org/
.. _Numpy: http://docs.scipy.org/doc/numpy
.. _SciPy: http://docs.scipy.org/doc/scipy/reference/
.. _matplotlib: https://matplotlib.org/contents.html#
.. _Pandas: http://pandas.pydata.org/pandas-docs/stable
.. _Scikit-Learn: http://scikit-learn.org/stable
.. _autodoc: http://www.sphinx-doc.org/en/stable/ext/autodoc.html
.. _Google style: https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings
.. _NumPy style: https://numpydoc.readthedocs.io/en/latest/format.html
.. _classical style: http://www.sphinx-doc.org/en/stable/domains.html#info-field-lists
