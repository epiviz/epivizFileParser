from efs_parser.GtfParsedFile import GtfParsedFile

bb = GtfParsedFile("tests/genes.tsv.gz")
#bb = GtfParsedFile("genes.tsv.gz")

def test_columns():
    assert (bb.columns==['chr', 'start', 'end', 'width', 'strand', 'geneid', 'exon_starts', 'exon_ends', 'gene'])

def test_range():
    gf = bb.getRange('chr1', 11874, 944574)
    assert (len(gf[0]) == 33)

def test_search_existing_gene():
    sg = bb.search_gene('MIR6859-1')
    assert (len(sg[0])==3)
    assert (sg[0][0]['chr']=='chr1')
    assert (sg[0][1]['chr']=='chr15')
    assert (sg[0][2]['chr']=='chr16')

def test_search_no_gene():
    sg = bb.search_gene('')
    assert (sg==None)
