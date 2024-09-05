<a id="readme-top"></a>
<!-- PROJECT LOGO -->
<!-- <br /> -->
<!-- <div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a> -->
<h2 align="center">"자린고비"</h2>
  <p align="center">
    최저가 요리 유튜브 레시피 검색 서비스 (24.03~)
    <br />
    <a href="https://palebluedot.gitbook.io/palebluedot-1"><strong>Explore the development docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/97zPaleBlueDot/Client/blob/main/resource/demo_gif.gif">View Full Demo</a>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#자린고비의-주요-특징과-효험">자린고비의 주요 특징과 효험</a></li>
      </ul>
      <ul>
        <li><a href="#Main-Tech-Stack">Main Tech Stack</a></li>
      </ul>
    </li>
    <li><a href="#Feature-Description">Feature Description</a></li>
    <li>
      <a href="#System-Architecture">System Architecture</a>
      <ul>
        <li><a href="#레시피-및-최저가-상품-정보-데이터-파이프라인">레시피 및 최저가 상품 정보 데이터 파이프라인</a></li>
      </ul>
    </li>
    <li><a href="#Future-Roadmap">Future Roadmap</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project
![for_readme](https://github.com/user-attachments/assets/d3f965b7-9d96-448b-b722-75d9dc141275)<br><br>

### 자린고비의 주요 특징과 효험
- 텍스트 기반 요리 레시피가 아닌, `유튜브 영상 레시피 활용`을 위한 정보 가공
- 음식점/편의점 판매 `요리의 원가 정보 제공`을 통한 <u>소비자 중심 경제적 편익 증진</u>
- `온라인 전자상거래 구매 링크 연동`으로 재료를 찾거나 가격을 비교하는 데 드는 <u>시간 및 구매 비용 절약</u>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Main Tech Stack
* Frontend: ![Retool][Retool]![Javascript][Javascript]![JQuery][JQuery.com]
* Backend: ![Django][Django]![ElasticSearch][ElasticSearch]
* Data Pipeline: ![Airflow][Airflow]![Gemini][Gemini]
* RDB: ![postgresql][postgresql]

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- Feature Description -->
## Feature Description
- 🔍 요리 영상(유튜브) 레시피 검색
- 📉🤑 최신 소매가를 반영해, 최저 비용으로 요리 가능한 영상(유튜브) 레시피(재료, 단위, 양) 정보 제공
- 🛍️ 최저 비용 산출에 사용된 재료별 최저가 상품 정보 제공
- 🛒 재료별 최저가 상품 구매 링크 연동
- 🏪 24시간 단위로 최저가 상품, 최저가 레시피 정보 갱신
- 📊 사용자 검색 로그 적재
- 🆕 신메뉴 및 레시피 정보 지속적 업데이트

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- System Architecture -->
## System Architecture
![palebluedot_architect](https://github.com/user-attachments/assets/ccd392df-434e-4caf-9e3a-b72fc4ab853e)
- 쿠팡, 유튜브 크롤링 데이터 파이프라인(Airflow): Microsoft Azure VM
- API 서버, DB 서버: AWS Lightsail EC2 (2vCPU, 4GB RAM)
- 검색 엔진(ElasticSearch): Vultr VM (4vCPU, 8GB RAM)

_For more details, please refer to the [Documentation](https://palebluedot.gitbook.io/palebluedot-1/infra)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### 레시피 및 최저가 상품 정보 데이터 파이프라인
<div align="center">
<img width="90%" src="https://github.com/user-attachments/assets/54291971-5f8b-441c-a694-fce298c8fde0"/>
</div>

#### 1) 기본 음식명•재료명 데이터 수집
- 최초 유튜브 레시피 기반 확보
- 공공 API 호출 크롤링
- 11,575건 중 153건의 음식명 데이터 선별 후 저장, 활용
- 데이터 출처
  - 식품의약품안전처 ‘식품영양성분 데이터베이스’
  - 소스산업화센터 ‘소스 레시피 DB’
  - Lampcook ‘음식 다국어사전’
<br>

#### 2) 영상(유튜브) 레시피 정보 수집
(1) 유튜브 검색 공개 API인 Youtube Data API v3 호출 → “메뉴명 + 레시피” 검색 → 상위 10개 영상 링크 추출
(2) selenium 기반 웹 크롤링, 영상 하단 ‘더보기' 정보 스크래핑
(3) 프롬프트와 Gemini API 를 적용한 ‘더보기' 정보 전처리
검색했던 음식명과 일치하는 음식의 레시피가 맞는지 1차 검증
→ ’더보기'에 기재된 텍스트 내 레시피 정보 포함 여부 확인
→ 포함 시, 재료명+양+단위(+대체 재료명) 또는 재료명+모호한 값(+대체 재료명) 조합 목록으로 전처리된 데이터 반환 (*모호한 값: ‘조금', ‘적당량', ‘많이' 등)
→ 모호한 값은 양(float)+단위(string) 값으로 변환 (변환 정보 누락 시 최저가 레시피 후보로 포함하지 않음)


#### 3) 재료별 최저가 상품 정보 수집(갱신)
- Airflow 를 통해 24시간 주기로 값 갱신 배치 작업
- '2)' 에서 확보된 재료명을 쿠팡(coupang.com)에 검색해 최저가 상품 1개만 선별 저장 (사이트에 기재된 단위 가격을 비교, 수집)
- 쿠팡 검색 시, 정렬은 ‘쿠팡추천순', 그외 ‘로켓배송/로켓프레시’ 옵션 필수 설정


#### 4) 최저가 레시피 정보 업데이트
- Airflow 를 통해 24시간 주기로 값 갱신 배치 작업
- 재료별로 최저가 정보에서 추출한 단위 가격과 레시피에 사용된 양∙단위 정보를 곱하고, 총합한 값을 레시피 가격으로 정의
- 최대 10개의 레시피 총 가격을 비교해 최저가 레시피 선정
<!-- * npm
  ```sh
  npm install npm@latest -g
  ``` -->
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- Future Roadmap -->
## Future Roadmap
- [ ] 시스템, 유저 대시보드 추가
- [ ] 레시피 2개 이상 보여주기 (최저가순)
- [ ] Frontend 재개발
- [ ] 양•단위 변환 값 추가 → 서비스되는 메뉴•레시피 종류 늘리기

See the [open issues](https://github.com/github_username/repo_name/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ## Acknowledgments
* []()
<p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[Retool]: https://img.shields.io/badge/retool-3D3D3D?style=for-the-badge&logo=retool&logoColor=white
[Django]: https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=61DAFB
[ElasticSearch]: https://img.shields.io/badge/elasticsearch-005571?style=for-the-badge&logo=elasticsearch&logoColor=FF3E00
[Airflow]: https://img.shields.io/badge/apacheairflow-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=4FC08D
[Gemini]: https://img.shields.io/badge/googlegemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white
[Javascript]: https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=white
[postgresql]: https://img.shields.io/badge/postgresql-4169E1?style=for-the-badge&logo=postgresql&logoColor=white
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white