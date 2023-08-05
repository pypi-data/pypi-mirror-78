import numpy as np
import pandas as pd
from .Describer import Describer


class DTypesDescriber(Describer):
    def get_section_header(self, column_list_threshold=6):
        return "Data types"

    def describe(self, df):
        assert isinstance(df, pd.DataFrame)

        messages = ["Columns by data type"]
        df_numeric = df.select_dtypes(np.number)
        df_dates = df.select_dtypes(np.datetime64)
        df_strings_or_objects = df.select_dtypes(object)
        df_other = df.select_dtypes(exclude=[np.number, np.datetime64, object])

        if len(df_numeric.columns) > 0:
            messages.append(f"- Numeric: {len(df_numeric.columns)}")

        if len(df_dates.columns) > 0:
            messages.append(f"- Date/times: {len(df_dates.columns)}")

        if len(df_strings_or_objects.columns) > 0:
            messages.append(f"- Objects/strings: {len(df_strings_or_objects.columns)}")

        if len(df_other.columns) > 0:
            messages.append(f"- Other types: {len(df_other.columns)}")

        return messages
