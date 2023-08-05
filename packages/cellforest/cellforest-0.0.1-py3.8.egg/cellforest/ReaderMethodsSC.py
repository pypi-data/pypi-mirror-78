import pickle

import pandas as pd
from pathlib import Path
from scipy import io

from dataforest.utils.decorators import default_kwargs


class ReaderMethodsSC:
    TSV_DEFAULTS = {"sep": "\t", "header": None}
    TSV_GZ_DEFAULTS = {**TSV_DEFAULTS, "compression": "gzip"}
    PICKLE_DEFAULTS = {}

    @staticmethod
    @default_kwargs(TSV_DEFAULTS)
    def tsv(filepath, **kwargs):
        df = pd.read_csv(filepath, **kwargs)
        return df

    @staticmethod
    @default_kwargs(TSV_GZ_DEFAULTS)
    def tsv_gz(filepath, **kwargs):
        defaults = {"sep": "\t", "compression": "gzip", "header": None}
        defaults.update(kwargs)
        kwargs = defaults
        df = pd.read_csv(filepath, **kwargs)
        return df

    @staticmethod
    @default_kwargs(PICKLE_DEFAULTS)
    def pickle(filepath, **kwargs):
        with Path(filepath).open("rb") as f:
            mat = pickle.load(f, **kwargs)
        return mat

    @staticmethod
    def rds(filepath):
        raise NotImplementedError()

    @staticmethod
    def mtx_gz(filepath):
        return io.mmread(str(filepath))
