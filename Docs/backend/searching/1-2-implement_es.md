# 요건
1. 오탈자 포함 검색(ex:김ㅁ치전) 처리 기능 구현
- 파이썬으로 데이터 불리기
2. 비-음식명(ex: 선풍기) 필터링 기능 구현
- 선풍기 => 깐풍기는 안 되는가
- 필터링을 한다면 웹에서 안내 기능 추가?

비음식명(ex.선풍기) 100% 매치 (오타어,동의어,정확한 음식명) 보다 정확도가 제일 높은 거 하나 뽑기가 ES 쿼리 짜기는 더 쉬움

자동완성은 난이도가 상승

3. 유사 음식명 검색 기능 구현 (ex: 파인애플새우볶음밥'을 검색했지만 음식명 DB에 없는 경우, '새우볶음밥'이 결과로 나오도록 구현
- fuzzy

# ES ON EC2
## 엘라스틱서치 설치
```
sudo apt update
sudo apt install apt-transport-https ca-certificates wget
```
pat 업데이트 후 인증 관련 패키지와 wget 인스톨

```
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
```
GPG키 가져오기

```
sudo sh -c 'echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" > /etc/apt/sources.list.d/elastic-7.x.list'
```
es 리포지토리를 apt에 추가

```
sudo apt update
sudo apt install elasticsearch
```
apt 업데이트하여 레포 반영후 es 인스톨

## 외부접속 허용
```
sudo sed -i '/^cluster\.initial_master_nodes/!s/$/\ncluster.initial_master_nodes: ["node-1", "node-2"]/' /etc/elasticsearch/elasticsearch.yml

sudo sed -i '/^http\.port/!s/$/\nhttp.port: 9200/' /etc/elasticsearch/elasticsearch.yml

sudo sed -i '/^network\.host/!s/$/\nnetwork.host: 0.0.0.0/' /etc/elasticsearch/elasticsearch.yml

sudo sed -i '/^xpack\.security\.enabled/!s/$/\nxpack.security.enabled: false/' /etc/elasticsearch/elasticsearch.yml
```
## 노리 플러그인 설치
```
sudo /usr/share/elasticsearch/bin/elasticsearch-plugin install analysis-nori
```

## 시동 명령어
```
1. sudo systemctl enable --now elasticsearch.service
2. sudo -i service elasticsearch start
```
재부팅시 자동으로 es 시작하려면 1, 그냥 시작하려면 2




# References
https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html

https://skysoo1111.tistory.com/68

https://velog.io/@jhchoi94/%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0-%EA%B5%AC%EC%84%B1-%EB%8B%A8%EC%9D%BC-%EA%B5%AC%EC%84%B1 인증 관련도 있음


인증관련
https://linux.systemv.pe.kr/2022/03/elasticsearch-%EB%B3%B4%EC%95%88-%EC%9D%B8%EC%A6%9D%EC%84%9C/

유저 및 롤 관련
https://blog.naver.com/rlaalsdn456456/222361332093 

mecab nori
https://velog.io/@nocode/Elasticsearch-8.x%EC%97%90%EC%84%9C-Nori-%EC%82%AC%EC%9A%A9%EC%9E%90-%EC%82%AC%EC%A0%84%EC%9D%84-%EC%82%AC%EC%9A%A9%ED%95%98%EB%8A%94-%EB%B0%A9%EB%B2%95

벌크 + nori
https://seolhee2750.tistory.com/m/269

단어사용통계
https://smin1620.tistory.com/284?category=1021642

NOT DOCKER
https://jjeongil.tistory.com/2007