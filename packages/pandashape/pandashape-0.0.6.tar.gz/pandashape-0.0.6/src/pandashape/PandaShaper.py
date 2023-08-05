import pandas as pd
from .enums.Columns import Columns
from .describers import GeneralDescriber, DistributionDescriber, DTypesDescriber
from .internal import DescriberExecutor, TransformerExecutor


class PandaShaper:
    def __init__(self, df, inplace=False):
        assert(isinstance(df, pd.DataFrame))
        self.df = df.copy() if not inplace else df

    def describe(self, describers=[GeneralDescriber, DTypesDescriber, DistributionDescriber], columns=Columns.All):
        executor = DescriberExecutor()
        executor.describe(self.df, describers, columns)

    def transform(self, columnDefinitions):
        executor = TransformerExecutor()
        return executor.transform(self.df, columnDefinitions)
