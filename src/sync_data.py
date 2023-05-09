import pandas as pd
import asyncio
import numpy as np
from .read_village_table import read_village_table
from .upsert_customer import upsert_customer

def sync_data(args):
    csv_file = args.csv_file

    # load CSV file
    df = pd.read_csv(csv_file, header=1)

    print(f"{len(df)} records were loaded from CSV: {csv_file}")

    # rename first column to 'customerid'
    df.columns.values[0] = 'customerid'

    # separate account number into connection number and zone cd
    df[['connno', 'zonecd']] = df['CONNECTION NO.'].str.extract(r'(\d+)([A-Z])')
    df['connno'] = df['connno'].astype(int)

    # extract minimum columns
    df = df.loc[df['zonecd'] != 'E', ['customerid', 'zonecd', 'connno', 'NAME', 'ACC STATUS', 'MTR#','ROUTE' , 'CATEGORY', 'SERVICE TYPE', 'DISCO TYPE']]
    print(f"{len(df)} records were loaded except Zone = E")

    df = df.rename(columns={'NAME': 'name'})
    df = df.rename(columns={'ACC STATUS': 'status'})
    df = df.rename(columns={'MTR#': 'serialno'})
    df = df.rename(columns={'ROUTE': 'village_name'})
    df = df.rename(columns={'CATEGORY': 'category'})
    df = df.rename(columns={'SERVICE TYPE': 'service_type'})
    df = df.rename(columns={'DISCO TYPE': 'disconnection_type'})

    # load environmental variables
    from dotenv import load_dotenv
    import os
    load_dotenv()

    # database conneciton string
    DSN = os.getenv("database_connection")
    print(f"connection_string of '{DSN}' is loaded from .env")

    # read village table
    df_village = asyncio.run(read_village_table(DSN))

    # join both dataframes by village_name to add villageid into df
    df = pd.merge(df, df_village, on='village_name', how='left')
    df['villageid'] = df['villageid'].fillna(np.nan).astype('Int64')

    df = df.loc[:, ['zonecd', 'connno', 'name', 'villageid', 'status','serialno' , 'category', 'service_type', 'disconnection_type']]

    # view data
    print(df)

    asyncio.run(upsert_customer(df, DSN))

    print(f"{len(df)} customers were updated successfully on PostGIS!")