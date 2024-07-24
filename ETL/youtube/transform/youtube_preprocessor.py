import os
import re
import time
from datetime import datetime, timedelta

import google.generativeai as genai
from dotenv import load_dotenv
from google.api_core import exceptions

from . import SYSTEM_PROMPT
from .utils import parse_json


class YoutubePreprocessor:
    def __init__(self):
        self.GOOGLE_API_KEY = None
        self.gemini = None

    def set_gemini_api(self, n):
        load_dotenv("../../../resources/secret.env")
        self.GOOGLE_API_KEY = os.environ.get(f"GOOGLE_API_KEY{n}", None)
        if self.GOOGLE_API_KEY is None:
            raise ValueError("GOOGLE_API_KEY is not set.")
        genai.configure(api_key=self.GOOGLE_API_KEY)
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
        return portions, ingredient_info

    def _query_to_gemini(self, gemini, video_text):
        response = gemini.generate_content(SYSTEM_PROMPT + video_text)
        return response.text

    def _inference(self, video_text: str, max_retry: int = 3) -> tuple[int, list[dict]]:
        count = 0
        while count < max_retry:
            try:
                if True:  # TODO: Fix validate logic
                    return self._query_to_gemini(self.gemini, video_text)

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
                time.sleep(3)
        return None

    def inference(self, video_text: str) -> tuple[int, list[dict]]:
        gemini_output = self._inference(video_text)
        portions, ingredient_info = self.postprocess(gemini_output)
        return portions, ingredient_info
