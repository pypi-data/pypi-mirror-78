# -*- coding: utf-8 -*-
from io import StringIO, BytesIO

import pandas as pd


def to_file(df: pd.DataFrame, file_type: str = None):
    if file_type == "csv":
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        data = csv_buffer.getvalue()
    else:
        pq_buffer = BytesIO()
        df.to_parquet(pq_buffer)
        data = pq_buffer.getvalue()

    return data


def from_file(data, file_type: str = None):
    if file_type == "csv":
        return pd.read_csv(StringIO(data.decode("utf-8")))
    elif file_type == "parquet":
        return pd.read_parquet(BytesIO(data))
    else:
        raise ValueError("Other file types than 'csv' and 'parquet are not supported'")
