import pandas as pd

df = pd.read_parquet("robot_framework_project/parquet_data/facility_type_avg_time_spent_per_visit_date")

df_1 = df['facility_type'].unique()

print(df_1)