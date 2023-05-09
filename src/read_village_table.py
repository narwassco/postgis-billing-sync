import pandas as pd
import asyncpg

# read village table
async def read_village_table(DSN):
    conn = await asyncpg.connect(dsn=DSN)
    query = "SELECT villageid, name as village_name FROM village;"
    results = await conn.fetch(query)
    await conn.close()
    rows = [row for row in results]
    df = pd.DataFrame.from_records(rows, columns=results[0].keys())
    return df