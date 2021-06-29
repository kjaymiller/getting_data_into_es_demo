import csv
from connection import client
from elasticsearch import helpers

with open('cat_data.csv') as f:
    reader = csv.DictReader(f)
    helpers.bulk(client, reader, index='cat_data')
