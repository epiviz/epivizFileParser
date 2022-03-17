import tiledb
import numpy as np
import pandas as pd

from .utils import dense_to_sparse

__author__ = "Jayaram Kancherla, Victor Alexandru"
__copyright__ = "jkanche, alexanv8"
__license__ = "mit"


class sceTileDB:
    """
    TileDB Class to parse single-cell folders.
    Args:
        path (str): local full path to directory for an experiment inside a dataset.
            ex: tests/data/<dataset_id>/<experiment_id>
    Detail:
        The experiment directory should contain:
            - cols.tsv
            - rows.tsv
            - <dimension>.tsv ex: tSNE.stv
            - data.tiledb
    """

    def __init__(self, path):
        self.path = path
        self.genes = self.get_features("symbol")

    def get_metadata(self):
        pass

    def get_dimensionality(self, dimension):
        try:
            result = pd.read_csv(
                f"{self.path}/{dimension}.tsv", sep="\t", header=0, index_col=False
            )
        except:
            raise Exception(f"{dimension} is missing in this dataset.")
        return result

    def get_annotation(self, annotation):
        try:
            result = pd.read_csv(
                f"{self.path}/cols.tsv",
                sep="\t",
                header=0,
                index_col=False,
                usecols=[annotation],
            )
        except:
            raise Exception(f"{annotation} is missing in this dataset.")
        return result

    def get_features(self, feature):
        try:
            result = pd.read_csv(
                f"{self.path}/rows.tsv",
                sep="\t",
                header=0,
                index_col=False,
                usecols=[feature],
            )
        except:
            raise Exception(f"{feature} is missing in this dataset.")
        return result

    def get_index_from_df(self, df, names, case_sensitivity=False):
        col_name = df.columns[0]

        for name in names:
            if not df[col_name].str.contains(name, case=case_sensitivity).any():
                raise Exception(f"{name} does not exist")

        return df.index[df[col_name].isin(names)].tolist()

    def gene_expression(
        self, genes, summary: bool = False, precision: int = None, sparse: bool = True
    ):
        genes_df = self.genes
        gene_indexes = self.get_index_from_df(genes_df, genes)

        response = {}

        with tiledb.open(f"{self.path}/data.tiledb", "r") as A:
            tiledb_np_array = A.multi_index[gene_indexes, :]["vals"]

            if precision is not None:
                tiledb_np_array = np.round(tiledb_np_array, precision)

            if sparse:
                expression = dense_to_sparse(tiledb_np_array, genes)
            else:
                expression = {"data": tiledb_np_array.tolist()}

            response["data"] = expression

            if summary:
                response["summary"] = {
                    "max": np.amax(tiledb_np_array, axis=1).tolist(),
                    "min": np.amin(tiledb_np_array, axis=1).tolist(),
                    "mean": np.round(
                        np.mean(tiledb_np_array, axis=1), precision
                    ).tolist(),
                    "prevalence": np.round(
                        (
                            np.count_nonzero(tiledb_np_array, axis=1)
                            / np.size(tiledb_np_array, axis=1)
                            * 100
                        ),
                        precision,
                    ).tolist(),
                }

        response["genes"] = genes

        return response
