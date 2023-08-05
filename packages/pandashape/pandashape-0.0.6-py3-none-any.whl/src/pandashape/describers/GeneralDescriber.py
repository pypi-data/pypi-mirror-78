from .Describer import Describer


class GeneralDescriber(Describer):
    TEMP_SKEW_THRESHOLD = 0.4

    def get_section_header(self):
        return "General frame info"

    def describe(self, df):
        messages = [f"Shape: {df.shape}"]

        # NULLS
        columns_with_nulls = df.columns[df.isna().any()].array.to_numpy()
        if len(columns_with_nulls) > 0:
            messages.append(
                f"Columns with one or more null values: {columns_with_nulls}"
            )

        # LE CANDIDATES
        object_typed_columns = df.select_dtypes(
            include='object').columns.array.to_numpy()

        if len(object_typed_columns) > 0:
            messages.append(
                f"Columns of type \"object\" (may need label encoding): {object_typed_columns}"
            )

        return messages
