# 5. Airflow 운영 환경 구축

# 1) 기존에 구축한 방법

{% embed url="https://www.notion.so/thewayaboutme/d9c22d81ad5b440ab11e1cce39db1929?pvs=4#7897c623bfe243b58bb9b9bc032ff85d" %}


# 2) Azure VM에 Airflow 환경 세팅하는 방법 (with docker compose)
### 세팅

- azure 인스턴스 만듦.
  - B2s
    - 리전: West US 2
    - vCPUs: 2
    - Memory: 4GB
    - Storage: 30GB SSD
    - 월 $30.368 (약 42174원)
    - 우분투 22.04
- 접속 커맨드
  - `ssh -i ~/.ssh/jaringobi_airflow.pem  jaringobi@<your-azure-vm-ip>`

## 실행 방법

1. Azure VM에 접속: SSH를 사용하여 Azure VM 인스턴스에 접속합니다.
2. Docker 및 Docker Compose 설치
    - 설치 후 로그아웃했다가 다시 로그인하여 권한 변경사항을 적용합니다.

    ```bash
    sudo apt update
    sudo apt install docker.io docker-compose -y
    sudo usermod -aG docker $USER
    ```

3. 프로젝트 디렉토리 생성

    ```bash
    mkdir airflow-docker
    cd airflow-docker
    ```

4. Docker Compose 파일 생성

    ```yaml
    vim docker-compose.yml
    ```

    ```yaml
    version: '3'
    
    x-airflow-common:
      &airflow-common
      image: apache/airflow:2.5.0
     user: "${AIRFLOW_UID:-50000}:0"
      environment:
        &airflow-common-env
        AIRFLOW__CORE__EXECUTOR: LocalExecutor
        AIRFLOW__CORE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
        AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
        AIRFLOW__CORE__FERNET_KEY: ''
        AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION: 'true'
        AIRFLOW__CORE__LOAD_EXAMPLES: 'true'
        AIRFLOW__API__AUTH_BACKENDS: 'airflow.api.auth.backend.basic_auth,airflow.api.auth.backend.session'
        AIRFLOW__WEBSERVER__BASE_URL: http://<your-azure-vm-ip>:8080
        AIRFLOW__WEBSERVER__WEB_SERVER_HOST: 0.0.0.0
      volumes:
        - ./dags:/opt/airflow/dags
        - ./logs:/opt/airflow/logs
        - ./plugins:/opt/airflow/plugins
      depends_on:
        &airflow-common-depends-on
        postgres:
          condition: service_healthy
    
    services:
      postgres:
        image: postgres:13
        environment:
          POSTGRES_USER: airflow
          POSTGRES_PASSWORD: airflow
          POSTGRES_DB: airflow
        volumes:
          - postgres-db-volume:/var/lib/postgresql/data
        healthcheck:
          test: ["CMD", "pg_isready", "-U", "airflow"]
          interval: 5s
          retries: 5
        restart: always
    
      airflow-webserver:
        <<: *airflow-common
        command: webserver
        ports:
          - 0.0.0.0:8080:8080
        healthcheck:
          test: ["CMD", "curl", "--fail", "http://localhost:8080/health"]
          interval: 10s
          timeout: 10s
          retries: 5
        restart: always
        depends_on:
          <<: *airflow-common-depends-on
    
      airflow-scheduler:
        <<: *airflow-common
        command: scheduler
        healthcheck:
          test: ["CMD-SHELL", 'airflow jobs check --job-type SchedulerJob --hostname "$${HOSTNAME}"']
          interval: 10s
          timeout: 10s
          retries: 5
        restart: always
        depends_on:
          <<: *airflow-common-depends-on
    
    networks:
      default:
        driver: bridge
        
    volumes:
      postgres-db-volume:
    ```

5. 필요한 디렉토리 생성

    ```yaml
    mkdir -p ./dags ./logs ./plugins
    ```

6. Docker Compose 실행

    ```yaml
    docker-compose up -d
    ```

7. Airflow 초기화
    - 권한 문제 해결

        ```bash
        sudo chown -R 50000:50000 ./logs
        sudo chmod -R 775 ./logs
        ```

    - 환경 변수 파일을 생성

        ```bash
        echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
        ```

    ```bash
    docker-compose run airflow-webserver airflow db init
    ```

8. Airflow 관리자 계정 생성

    ```bash
    docker-compose run airflow-webserver airflow users create \
       --username admin \
       --firstname Admin \
       --lastname User \
       --role Admin \
       --email admin@example.com \
       --password admin
    ```

9. Airflow 웹 인터페이스 접속
    - 브라우저에서 http://<your-azure-vm-ip>:8080 으로 접속합니다. username: admin, password: admin으로 로그인할 수 있습니다.
    - 접속 안된다면
        - `airflow-webserver` 잘 떠있나 확인하기

            ```bash
            docker-compose logs airflow-webserver
            ```

        - 포트 맵핑 확인
            - 8080:8080
        - 방화벽 설정 확인

            ```bash
            sudo ufw status
            
            # Status: inactive
            # 라고 나오면 아래 커맨드 실행
            sudo ufw allow 8080/tcp
            ```

        - **azure → 네트워크 설정에서 8080 포트 열어서 해결.**
            - 원본: Any 또는 Your IP
            - 원본 포트 범위: *
            - 대상: Any
            - 대상 포트 범위: 8080
            - 프로토콜: TCP
            - 작업: 허용
            - 우선 순위: (1000 이하의 숫자)

- 이슈 해결
  - airflow-scheduler log 보니까 해당 에러가 있어서 권한 수정함.

    ```bash
    PermissionError: [Errno 13] Permission denied: '/opt/airflow/logs/dag_processor_manager'
    ```

    ```bash
    ls -l ./logs
    sudo chown -R 50000:50000 ./logs # 기존에는 50000:root로 되어 있었음.
    sudo chmod -R 755 ./logs
    ```
