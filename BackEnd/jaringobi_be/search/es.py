from decouple import config
from pathlib import Path
from urllib.parse import urljoin

import requests
from requests.auth import HTTPBasicAuth

BASE_DIR = Path(__file__).resolve().parent.parent

es_host = config('ES_HOST')
es_auth = HTTPBasicAuth(config('ES_ID'), config('ES_PW'))
headers = {'Content-Type': 'application/json'}


def search_fuzzy(menu, test=True, fuzziness="AUTO"):
    query = {
        "query": {
            "fuzzy": {
                "food": {
                    "value": menu,
                    "fuzziness": fuzziness
                }
            }
        }
    }


    host = urljoin(es_host, 'food_idx/_search')
    response = requests.post(host, json=query, auth=es_auth, headers=headers)  # Response type
    print("Raw response:", response.text)
    response.raise_for_status()
    response_json = response.json()  # dict type

    if not test:
        if 'hits' in response_json and 'hits' in response_json['hits']:
            # TODO: generator 로 리팩토링
            result = [hit['_source']['food'] for hit in response_json['hits']['hits']]
            print(result)
            return result
    return response

