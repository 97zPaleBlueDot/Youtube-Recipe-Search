import csv
import logging
import os
import re
import time
from datetime import datetime, timedelta
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

# 메모리 사용량 체크 코드
# from memory_profiler import profile

# 상품명을 기반으로 쿠팡에서 상품 검색 요청을 보내는 함수
def ingredientNameRequests(ingredient_name):
    logger = logging.getLogger("ingredientNameRequests")

    encoded_string = quote(ingredient_name, encoding="utf-8")
    logger.info(f"Ingredient Name: {ingredient_name}, Encoded String: {encoded_string}")

    url = (
        f"https://www.coupang.com/np/search?component=&q={encoded_string}&channel=user"
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
    }

    retries = 1
    delay = 1

    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response
        except requests.exceptions.RequestException as e:
            logger.error(
                f"Error occurred while making a request of ingredient_name: {e}"
            )

        if attempt < retries - 1:
            logger.info(f"Retrying in {delay} seconds...")
            time.sleep(delay)

    logger.error("Max retries reached. Could not retrieve data.")
    return None


# 쿠팡에서 받은 응답을 파싱하여 상품 세부 정보를 추출하는 함수
# @profile
def ingredientsDetailResult(response, ingredient_name):
    ingredient_result = []

    logger = logging.getLogger("ingredientsDetailResult")
    try:
        bsObj = BeautifulSoup(response.content, "html.parser")
        ul = bsObj.find("ul", id="productList")
        lis = ul.find_all("li")
    except Exception:
        logger.error(f"Failed to search ingredient_name on coupang: {ingredient_name}")
        return ingredient_result

    rank_number = 10
    rank_number_list = [i for i in range(1, rank_number + 1)]
    rank_class_name = None

    for li in lis:
        ingredient_detail = []

        if rank_class_name is None and len(rank_number_list) != 0:
            rank = rank_number_list.pop(0)
            rank_class_name = "number no-" + str(rank)

        if li.find("span", class_=rank_class_name) is not None:
            ingredient_detail.append(ingredient_name)

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ingredient_detail.append(current_time)

            product_title = (
                li.find("div", class_="name").text
                if li.find("div", class_="name")
                else None
            )
            ingredient_detail.append(product_title)

            price = (
                int(li.find("strong", class_="price-value").text.replace(",", ""))
                if li.find("strong", class_="price-value")
                else None
            )
            ingredient_detail.append(price)

            unit_price_string = (
                li.find("span", class_="unit-price")
                .text.replace(" ", "")
                .replace(",", "")[1:-1]
                if li.find("span", class_="unit-price")
                else None
            )
            if unit_price_string is not None:
                numbers = re.findall(r"\d+", unit_price_string)
                unit_and_unit_price = [int(num) for num in numbers]
                unit = unit_and_unit_price[0]
                unit_price = unit_and_unit_price[1]
                measure = re.findall(r"\d+(.*?)당", unit_price_string)[0]
                ingredient_detail.append(unit)
                ingredient_detail.append(measure)
                ingredient_detail.append(unit_price)
            else:
                ingredient_detail.append(None)
                ingredient_detail.append(None)
                ingredient_detail.append(999999999)

            badage_rocket = (
                "로켓배송" if li.find("span", class_="badge rocket") else None
            )
            ingredient_detail.append(badage_rocket)

            url = (
                "https://www.coupang.com" + li.find("a", href=True)["href"]
                if li.find("a", href=True)
                else None
            )
            ingredient_detail.append(url)

            if (
                li.find("img", class_="search-product-wrap-img").get("data-img-src")
                is not None
            ):
                image = "https:" + li.find("img", class_="search-product-wrap-img").get(
                    "data-img-src"
                )
            elif (
                li.find("img", class_="search-product-wrap-img").get("src") is not None
            ):
                image = "https:" + li.find("img", class_="search-product-wrap-img").get(
                    "src"
                )
            else:
                image = None
            ingredient_detail.append(image)
            
            # 최저가 계산을 위한 로직
            
            
            ingredient_result.append(ingredient_detail)
            rank_class_name = None

            logger.info(f"Ingredient Detail: {ingredient_detail}")

            if len(rank_number_list) == 0:
                return ingredient_result
    return ingredient_result

# 상품명 가져오기 

# DB에서 상품명을 가져오는 함수 => 실제 동작
# def import_ingredient_name_table():
#     conn = psycopg2.connect(
#         dbname=Variable.get("dbname"),
#         user=Variable.get("user"),
#         password=Variable.get("password"),
#         host=Variable.get("host"),
#         port="5432",
#     )

#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM ingredient")
#     table = cursor.fetchall()
#     conn.close()

#     youtube_dataset = [list(row) for row in table]
#     ingredient_name_list = []

#     for row in youtube_dataset:
#         ingredient_name_list.append(row[2])

#     ingredient_name_list = list(set(ingredient_name_list))
#     ingredient_name_list.sort()
#     ingredient_name_list = ingredient_name_list[
#         1 : (len(ingredient_name_list) // 10) * 1
#     ]

#     return ingredient_name_list


# CSV 파일에서 상품명을 가져오는 함수 => 테스트용
def import_ingredient_name_table():
    dag_folder = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(
        dag_folder, "youtube_preprocessed_dataset_2024-02-23-15-56.csv"
    )
    ingredient_name_list = []
    with open(file_path, "r", encoding="utf-8") as file:
        youtube_dataset = [line.strip().split(",") for line in file.readlines()]
        ingredient_name_list = []
        for data in youtube_dataset:
            if len(data) != 0:
                ingredient_name_list.append(data[0])

        ingredient_name_list = list(set(ingredient_name_list))
        ingredient_name_list.sort()

    # print(ingredient_name_list)

    return ingredient_name_list


# 상품명을 기반으로 상품 정보를 추출 및 변환하는 함수
# @profile
def extract_and_transform(ingredient_name_list):
    ingredient_result_fin = [
        [
            "ingredient_name",
            "time_stamp",
            "product_title",
            "price",
            "unit",
            "measure",
            "unit_price",
            "badage_rocket",
            "url",
            "image",
        ]
    ]
    while len(ingredient_name_list) != 0:
        ingredient_name = ingredient_name_list.pop(0)
        ingredient_response = ingredientNameRequests(ingredient_name)
        
        ingredient_result = ingredientsDetailResult(
            ingredient_response, ingredient_name
        )
        # print(f'ingredient: {ingredient_name}')
        # print(ingredient_result) -> 단위가격
        ingredient_result.sort(key=lambda x:x[6])
        if ingredient_result:
            cheapest_ingredient = ingredient_result[0]
            ingredient_result_fin.append(cheapest_ingredient)
    return ingredient_result_fin


# 추출 및 변환된 상품 정보를 CSV 파일에 쓰는 함수
def write_to_csv(ingredient_result):
    current_time = datetime.now()
    file_name = f'ingredient_result_1_{current_time.strftime("%Y-%m-%d_%H-%M-%S")}.csv'
    with open(file_name, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(ingredient_result)
    return file_name

if __name__ == "__main__":
    ingredient_name_list = import_ingredient_name_table()
    
    ingredient_result = extract_and_transform(ingredient_name_list)
    write_to_csv(ingredient_result)
    print('fin')