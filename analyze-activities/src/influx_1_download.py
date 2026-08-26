"""Download data from Influx DB."""

from pathlib import Path

import pandas as pd
from influxdb import DataFrameClient

from influx_creds import creds

FILE_OUT = Path("data/influx-media.csv")
RETENTION = "y1"
MEASUREMENT = "Shelly_y1"
# TODO: only download new lines
QUERY = (
    f'SELECT ShellyNo, watt_now FROM "{RETENTION}"."{MEASUREMENT}" WHERE ShellyNo = 3'  # noqa: S608 #nosec
)
# watt_now is more stable than watt_last, maybe the time is not that stable?


def connect2_df(creds: dict) -> DataFrameClient:
    """
    Connect to DB.

    copied from my private Raspi repo
    """
    client = DataFrameClient(
        host=creds["host"],
        port=creds["port"],
        username=creds["user"],
        password=creds["password"],
        database=creds["database"],
    )
    return client


def fetch_data_to_df2(
    client: DataFrameClient, query: str, measurement: str, *, tz_de: bool
) -> pd.DataFrame:
    """
    Fetch data from DB into to Pandas DataFrame via DataFrameClient.

    time is as index
    copied from my private Raspi repo
    """
    result = client.query(query)
    df: pd.DataFrame = result[measurement]  # type: ignore
    df.index.name = "datetime"
    if tz_de:
        assert type(df.index) is pd.DatetimeIndex
        df.index = df.index.tz_convert("Europe/Berlin").tz_localize(None)
    return df


if __name__ == "__main__":
    client = connect2_df(creds=creds)
    df = fetch_data_to_df2(
        client=client, query=QUERY, measurement=MEASUREMENT, tz_de=True
    )

    df.to_csv(FILE_OUT, sep="\t", lineterminator="\n")
