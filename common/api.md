---
layout:
  title:
    visible: true
  description:
    visible: false
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
---

# 🥬 API 명세
## 응답 형태

```json
{
  "code"   : int,    // required, 코드(하단 참조)
  "message": string, // optional, 상태에 대한 메시지
  "result" : object  // optional, 응답 객체
}
```

## 처리할 상태 코드

```json
BAD_REQUEST(400, "Bad Request"),
NOT_FOUND(404, "Not Found"),
UNEXPECTED(500, "This request cannot be processed.")
```


## Django REST API


### `GET` /api/search

<aside>
📝 사용자가 검색한 메뉴의 최저가 유튜브 레시피를 보여 준다.
</aside>

- Request
    - Start Line
        ```bash
        GET /api/search HTTP/1.1
        ```
    - Header
    - Body
        ```json
        ```
        
- Response
    - Status Line
        ```bash
        200 OK
        404 NOT FOUND          // 
        500 UNEXPECTED             // 
        ```
    - Header
    - Body
      ```json
      {
        "recipe": {
            "ingredients": [
                {
                    "cheapest_product": {
                            "product_title": string,
                            "unit_price": float,
                            "unit_value": float,
                            "unit_name": string,
                            "url": string,
                            "img_src": string
                        },
                    "name": string,
                    "quantity": float,
                    "unit": string,
                    "vague": string,
                },
            ],
            "portions": int,
        },
        "menu": string,
        "youtube_url": string,
        "min_total_price": float
      }
      ```


## ElasticSearch REST API
<aside>
- ElasticSearch와 직접 통신할 땐 `POST` `/food_idx/_search`
</aside>


### 유사 결과 여러 개 (불일치해도 유사한 단어로 반환), 일부 글자만 일치해도 반환
<aside>
음식명 검색) 닭갈비 검색 시 완전 일치하는 '닭갈비'를 첫번째로, 이하로는 간장닭갈비, 양념닭갈비, 춘천닭갈비, 치즈닭갈비...
비음식명 검색) 선풍기 검색 시, 깐풍기, 풍기크레마, 풍기피자...
</aside>

- Request
    - Start Line
        ```bash
        GET /api/search/fuzzy HTTP/1.1
        ```
    - Header
    - Body
        ```json
        {
            "query": {
                "fuzzy": {
                    "food": { 
                        "value": string,
                        "fuzziness": string
                    }
                }
            }
        }
        ```
        
- Response
    - Status Line
        ```bash
        200 OK
        404 NOT FOUND          // 
        500 UNEXPECTED             // 
        ```
    - Header
    - Body
  ```json
  {
    "took": int,
    "timed_out": bool,
    "_shards": {
        "total": int,
        "successful": int,
        "skipped": int,
        "failed": int
    },
    "hits": {
        "total": {
            "value": int,
            "relation": string
        },
        "max_score": float,
        "hits": [
            {
                "_index": string,
                "_id": string,
                "_score": float,
                "_source": {
                    "food": string
                }
            },
        ]
    }
  }
  ```


### 음식명이 아닌 것은 필터링, 완전 포함하는 단어만 취급
<aside>
음식명 검색) 소불고기 검색 시 완전 일치하는 '소불고기'를 첫번째로, 이하로는 뚝배기소불고기, 소불고기밥, 소불고기전골, ..
비음식명 검색) 다리미 검색 시, 아무것도 반환하지 않음
</aside>
- Request
    - Start Line
      ```bash
        GET /api/search/match HTTP/1.1
        OR
        GET /api/search/term HTTP/1.1
        ```
    - Header
    - Body
      ```json
        {
          "query": {
              "match(또는 term)": {
                  "food": text
              }
          }
        }
      ```
        
- Response
    - Status Line
        ```bash
        200 OK
        404 NOT FOUND          // 
        500 UNEXPECTED             // 
        ```
    - Header
    - Body
  ```json
  {
    "took": int,
    "timed_out": bool,
    "_shards": {
        "total": int,
        "successful": int,
        "skipped": int,
        "failed": int
    },
    "hits": {
        "total": {
            "value": int,
            "relation": string
        },
        "max_score": float,
        "hits": [
            {
                "_index": string,
                "_id": string,
                "_score": float,
                "_source": {
                    "food": string
                }
            },
        ]
    }
  }
  ```