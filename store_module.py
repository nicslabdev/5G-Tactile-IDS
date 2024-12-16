import influxdb_client, os, time
import pandas as pd
import numpy as np

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

def save_to_influxdb(X: pd.DataFrame, Y):
    # Initializa client
    token = os.environ.get("INFLUXDB_TOKEN")
    token = "sdfbl9YowtCfERWHmjjjq-GXfFoFgZJpZoCe4eMfPmufSXMahDQ2Dvj-yKns6imYFWSvuzy9zmylGG1pyyc6ZQ=="
    org = "5gtactile"
    url = "http://localhost:8086"

    write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

    # Write data
    bucket = "5gTactileIDS"
    write_api = write_client.write_api(write_options=SYNCHRONOUS)
    for index, row in X.iterrows():
        point = Point("IDS")
        for col in X.columns:
            point.field(col, row[col])
        point.field("Prediccion", Y[index])

        write_api.write(bucket=bucket, org=org, record=point)
        time.sleep(0.5)

    # query_api = write_client.query_api()
    # query = """from(bucket: "5gTactileIDS")
    #     |> range(start: -20m)
    #     |> filter(fn: (r) => r._measurement == "measssurement1")"""
    # tables = query_api.query(query, org=org)

    # for table in tables:
    #     for record in table.records:
    #         print(record)