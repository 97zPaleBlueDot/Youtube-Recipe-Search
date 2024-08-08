from __future__ import annotations

import os
import re
import time
from datetime import datetime, timedelta

import google.generativeai as genai
import pandas as pd
from dotenv import load_dotenv
from google.api_core import exceptions

from . import RECIPE_PROMPT, SYSTEM_PROMPT
from .utils import parse_json


class YoutubePreprocessor:
    def __init__(self):
        self.GEMINI_API_KEY = None
        self.gemini = None
        unit_conversion_df = pd.read_csv(
            "../../data/constant/unit_conversion.csv", encoding="utf-8"
        )
        quantity_conversion_df = pd.read_csv(
            "../../data/constant/quantity_conversion.csv", encoding="utf-8"
        )

        self.unit_conversion_dict = unit_conversion_df.set_index("unit_name")[
            ["converted_vol", "standard_unit"]
        ].to_dict(orient="index")
        self.quantity_conversion_dict = quantity_conversion_df.set_index(
            ["ingredient_name", "unit_name"]
        )["converted_gram"].to_dict()

    def convert_unit(self, row):
        vague_unit = row["vague"]
        if vague_unit in self.unit_conversion_dict:
            converted_vol = self.unit_conversion_dict[vague_unit]["converted_vol"]
            standard_unit = self.unit_conversion_dict[vague_unit]["standard_unit"]
            return pd.Series([float(converted_vol), standard_unit, ""])
        else:
            return pd.Series([row["quantity"], row["unit"], row["vague"]])

    def convert_quantity(self, row):
        ingredient_name = row["ingredient"]
        unit_name = row["unit"] if row["unit"] else row["vague"]

        if (ingredient_name, unit_name) in self.quantity_conversion_dict:
            converted_gram = self.quantity_conversion_dict[(ingredient_name, unit_name)]
            return pd.Series([converted_gram, "g", ""])
        else:
            return pd.Series([row["quantity"], row["unit"], row["vague"]])

    def set_gemini_api(self, n):
        load_dotenv("../../../resources/secret.env")
        self.GEMINI_API_KEY = os.environ.get(f"GEMINI_API_KEY{n}", None)
        if self.GEMINI_API_KEY is None:
            raise ValueError("GEMINI_API_KEY is not set.")
        genai.configure(api_key=self.GEMINI_API_KEY)
        self.gemini = genai.GenerativeModel("gemini-pro")

    def preprocess(self, text) -> str:
        return str(text).strip()

    def convert_to_number(self, text) -> int:
        if text is not None:
            try:
                number_string = ""
                for char in text:
                    if char.isdigit() or char == ".":
                        number_string += char
                number = float(number_string)
                if text[-1] == "천":
                    number *= 1000
                if text[-1] == "만":
                    number *= 10000
                if text[-1] == "K":
                    number *= 1000
                if text[-1] == "M":
                    number *= 10000
                return int(number)

            except Exception as e:
                print(e)
                print("text:", text)
                return 0
        else:
            return 0

    def convert_to_date(self, text):
        try:
            # '년 전', '개월 전', ... 형식 처리
            if "년" in text:
                num = int("".join(filter(str.isdigit, text)))
                delta = timedelta(days=num * 365)
                result = datetime.now() - delta
                return result.strftime("%Y-%m-%d")
            if "개월" in text:
                num = int("".join(filter(str.isdigit, text)))
                delta = timedelta(days=num * 30)
                result = datetime.now() - delta
                return result.strftime("%Y-%m-%d")
            if "주" in text:
                num = int("".join(filter(str.isdigit, text)))
                delta = timedelta(days=num * 7)
                result = datetime.now() - delta
                return result.strftime("%Y-%m-%d")
            if "일" in text:
                num = int("".join(filter(str.isdigit, text)))
                delta = timedelta(days=num * 1)
                result = datetime.now() - delta
                return result.strftime("%Y-%m-%d")
            if "시간" in text:
                result = datetime.now()
                return result.strftime("%Y-%m-%d")
            if "분" in text:
                result = datetime.now()
                return result.strftime("%Y-%m-%d")
        except Exception as e:
            print(e)
            print(text)

        # '년. 월. 일.' 형식 처리
        try:
            result = datetime.strptime(text, "%Y. %m. %d.")
            return result.strftime("%Y-%m-%d")
        except ValueError:
            print("년. 월. 일. 형식 처리 중 에러 발생")
            print(text)

        # 그 외의 형식 처리
        try:
            filtered_text = re.findall(r"[\d.]+", text)
            if filtered_text:
                result = datetime.strptime(filtered_text[0], "%Y.%m.%d.")
                return result.strftime("%Y-%m-%d")
        except ValueError:
            print("다른 형식 처리 중 에러 발생")
            print(text)
        return None

    def postprocess(self, text: str) -> tuple[int, list[dict]]:
        parsed_json = parse_json(text)
        portions = int(parsed_json["portions"]) if "portions" in parsed_json else 1
        ingredient_info = parsed_json["items"] if "items" in parsed_json else []

        if ingredient_info:
            ingredients_df = pd.DataFrame(ingredient_info)
            ingredients_df[["quantity", "unit", "vague"]] = ingredients_df.apply(
                self.convert_unit, axis=1
            )
            ingredients_df[["quantity", "unit", "vague"]] = ingredients_df.apply(
                self.convert_quantity, axis=1
            )
            ingredient_info = ingredients_df.to_dict(orient="records")

        return portions, ingredient_info

    def _query_to_gemini(self, gemini, video_text: str, menu_name: str):
        response = gemini.generate_content(
            SYSTEM_PROMPT + menu_name + "\n\n" + RECIPE_PROMPT + video_text
        )
        return response.text

    def _inference(
        self, video_text: str, menu_name: str, max_retry: int = 3
    ) -> tuple[int, list[dict]]:
        count = 0
        while count < max_retry:
            try:
                return self._query_to_gemini(self.gemini, video_text, menu_name)

            except exceptions.InvalidArgument as e:
                print(f"잘못된 인자: {e}")
            except exceptions.ResourceExhausted as e:
                print(f"리소스 소진 (할당량 초과): {e}")
            except exceptions.PermissionDenied as e:
                print(f"권한 거부 (API 키 문제 등): {e}")
            except exceptions.BadRequest as e:
                print(f"잘못된 요청: {e}")
            except exceptions.ServiceUnavailable as e:
                print(f"서비스 불가: {e}")
            except exceptions.DeadlineExceeded as e:
                print(f"요청 시간 초과: {e}")
            except Exception as e:
                print(f"알 수 없는 오류 발생: {e}")
            finally:
                count += 1
                print(f"Retry count: {count}")
                time.sleep(3)
        return None

    def inference(self, video_text: str, menu_name: str) -> tuple[int, list[dict]]:
        gemini_output = self._inference(video_text, menu_name)
        portions, ingredient_info = self.postprocess(gemini_output)
        return portions, ingredient_info
