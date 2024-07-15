/*psql 접속 후 절차
1. 데이터베이스 생성 및 접속 전환*/
CREATE DATABASE raw_data;
CREATE DATABASE service;
/*  psql 명령 정리
접속한 데이터베이스 전환: \c raw_data
접속한 데이터베이스 내 모든 테이블 목록 조회: \dt
*/

/* 2. Create Table
1) raw_data: 원천 -> 유튜브/쿠팡 크롤링 ETL
따로 얻어낸 원천 메뉴명 데이터도 있고, 새롭게 생성될 메뉴도 포함된다(메시지 큐 기반 심화 기능)!*/
CREATE TABLE IF NOT EXISTS menu (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    category VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP);

/* 쿠팡 상품 초기 크롤링 상태.
rank, rating_total_count, discount_rate 컬럼 없앰. */
CREATE TABLE IF NOT EXISTS product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(1024) NOT NULL,
    unit_price FLOAT,
    unit VARCHAR(32),
    url VARCHAR(2048),
    img_src VARCHAR(2048),
    badge_rocket VARCHAR(64),
    storage_method VARCHAR(128),
    expiration_date DATE,
    is_bulk BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP);

CREATE TABLE IF NOT EXISTS youtube_vdo (
    id SERIAL PRIMARY KEY,
    youtube_url VARCHAR(1024) NOT NULL,
    menu_id INTEGER NOT NULL,
    full_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,
    FOREIGN KEY (menu_id) REFERENCES menu (id));



-- 2) raw_data: ETL -> ELT
CREATE TABLE IF NOT EXISTS recipe (
    id SERIAL PRIMARY KEY,
    youtube_vdo_id INTEGER NOT NULL,
    menu_id INTEGER NOT NULL,
    FOREIGN KEY (menu_id) REFERENCES menu (id),
    FOREIGN KEY (youtube_vdo_id) REFERENCES youtube_vdo (id));

CREATE TABLE IF NOT EXISTS ingredient (
    id SERIAL PRIMARY KEY,
    product_id INTEGER,  -- 늦게 채워져도 됨, 쿠팡 검색에 없을 수 있어 키 제약 안검
    name VARCHAR(128) NOT NULL,
    volume FLOAT,
    unit VARCHAR(64),
    vague VARCHAR(128));

CREATE TABLE IF NOT EXISTS recipe_ingredient (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipe (id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredient (id));

CREATE TABLE IF NOT EXISTS unit_conversion (
    conversion_id SERIAL PRIMARY KEY,
    ingredient_name VARCHAR(128),
    unit_name VARCHAR(64),
    converted_vol FLOAT);


-- 3) service: ELT -> service
CREATE TABLE IF NOT EXISTS cheap_recipe (  -- recipe, youtube_vdo 값을 조인해서 만들어짐
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER NOT NULL,
    menu VARCHAR(64) NOT NULL,
    youtube_url VARCHAR(1024) NOT NULL,
    min_total_price FLOAT,  -- 핵심!!
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS cheapest_product (  -- product, ingredient를 조인해 만들어짐
    id SERIAL PRIMARY KEY,
    ingredient_id INTEGER NOT NULL,
    ingredient VARCHAR(128) NOT NULL,  -- equals to product name
    product_url VARCHAR(2048),
    unit_price FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);