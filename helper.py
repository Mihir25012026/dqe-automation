import pandas as pd
from robot.libraries.BuiltIn import BuiltIn


def read_html_table():
    driver = BuiltIn().get_library_instance('SeleniumLibrary').driver

    table = driver.find_element("class name", "table")
    columns = table.find_elements("class name", "y-column")

    headers = []
    column_data = []

    for col in columns:
        header = col.find_element("id", "header").text.strip()
        headers.append(header)

        cells = col.find_elements("class name", "cell-text")
        values = [c.text.strip() for c in cells if c.text.strip() != header]
        column_data.append(values)

    rows = list(zip(*column_data))
    df = pd.DataFrame(rows, columns=headers)

    # Normalize data types
    df['Visit Date'] = pd.to_datetime(df['Visit Date'], dayfirst=True)
    df['Average Time Spent'] = df['Average Time Spent'].astype(float)

    return df


def read_parquet_data(path, filter_date=None):
    df = pd.read_parquet(path)

    df['visit_date'] = pd.to_datetime(df['visit_date'])

    if filter_date:
        df = df[df['visit_date'].dt.strftime('%Y-%m') == filter_date[:7]]

    # Rename to match HTML
    df = df.rename(columns={
        'facility_type': 'Facility Type',
        'visit_date': 'Visit Date',
        'avg_time_spent': 'Average Time Spent'
    })

    df['Average Time Spent'] = df['Average Time Spent'].astype(float)

    return df[['Facility Type', 'Visit Date', 'Average Time Spent']]


def compare_dataframes(df1, df2):
    df1_sorted = df1.sort_values(by=df1.columns.tolist()).reset_index(drop=True)
    df2_sorted = df2.sort_values(by=df2.columns.tolist()).reset_index(drop=True)

    # If shapes differ → mismatch
    if df1_sorted.shape != df2_sorted.shape:
        return False, f"Row count mismatch: HTML={df1_sorted.shape[0]}, Parquet={df2_sorted.shape[0]}"

    # If equal → compare values
    if df1_sorted.equals(df2_sorted):
        return True, None

    diff = pd.concat([df1_sorted, df2_sorted]).drop_duplicates(keep=False)
    return False, diff