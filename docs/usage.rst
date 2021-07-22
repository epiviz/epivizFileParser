=====
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
