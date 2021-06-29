from elasticsearch import Elasticsearch
import os

client = Elasticsearch(
        hosts= ["Jays-Mac-mini-3.local"],
	http_auth=(
		os.environ.get('ES_USER'),
		os.environ.get('ES_PASSWORD')
		),
        )
