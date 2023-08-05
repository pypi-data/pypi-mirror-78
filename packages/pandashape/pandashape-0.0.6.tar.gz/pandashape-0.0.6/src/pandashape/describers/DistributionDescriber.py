from numpy.lib.arraysetops import unique
from .Describer import Describer
import numpy as np
from scipy import stats


class DistributionDescriber(Describer):
    def __init__(self, outlier_threshold=2, skewness_threshold=0.4):
        self.outlier_threshold = outlier_threshold
        self.skewness_threshold = skewness_threshold

    def get_section_header(self):
        return "Distribution"

    def describe(self, df):
        messages = []
        columns_to_analyze = df.select_dtypes(include=np.number)

        # skip columns that only have two values and are thus very likely categorical/binary
        columns_to_analyze = [col for col in columns_to_analyze if len(df[col].unique()) > 2]

        # track outliers for reporting
        outlier_columns = []

        for column_name in columns_to_analyze:
            # zscore becomes a numpy array
            zscores = np.abs(stats.zscore(df[column_name]))
            # i had no idea this was a thing, but apparently it is
            outliers_filter = zscores > self.outlier_threshold
            outliers = zscores[outliers_filter]
            outlier_count = len(outliers)

            if outlier_count > 0:
                outlier_columns.append({
                    'column_name': column_name,
                    'count': outlier_count
                })

        if len(outlier_columns) > 0:
            messages.append(
                f"These columns have significant outlier values (more than +/- {self.outlier_threshold} standard deviations from the mean).")

            for outlier_column in outlier_columns:
                messages.append(f"- {outlier_column['column_name']} ({outlier_column['count']})")

        # skew
        skewness = df.skew()
        skewed_keys = []

        for column in columns_to_analyze:
            # skewness.keys()
            if abs(1-skewness[column]) >= self.skewness_threshold:
                skewed_keys.append(column)

        if len(skewed_keys) > 0:
            messages.append("")
            messages.append(
                f"These columns are skewed beyond the threshold of 1 +/- {self.skewness_threshold}. You may want to scale them somehow.")

            for key in skewed_keys:
                messages.append(f" - {key} ({skewness[key]})")

        return messages
