#!/bin/bash

# TAR 파일을 배포 디렉토리로 이동
cd /opt/bitnami/BackEnd

# 가상환경 활성화
source .venv/bin/activate

# Django 프로젝트 디렉토리로 이동
cd /opt/bitnami/BackEnd/jaringobi_be

# 로그 폴더 경로 설정
LOG_DIR="server_onoff_logs"
LOG_FILE="$LOG_DIR/$(date '+%Y-%m-%d_%H-%M-%S').log"

# 로그 폴더가 존재하지 않으면 생성
mkdir -p $LOG_DIR

# 로그 파일에 로그 기록 시작
{
    echo "==== Django Server Restart ===="
    echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"

    # 활성화된 Python 경로 확인
    echo "Using Python interpreter at: $(which python)"

    # 서버가 실행 중인 프로세스 확인
    echo "Checking for running Django server..."
    PID=$(ps aux | grep 'manage.py runserver' | grep -v grep | awk '{print $2}')

    if [ -z "$PID" ]; then
      echo "No running Django server found."
    else
      echo "Found running Django server with PID: $PID"
      echo "Stopping Django server..."
      kill -9 $PID
      echo "Django server stopped."
    fi

    # Django 서버 다시 시작
    echo "Starting Django server..."
    nohup $(which python) manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &
    echo "Django server started."

    echo "===================================="
} >> $LOG_FILE 2>&1

echo "Logs saved to $LOG_FILE"
