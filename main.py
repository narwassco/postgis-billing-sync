import argparse
from src.sync_data import sync_data

parser = argparse.ArgumentParser(description='Syncronise billing CSV data with customer table on PostGIS.')
subparsers = parser.add_subparsers()

sync_parser = subparsers.add_parser('sync', help='Syncronise billing data with customer table.')
sync_parser.add_argument('csv_file', type=str, help='File path for CSV file from billing system.')
sync_parser.set_defaults(func=sync_data)

args = parser.parse_args()

args.func(args)
