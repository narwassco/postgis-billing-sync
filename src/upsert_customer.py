import pandas as pd
import asyncpg
import datetime

async def upsert_customer(df, DSN):
    now = datetime.datetime.now()
    conn = await asyncpg.connect(dsn=DSN)
    try:
        async with conn.transaction():
            for i, row in df.iterrows():
                query = f"""
                    INSERT INTO public.customer (
                        zonecd, 
                        connno, 
                        name, 
                        villageid, 
                        status, 
                        serialno, 
                        category, 
                        service_type, 
                        disconnection_type,
                        insertdate
                    )
                    VALUES (
                        $1, -- zonecd
                        $2, -- connno
                        $3, -- name
                        $4, -- villageid
                        $5, -- status
                        $6, -- serialno
                        $7, -- category
                        $8, -- service_type
                        $9, -- disconnection_type
                        $10 -- insertdate
                    )
                    ON CONFLICT (zonecd, connno) DO UPDATE
                    SET name = $3,
                        villageid = $4,
                        status = $5,
                        serialno = $6,
                        category = $7,
                        service_type = $8,
                        disconnection_type = $9,
                        updatedate = $10
                    ;
                """
                values = (
                    row['zonecd'], 
                    row['connno'], 
                    row['name'],
                    row['villageid'],
                    row['status'],
                    None if pd.isna(row['serialno']) else str(row['serialno']),
                    row['category'],
                    row['service_type'],
                    None if pd.isna(row['disconnection_type']) else str(row['disconnection_type']),
                    now
                )
                await conn.execute(query, *values)
    finally:
        await conn.close()