# postgis-billing-sync
This repository is to manage the script which synchronies GIS database and new billing system data.

## Install

```shell
pipenv install
```

```shell
cp .env.example .env
```

update `database_connection` variable for your database.

## Usage

To sync billing CSV to PostGIS, execute the following command. Make sure specifing CSV file path as well.

```shell
pipenv run sync data/CUSTOMER\ ACCOUNTS\ CSV_16_18_14.csv
```

## Download uncaptured customer data

You can download the customer data which the coordinates are not captured yet by using the following SQL.

```sql
SELECT
    a.zonecd, 
    a.connno, 
    a.name, 
    a.villageid, 
    a.insertdate, 
    a.updatedate, 
    a.status, 
    a.serialno, 
    a.category, 
    a.service_type, 
    a.disconnection_type
FROM public.customer a
where not exists (select * from meter where zonecd = a.zonecd and connno = a.connno)
and zonecd in ('A', 'B', 'C', 'D')
```

If you only want to download cusotmers in Narok town, change `and zonecd in ('A', 'B', 'C', 'D')` to `and zonecd in ('A', 'B')`.

If you only want to download them in Ololulunga, change it to `and zonecd in ('C')`

## update customer table

- insert new columns to customer

```sql
ALTER TABLE IF EXISTS public.customer
    ADD COLUMN category character varying;

ALTER TABLE IF EXISTS public.customer
    ADD COLUMN service_type character varying;

ALTER TABLE IF EXISTS public.customer
    ADD COLUMN disconnection_type character varying;
```

delete sno column from customer

```sql
ALTER TABLE IF EXISTS public.customer DROP COLUMN IF EXISTS sno;
```

change data type for status column

```sql
ALTER TABLE public.customer
    ALTER COLUMN status TYPE character varying;
```

## update village table

There are several differences on village data between current database and billing system.

The village table need to be updated by the following SQLs.

```sql
update public.village set name = 'Olesankale' where name = 'Olesankare';
update public.village set name = 'London' where name = 'LONDON';
update public.village set name = 'Olopito' where name = 'OLOPITO';
update public.village set name = 'CBD Central' where name = 'CBD-Central';
update public.village set name = 'CBD Pussy' where name = 'CBD-Pussy';
update public.village set name = 'CBD Osupuko' where name = 'CBD-Osupuko';
update public.village set name = 'TM Area' where name = 'TM AREA';

INSERT INTO public.village (villageid, name, insertdate, geom, area, zone)
SELECT 38 as villageid, 'CBD CENTRAL II' as name, now() as insertdate, geom, area, zone from public.village where name = 'CBD Central'

INSERT INTO public.village (villageid, name, insertdate, geom, area, zone)
SELECT 39 as villageid, 'Lower London' as name, now() as insertdate, geom, area, zone from public.village where name = 'London'

INSERT INTO public.village (villageid, name, insertdate, geom, area, zone)
SELECT 40 as villageid, 'Olepolos' as name, now() as insertdate, geom, area, zone from public.village where name = 'Ololulunga Town'
```
