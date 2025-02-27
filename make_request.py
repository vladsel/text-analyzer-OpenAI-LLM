import os

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEXT_DOCUMENT = os.path.join(BASE_DIR, os.environ["TEXT_DOCUMENT"])
GENERATED_SUMMARY = os.path.join(BASE_DIR, os.environ["GENERATED_SUMMARY"])
GENERATED_CONTENTS = os.path.join(BASE_DIR, os.environ["GENERATED_CONTENTS"])

TEXT_DOCUMENT_KEY = os.environ["TEXT_DOCUMENT_KEY"]
GENERATED_SUMMARY_KEY = os.environ["GENERATED_SUMMARY_KEY"]
GENERATED_CONTENTS_KEY = os.environ["GENERATED_CONTENTS_KEY"]

SUMMARY_API_URL = os.environ["SUMMARY_API_URL"]
CONTENTS_API_URL = os.environ["CONTENTS_API_URL"]


def summary():
    print(TEXT_DOCUMENT)
    url = SUMMARY_API_URL
    data = {
        TEXT_DOCUMENT_KEY: TEXT_DOCUMENT,
        GENERATED_SUMMARY_KEY: GENERATED_SUMMARY
    }
    response = requests.post(url, json=data)
    print(response.json())


def contents():
    url = CONTENTS_API_URL
    data = {
        TEXT_DOCUMENT_KEY: TEXT_DOCUMENT,
        GENERATED_CONTENTS_KEY: GENERATED_CONTENTS
    }
    response = requests.post(url, json=data)
    print(response.json())


if __name__ == "__main__":
    summary()
    contents()
