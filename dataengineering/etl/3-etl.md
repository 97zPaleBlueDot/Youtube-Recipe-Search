# 3. ETL 속도 개선

## 1) 기존 상황

쿠팡 크롤링을 통한 수집 작업 시 분당 1회만 크롤링이 가능한 관계로, 빠른 시간에 다량의 데이터를 구축할 수 없음\
\
⇒ 동일한 DAG를 10개 만들고 돌려 버림 (아래 코드 참고)\
[https://github.com/The-Pirates-of-Jaryngobi/the-cheapest-youtube-recipe/tree/main/ETL\_pipelines/coupang/dags](https://github.com/The-Pirates-of-Jaryngobi/the-cheapest-youtube-recipe/tree/main/ETL\_pipelines/coupang/dags)\
\
⇒ 단일 DAG 안에서 동일 task 여러 개를 비동기•분산•병렬 처리 하는 게 더 빠르진 않을지?