#!/bin/bash

# TAR 파일을 배포 디렉토리로 이동
cd /home/ec2-user/myapp

# TAR 파일 압축 풀기
tar -xzf $GITHUB_SHA.tgz
