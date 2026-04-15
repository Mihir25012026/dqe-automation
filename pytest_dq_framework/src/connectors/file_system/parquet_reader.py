import pandas as pd

class ParquetReader:
    def process(self, path):
        return pd.read_parquet(path)
