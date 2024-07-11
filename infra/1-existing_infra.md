# 1. 기존 Infra 아키텍처

<figure><img src="../.gitbook/assets/image (3).png" alt=""><figcaption></figcaption></figure>

* Internet gateway, NAT gateway 통한 VPC 보안
* Bastion host를 구축하고 private subnet 접속 제한
* ec2, rds 기반 airflow ui, scheduler, worker, meta db 구축
* AWS Codebuild 통한 자동 코드 배포
* ~~S3 기반 정적 웹 사이트 hosting~~ (몰라도 됨)
