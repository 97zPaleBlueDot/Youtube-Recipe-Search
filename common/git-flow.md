---
description:
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

# 📒 Git Flow

## Commit Convention
### Commit Message
- feat: 기능 추가 및 수정
- design: 레이아웃 추가 및 수정
- fix: 버그 수정
- test: 테스트 코드 추가 및 수정
- setting: 환경 설정
- docs: 문서 추가 및 수정
- refactor: 코드 리팩토링
- style: 주석, 프리티어 등 기능의 영향없이 코드의 모양새만 바뀌는 경우
- ci: CI 관련 변경
- perform 성능 변화를 목적으로 코드 추가 및 수정

### Commit Title
> 커밋 타입(커밋 범위): 커밋 메세지 제목 (#이슈번호)
```
- 좋은 예시) feat(FE) : 깃허브 로그인 버튼 컴포넌트 구현 (#13)
- 나쁜 예시) feat: 로그인 구현
```
- 커밋 타입 : 소문자 영단어로 작성
- 커밋 범위 : FE (클라이언트 관련 작업), BE (서버 관련 작업), DO (DevOps 관련 작업) 중 관련된 작업으로 작성
- 커밋 메세지 제목 : 명령형으로 작성, 마침표로 끝나지 않음
- 이슈번호 : 커밋과 관련된 이슈 번호 작성

### Commit Unit
- 커밋 메시지를 기준으로 작성
- 하나의 커밋에는 하나의 작업단위만 작업
- 한 커밋이 너무 많은 파일을 수정하는 것을 지양
<br><br>


## Branch Strategy & Naming Convention
> 프로젝트를 진행하면서 브랜치를 생성할 때, 다음의 원칙을 따르도록 한다.

### 🚩 Strategy

브랜치 전략으로 `Git-Flow`를 사용한다.
*Git-Flow를 따르는 개발 방법: https://velog.io/@diduya/git-%ED%9A%A8%EC%9C%A8%EC%A0%81%EC%9D%B8-%ED%98%91%EC%97%85%EC%9D%84-%EC%9C%84%ED%95%9C-Git-Flow-%EC%9D%B4%ED%95%B4%ED%95%98%EA%B8%B0-git-branch-repository

- main branch  
  : 배포 가능한 상태만을 관리한다.

- develop branch  
  : 기능 개발을 위한 브랜치들을 병합하기 위해 사용한다. <br>
  모든 기능이 추가되고 버그가 수정되어 배포 가능한 안정적인 상태라면 해당 develop 브랜치를 master 브랜치에 merge한다. <br>
  평소에는 이 브랜치를 기반으로 개발을 진행한다.

- feature branch  
  : 기능을 개발하는 브랜치로, 새로운 기능 개발 및 버그 수정이 필요할 때마다 develop 브랜치로부터 분기한다. <br>
  feature 브랜치에서의 작업은 기본적으로 공유할 필요가 없기 때문에 자신의 로컬 저장소에서 관리한다. <br>
  개발이 완료되면 develop 브랜치로 merge하여 팀원과 공유한다. <br>
  더 이상 필요하지 않은 feature 브랜치는 삭제한다.

- release branch  
  : 배포를 위한 브랜치로, 최종적인 버그 수정이나 문서 추가 등 배포와 관련된 작업을 수행한다. <br>
  배포 관련 작업 이외에는 release 브랜치에 새로운 기능을 추가로 merge하지 않는다.

- hotfix branch  
  : 배포한 버전에 긴급하게 수정을 해야 할 필요가 있을 경우, master 브랜치에서 분기한다. <br>
  문제가 되는 부분을 수정 후에 master 브랜치에 merge하고 배포한다. <br>
  hotfix 브랜치에서의 변경 사항은 develop 브랜치에도 merge한다.

중심이 되는 master와 develop 브랜치를 제외한 나머지 feature, release, hotfix 브랜치는 merge되면 삭제하도록 한다.

### 🌿 Naming Rule

master와 develop 브랜치는 본래 이름을 사용하도록 한다.

feature 브랜치는 `feature/기능요약` 형식을 사용하도록 한다.

release 브랜치는 `release-버전` 형식을 사용하도록 한다.

hotfix 브랜치는 `hotfix-버전` 형식을 사용하도록 한다.

### 🎈 Naming Example

```
// feature branch
feature/login
feature/room-save
feature/comment-delete

// release branch
release-1.0
release-1.4

// hotfix branch
hotfix-1.0.1
hotfix-1.4.3
```

---

> #### Reference
> - [Branch 생성 방식과 네이밍 규칙](https://velog.io/@kim-jaemin420/Git-branch-naming)