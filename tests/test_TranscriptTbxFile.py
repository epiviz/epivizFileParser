from efs_parser.TranscriptTbxFile import TranscriptTbxFile

#ee = TranscriptTbxFile("transcripts.tsv.bgz")
ee = TranscriptTbxFile("tests/transcripts.tsv.bgz")
def test_columns():
    assert (ee.columns==['chr', 'start', 'end', 'strand', 'transcript_id', 'exon_starts', 'exon_ends', 'gene'])

def test_range():
    gf= ee.getRange('chr1',11874,944574)
    assert (len(gf[0]) == 46)

