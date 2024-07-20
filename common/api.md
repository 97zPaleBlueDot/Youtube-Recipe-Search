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

### `GET` /home

<aside>
📝 메인 페이지를 불러온다.
</aside>

- Request
    - Start Line
        
        ```bash
        GET /home HTTP/1.1
        ```
        
    - Header
        
- Response
    - Status Line
        
        ```bash
        200 OK
        ```
        
    - Header
    - Body

### `POST` /search

<aside>
📝 사용자가 검색한 메뉴의 최저가 유튜브 레시피를 보여 준다.
</aside>

- Request
    - Start Line
        ```bash
        POST /search HTTP/1.1
        ```
    - Header
    - Body
        ```json
        "menu_name" : string      // required, string, DB에 없는 값!
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
          "youtube_url" : string, // required, 유튜브 영상 링크
          "total_price" : float, // required, 최종 가격
        	"ingredients" : [
                      {
                        "name" : string, // required, 재료명
                        "unit_price" : float, // 단위 가격
                        "price" : float, // 상품 가격
                        "quantity" : float, // 용량
                        "unit" : string, // 재료 단위
                        "product_url" : string // 상품 url
                        "img_url" : string // 상품 이미지
                      },
                      ...
        	], // 재료
        	"ingredients_without_unit" : [
        	  {
                    "name" : string,
                    "vague" : string
                  },
        	] // 변환된 양+단위 정보가 없는 재료
        }
        ```