# 3. 가성비 서비스 운영을 위한 가성비 인프라 사용 계획

모든 방법을 나열하고 비교 후 여러 대안 혹은 결론을 도출해보겠습니다.<br><br>

## 목표
참고 자료는 [트래픽 수준에 따른 아키텍처 설계](https://sundries-in-myidea.tistory.com/114)
- 목표 트래픽: 1000명대.
  - `1000명` = 로드밸런서 도입 기준. 그만큼 예산도 달라짐
- 운영 기간: (공모전 종료 이후 기준) 최소 6개월 (포폴에 운영 종료 안한 서비스로 수록 예정)
<br><br>

## 필요한 기술 목록
- VPC? 이게 안되면, 관련 보안 기능 포함된 타 서비스 사용
- 퍼블릭 도메인과 DNS
- 보안 (SSL, HTTPS 등)
- 로드 밸런서
- 서버: 크롤링 2개 OR 크롤링1개 & 에어플로??개, 백엔드 API, 검색, DB, (메시지 큐)
*Airflow를 가볍게 올리는 경우의 pros & cons, 그 방법?
<br><br>

## 운영 목적에 따른 계획
### ~9월 또는 10월: 공모전 종료 전
- 공모전 평가 기준 중 '최신 기술 사용 정도'가 있음
  - 이왕이면 테라폼 코드를 쓸 수 있는 플랫폼을 계속 사용
  - PaaS보단 SaaS, IaaS
 <br>
 
### 종료 후 트래픽 관찰 & 광고 부수입용 운영 시
- 애드센스 부착이 가능해야 함
- 컴퓨팅 사양 및 운영 시간/비용에 대한 가성비 중요
- 배우는 게 많은 기술 스택보단 가성비, 편의성 중심으로 선택
<br><br>

### Airflow 기술 스택 변경 OR 유지?
다음과 같은 이유로 유지를 결정했습니다.
- DB 구축 목적으로 사용하는 것 외에도, 쌓고 싶은 데이터가 많음
  - 데이터 소스(원천 데이터)가 많을수록 규모 있는 스케줄링 오픈소스의 효용이 클 것으로 예상
- 취준 스펙에 유리, 업무애도 많은 도움 되는..
  - 구축&운영 경험이 학습, 스펙 양쪽에 도움될 것
- 기존 코드 수정 작업을 최소화할 수 있음
<br><br>


## 기술 스택별 대안 목록
아래와 같은 관점으로 견적 비교
- 무료 계정 지원 기간(개월~년)
- 크레딧 금액 및 시간(hrs)
- CPU, 메모리, 디스크, 대역폭, 전송량 spec<br>

사람이 4명이란 점도 활용할 것..!
<br><br>

### 클라우드 플랫폼 혹은 그 산하 서비스
#### AWS
##### 1. [Lightsail](https://aws.amazon.com/ko/lightsail/pricing/)
- 예산 계획이 쉽고 직관적
  - 메모리, vCPU, Solid-State Drive(SSD) 스토리지와 같은 **리소스를 하나의 플랜으로 묶어 번들로 제공**
- 모든 Lightsail 플랜에 포함
  - **고정 IP 주소**
  - DNS 관리
  - 원클릭 SSH 터미널 액세스(Linux/Unix)
  - 강력한 API
  - **고가용성 SSD 스토리지**
  - **서버 모니터링**
- **3개월 내 750 시간**까지 무료
  - Linux/Unix 번들(퍼블릭 IPv4 주소 포함)에 대한 3개월 무료 혜택
    - 12 USD/월: 2GB 메모리, vCPU 2개***, 60GB, SSD 디스크, 3TB 전송*
    - 24 USD/월: 4GB 메모리, vCPU 2개, 80GB SSD 디스크, 4TB 전송*
    - 44 USD/월: 8GB 메모리, vCPU 2개, 160GB SSD 디스크, 5TB 전송*
    - asterica 표기된 주의사항도 꼭 숙지해야 함.
  - Linux/Unix 번들(IPv6 주소 포함)에 대한 3개월 무료 혜택: 3.50 USD/월, 5 USD/월 및 10 USD/월 등
- **15 USD/월** 데이터베이스 번들에 대한 3개월 무료 혜택
- 10 USD/월 컨테이너 서비스(마이크로 -1 노드)에 대한 3개월 무료 혜택
- 로드밸런서: **18$/월**
- [lightsail 견적 받기](https://aws.amazon.com/ko/contact-us/sales-support-pricing/)
<br>

##### 2. AWS [saving plans](https://velog.io/@xgro/AWS-Saving-Plans-%EC%A0%81%EC%9A%A9%ED%95%98%EA%B8%B0)
흔히 알고 있는 On-Demand 와 다른 방식의 요금제가 많다. 그 중 뭘 써도 온디맨드보단 싸다. [계산기](https://calculator.aws/#/createCalculator/ec2-enhancement?nc2=h_ql_pr_calc)로 가장 정확하게 계산 가능<br>
ex) **t4g.large (2vCPU, 8 GiB 메모리)**, 1년 **557$ → 344$ (1년 필수 결제)**
<br>

##### 3. ~~AWS lambda~~
서버리스 기술로, 
~~는 gateway랑 같이 써야 하는게 문젠데 이것도 유료여서.. 첨에 원래 람다였다가 바꾼 이유가 이것. API는 2개 뿐이지만 스키마 변경이 잦고 데엔 파트와 의존성이 있어 람다 안쓰기로..~~
<br>

##### 4. EC2 등 대표 서비스 프리티어
타 서비스와 비교 위해 기재해 둠
- EC2
  - t3.micro 인스턴스 (2코어 / 1GB RAM)
  - 월 750 시간 (한달 내내 사용 가능)
  - 아웃 바운드 트래픽 100GB
  - 1코어 성능 10%까지만 사용 가능.
    - [크레딧이 없으면 성능 발휘가 제대로 안된다.](https://helpit.tistory.com/23)
- EBS (Elastic Block Storage)
   - SSD 등 영구 블록 스토리지를 30GB까지 사용 가능
   - EC2 인스턴스 생성시 8GB의 EBS가 사용됨
   - 30GB 초과 시 인스턴스를 종료시켜도 비용 청구됨
- S3
   - 5GB 까지 무료
   - GET 요청 2만건, PUT 요청 2천건 까지
<br>

#### [Microsoft Azure 학생 계정](https://azure.microsoft.com/ko-kr/free/students#tabxabc182d79c494d2787c55ef0918b22d1) / [무료 credit](https://azure.microsoft.com/ko-kr/pricing/free-services/)
- 학생 지원 아닌 무료 크레딧은 1달/200$
- 12개월 경과 후 무료 크레딧이 다시 제공되는 서비스 일부 존재
-  Azure Virtual Machines - Linux / Windows
   - B1s 버스트 (1코어 1GB RAM)
   - Windows와 Linux 한 대씩 생성해서 750시간 씩 사용 가능
   - 아웃 바운드 트래픽 15GB
   - 1코어 성능 10%까지만 사용가능
- Azure Blob
  - 스토리지 서비스로, 5GB까지 무료
  - GET 2만건, PUT 1만건 까지
  - 64GB 고정하고 2개
- Azure Managed Disks
  - SSD 스토리지 서비스로 1GB 스냅샷, 200만개의 I/O 작업까지 무료
<br>

#### GCP
- 90일/300달러 크레딧
- Compute Engine
  - e2-micro (2코어 1GB RAM)
  - US의 리전 3개에서만 가능 (오리건 / 아이오와 / 사우스 캐롤라이나)
  - 1코어 성능 100% 시 30초만 사용 가능
  - 아웃 바운드 트래픽 1GB로 매우 적음
- 스토리지
  - Cloud Storage 5GB
  - Disk storage 30GB
<br>


#### Oracle Cloud (OCI)
- 1달 $300 크레딧. 평생 프리티어 사용 가능
- 프리티어 VM 스펙, 사용 시간 기준 가성비 1등
  - **고사양 서버를 저비용으로 쓰고 싶다면 가장 좋은 선택지**라 함
- 특이사항: **첫 가입 실패 시 평생 가입 불가**
- AMD 기반 VM / ARM 기반 VM
  - AMD (2코어 1GB RAM) / ARM (4코어 24GB RAM) 1달 간 3000시간 무료!!!
  - 업글 안하면 추가 비용 발생 안함
  - 1코어당 480mbps 대역폭
  - 아웃바운드 트래픽 10TB
  - 이런 고사양 VM이 2개까지 공짜 BUT 너무 혜자라 가용성이 거의 없음
    - 내가 만드려면 남이 삭제를 해야 한다
- 스토리지
  - 스토리지 100GB 2개 제공
  - VM마다 할당 가능
<br>

#### [Vultr](https://namu.wiki/w/Vultr)
- 가성비 좋은데 많이 안유명하대서 조사해 봄
  - 근데 [**4코어 / 8GB RAM / 6TB 대역폭 = $48/월**](https://www.vultr.com/pricing/).
- 타사에 비해 높은 업타임을 걸고 있다. 무려 100.0% 업타임을 SLA로 내걸고 있어 5분 이상 서버가 다운되면 그에 상응하는 크레딧을 지급해 준다.
<br>

#### cafe24, gabia
<br>

#### NCP
- Public IP 유료
- 3개월 10만원 크레딧
<br>

#### [DigitalOcean](https://www.digitalocean.com/pricing)
- 60일/$200 크레딧
- PostgreSQL
  - 최소 사양으로 해도 $15/달
- **8 GiB, 4 vCPUs, 5000 GiB 사양이 $84/달...**
- [나무위키](https://namu.wiki/w/DigitalOcean)
<br><br>


### 파편적 플랫폼/서비스
#### ~~Vercel~~
~~무료 호스팅 가능 (무료 트래픽 제공량 많은 편)지만 JS 기반 기술만 지원~~
<br>

#### 데베
어느 플랫폼이든 데베는 컴퓨팅 머신보다 훨씬 비쌈.
- mongodb.com → 무료 512MB 제공 가능
- [planetscale.com](https://planetscale.com/pricing?cluster_size=PS_10&storage_gb=&region=us-west) → 관계형 데이터베이스 무료 사용 가능.. 전혀 아니고 사양 젤낮은게 한 달 $39?;;
- ECS 같은 서버에 직접 구축
<br>

#### 백엔드 서버 플랫폼
- [Cloudtype](https://cloudtype.io/pricing)
  - 조코딩에 영상 올라와서 알게 됐는데, 가성비 원탑
  - **로드밸런서, https, DNS 등록, DB, CICD 등 한 번에 지원**
  - **검색엔진 수집(SEO) 불가**
    - 서비스로부터 발생하는 데이터 수집은 잘 안될 것 같음
  - **2 vCPU / 4GB RAM / 동시실행 12개, 최대 4인까지 계정 공유 가능 => 월 ₩49,500**
<br><br>



### 기타
#### 라즈베리파이 (크롤링 서버 만을 위한다던지)
학습, 가성비 다 매우 훌륭 but 시간 이슈 매우 큼
<br>

#### ~~깃헙 학생 혜택~~
~~헤로쿠, AWS 크레딧 있던거 다없어졌네~~
<br>

#### 디자인
ui.shadcn.com/themes → 컴포넌트 라이브러리 사용 가능
<br>

#### AWS ElasticSearch
AWS에서 제공하는 ElasticSearch 솔루션 서비스도 있음.
<br>

#### [위시켓](https://www.wishket.com/store/47/?utm_source=yozmit&utm_medium=banner&utm_campaign=aws&utm_content=cd3)
직접 요청해서 받아보기 전엔 요금 견적을 전혀 알 수 없음
<br><br>


## 결론
- 크롤링 비롯 Airflow
  - 구성 요소가 많은 만큼, 한 플랫폼 안에서 해결하는 게 좋을 듯
    - **저사양 인스턴스 여러 개 사용해도 괜찮다면, Azure 계정 만들고 돌려쓰기.?**
  - 설치해서 사용할랬더니 MetaDB로 사용하는 PostgreSQL 사양만 해도 많이..높..
- 백엔드 & 검색 엔진
  - 둘을 분리하여 운영 VS 모놀리식 중 뭘로 할지에 따라 다름
    - 둘중 어떻게 하는 게 더 저렴할지는 아직 안 따져봄
  - **가성비는 Cloudtype이 갑 but 기술적으로 배우는 게 있고 싶다면 컴퓨팅 머신 사용**
- 데이터베이스
  - 가장 가성비가 중요한 기술 스택
  - 프리티어로 **가장 고사양 사용 가능한 OCI**, 또는 **Airflow 구동 환경과 동일한 플랫폼**에서 VM 설치해서 사용 OR DB 솔루션 사용
- 여담으로, 의외로 AWS가 특별히 비싼 편이 아니었다 (같은 사양끼리 비교했을 때)
<br><br>


## 여담
### 컴퓨팅 자원 효율적 활용을 위한 엔지니어링 방안
#### Auto Scaling 구현
<br>

### `단일 계정 멀티 리전` OR `여러 계정 사용`
- Redshift는 리전마다 새 크레딧이 적용돼서, EC2 등도 그러려나.. 싶었
- 전자는 서로 다른 리전 간 전송 횟수, 전송량이 늘어 오히려 요금이 많이 나오고 프리티어 차감이 빨라진다 함
<br>



### 그 외 Reference
[각종 클라우드 플랫폼 요금과 크레딧](https://brunch.co.kr/@topasvga/1522)
[아직도 돈 내고 서버 이용 중? 무료 클라우드 서버 총정리 - 조코딩](https://youtu.be/c9ul5iuBjrg?si=6uXgDzSvXrF59P3Z)
[집에서 서버를 운영하는 게 가능한가요? - 커피 한잔 개발자님](https://jeho.page/essay/2024/04/29/home-server.html)
[클라우드 서비스 프리티어 별 비교 (AWS / Azure / GCP / Oracle)](https://2mukee.tistory.com/640)
[Google Cloud vs AWS vs Azure : 클라우드 서비스 비교](https://www.goldenplanet.co.kr/our_contents/blog?number=1025&pn=)
[GCP, AWS, AZURE, OCI 프리티어 사용기](https://ittraveler.tistory.com/entry/GCP-AWS-AZURE-OCI-%ED%94%84%EB%A6%AC%ED%8B%B0%EC%96%B4-%EC%82%AC%EC%9A%A9%EA%B8%B0-%EB%A6%AC%EB%B7%B0-%EA%B0%80%EC%9E%A5-%EC%A2%8B%EC%9D%80-%ED%94%84%EB%A6%AC%ED%8B%B0%EC%96%B4%EB%8A%94-%EC%96%B4%EB%94%94)
[크롤링 서버가 소모하는 자원을 직접 계산하는 게 인상 깊었던, 캐치딜 백엔드 개발 이야기 : 합리적인 서버 비용을 찾아서](https://kbs4674.tistory.com/125)
