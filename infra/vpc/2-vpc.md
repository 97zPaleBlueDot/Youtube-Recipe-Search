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

# 2. 기본 VPC 구축

## 1) 이전에 구축한 방법
이전엔 AWS 사이트에서 콘솔을 통해 손수 구축했습니다. 그러나, 옵션을 변경해야 하는데 이를 지원하지 않아 기존 것을 삭제하고 처음부터 새로 구축해야 하는 일이 잦다는 문제가 있었습니다. 이러한 이유로, Terraform과 Ansible을 사용해 IaC를 기반으로 한 인프라 구축을 시도해 편의성을 비롯한 여러 장단점을 비교하는 경험을 해보았습니다.

## 2)
이하로는 이번에 구축한 방식, 경과를 적어주세요.