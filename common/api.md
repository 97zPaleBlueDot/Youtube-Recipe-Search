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

### `GET` /api/home

<aside>
📝 메인 페이지를 불러온다.
</aside>

- Request
    - Start Line
        
        ```bash
        GET /api/home HTTP/1.1
        ```
        
    - Header
        
- Response
    - Status Line
        
        ```bash
        200 OK
        ```
        
    - Header
    - Body

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