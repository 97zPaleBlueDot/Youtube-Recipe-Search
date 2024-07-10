# 기존 데이터 파이프라인

<figure><img src="../.gitbook/assets/image (5).png" alt=""><figcaption><p>Data Pipeline</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (4).png" alt=""><figcaption><p>Software Architecture</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (6).png" alt=""><figcaption></figcaption></figure>

### 1) 유튜브 요리 영상 레시피

* Airflow 미사용
* 해당 메뉴 Youtube 검색 결과 상위 10개
* Youtube 영상 중 본문 또는 댓글에 레시피 정보 따로 기재돼 있는 영상 페이지만 크롤링, 스크래핑
* 영상 검색 결과는 Youtube API 키 발급받아 사용
* 맥락이 필요한 텍스트 전처리는 Gemini Pro API 사용

Problem: 텍스트 전처리 정확도 낮음, 레시피 중복 데이터 존재

추가할 기능:&#x20;

### 2) 재료의 최저가

* Airflow 사용, 24시간 주기로 최저가 상품 정보 갱신
* Coupang 상품 정보 검색, ‘쿠팡추천순' 필터 적용
* 검색 결과 Top 랭킹 상품에 기재된 단위 가격을 바탕으로 비교해 최저가 상품 추출. 이를 구현하는 2가지 방법:
  * ETL 시 상위 3\~10개 상품을 일단 저장. ELT 시 그 중 최저가인 것만 추출해 service 스키마에 저장
    * 장점: ETL 로직 다소 경량화, 상품 정보를 좀더 상세하게 따질 수 있음 (기준 밖 정보 필터링)
    * 단점: 저장 공간 및 데이터 갱신 비용 증가
  *   ETL 후 raw\_data 스키마에 저장할 때부터 최저가인 상품 정보 1개만 저장

