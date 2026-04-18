import pandas as pd


class DataQualityLibrary:
    """
    A library of static methods for performing data quality checks on pandas DataFrames.

    This class is intended to be used in a PyTest-based testing framework to validate
    the quality of data in DataFrames. Each method performs a specific data quality
    check and uses assertions to ensure that the data meets the expected conditions.
    """

    @staticmethod
    def check_duplicates(df, column_names=None):
        dup_count = df.duplicated(subset=column_names).sum()
        assert dup_count == 0, f"Duplicate keys found for {column_names}"

    @staticmethod
    def check_count(df1, df2):
        # Compare unique business keys instead of raw row count
        source_count = df1[['facility_type', 'visit_date']].drop_duplicates().shape[0]
        target_count = df2[['facility_type', 'visit_date']].drop_duplicates().shape[0]

        assert source_count == target_count, "Aggregated row count mismatch"

    @staticmethod
    def check_data_full_data_set(df1, df2):
        # Simple column match check
        assert set(df2.columns).issubset(set(df1.columns)), "Column mismatch"

    @staticmethod
    def check_dataset_is_not_empty(df):
        assert len(df) > 0, "Dataset is empty"

    @staticmethod
    def check_not_null_values(df, column_names=None):
        if column_names:
            for col in column_names:
                assert df[col].isnull().sum() == 0, f"Null values found in {col}"
        else:
            assert df.isnull().sum().sum() == 0, "Null values found in dataset"