import tiledb
import numpy as np
import pandas as pd

__author__ = "Jayaram Kancherla, Victor Alexandru"
__copyright__ = "jkanche, alexanv8"
__license__ = "mit"


class sceTileDB:
    """
    TileDB Class to parse single-cell folders.

    Args:
        path (str): local full path to an experiment inside a dataset.
            ex: tests/data/single-cell/GEPIVIZ_DS000010065/part_1

    Detail:
        The tiledb_folder should contain:
        TO DO
    """

    def __init__(self, path):
        self.path = path

    def extract_multiple_params(self, request_params):
        # composition
        pass

    def get_tSNE(self):
        return pd.read_csv(f'{self.path}/tSNE.tsv', sep='\t',
                           header=0, index_col=False)

    def get_UMAP(self):
        return pd.read_csv(f'{self.path}/UMAP.tsv', sep='\t',
                           header=0, index_col=False)

    def get_column(self, column_name):
        # column_name = ['cellTypeOntologyID']
        return pd.read_csv(f'{self.path}/cols.tsv', sep='\t',
                           header=0, index_col=False, usecols=column_name)

    def get_row(self, row_name):
        # row_name = ['symbol']
        return pd.read_csv(f'{self.path}/rows.tsv', sep='\t',
                           header=0, index_col=False, usecols=row_name)

    def get_index_from_df(self, df, names):
        col_name = df.columns[0]
        return df.index[df[col_name].isin(names)].tolist()

    def slice_by_gene(self, gene_names):
        genes = self.get_row(['symbol'])
        gene_indexes = self.get_index_from_df(genes, gene_names)
        # [1, 14698]

        gene_tuples = list(map(lambda x, y: (x, y), gene_indexes, gene_names))

        frames = []

        for gene_tuple in gene_tuples:
            print(gene_tuple)
            with tiledb.open(f'{self.path}/data.tiledb', 'r') as A:
                tiledb_arr = A[gene_tuple[0]+1:gene_tuple[0]+2, :]["vals"]
                df = pd.DataFrame(
                    tiledb_arr[0], index=None, columns=[gene_tuple[1]])

                frames.append(df)

        final_df = pd.concat(frames, axis=1)

        return final_df

    def getRange(self, chr, start=None, end=None, bins=2000, zoomlvl=-1, metric="AVG", respType="DataFrame", treedisk=None):
        pass
