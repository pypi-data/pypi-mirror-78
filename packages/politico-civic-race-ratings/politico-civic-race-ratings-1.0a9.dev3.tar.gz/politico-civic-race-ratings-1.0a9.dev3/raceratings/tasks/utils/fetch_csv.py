# Imports from python.
import csv


# Imports from other dependencies.
import requests


def fetch_csv(csv_url):
    data_response = requests.get(csv_url)

    return list(csv.DictReader(data_response.text.splitlines()))
