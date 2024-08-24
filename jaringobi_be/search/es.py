from decouple import config
from pathlib import Path
from urllib.parse import urljoin

import requests
from requests.auth import HTTPBasicAuth

BASE_DIR = Path(__file__).resolve().parent.parent
# ES URL
es_host = config('ES_HOST')
es_auth = HTTPBasicAuth(config('ES_ID'), config('ES_PW'))
#cert_file= config('ES_CERT_PATH')

def search_es(query):
    host = urljoin(es_host, 'food_idx/_search')
    response = requests.post(host, json=query, auth=es_auth) # 인증정보 활성화 필요
    
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code, response.text

def search_fuzzy(text, fuzziness="AUTO"):
    query = {
        "query": {
            "fuzzy": {
                "food": { 
                    "value": text,
                    "fuzziness": fuzziness
                }
            }
        }
    }
    return search_es(query)
    
def search_match(text):
    query = {
        "query": {
            "match": {
                "food": text
            }
        }
    }
    return search_es(query)

def search_term(text):
    query = {
        "query": {
            "term": {
                "food": text
            }
        }
    }
    return search_es(query)
