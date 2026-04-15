import pandas as pd
from setuptools.command.install import install



df = pd.DataFrame({
    "id": [1, 2],
    "name": ["A", "B"]
})

df.to_parquet("data/sample.parquet")