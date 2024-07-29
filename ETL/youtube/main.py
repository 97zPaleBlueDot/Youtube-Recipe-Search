import os
import time

import psycopg2
from dotenv import load_dotenv
from extract.youtube_crawler import YoutubeCrawler
from load.youtube_loader import YoutubeLoader
from transform.youtube_preprocessor import YoutubePreprocessor


if __name__ == "__main__":
    # 데이터베이스 연결
    database = "test"
    load_dotenv("../../resources/secret.env")
    conn_info = {
        "host": os.getenv("DB_HOST"),
        "database": database,
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
    }
    try:
        conn = psycopg2.connect(**conn_info)
        cursor = conn.cursor()
        print("Database connected successfully!")
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)

    youtube_crawler = YoutubeCrawler()
    youtube_crawler.set_webdriver()

    youtube_preprocessor = YoutubePreprocessor()
    youtube_preprocessor.set_gemini_api(0)

    youtube_loader = YoutubeLoader(conn=conn, cursor=cursor)

    menu_id_and_name_list = youtube_crawler.get_menu_id_and_name_list(cursor=cursor)

    for n in range(5):
        youtube_crawler.set_youtube_api(n)
        for i in range(
            n * 100, len(menu_id_and_name_list)
        ):  # api 당 최대 100개의 음식명 검색 가능.
            print("*" * 80)
            print("menu_id_and_name_list index:", i)
            menu_id = menu_id_and_name_list[i][0]
            menu_name = menu_id_and_name_list[i][1]
            try:
                video_link_list = youtube_crawler.search_menu_name(menu_name)
            except Exception:
                break

            for j in range(len(video_link_list)):
                print("video_link_list index:", j)
                video_link = video_link_list[j]
                try:
                    (
                        video_thumbnail,
                        video_title,
                        channel_img,
                        channel_name,
                        channel_link,
                        channel_subscribers_count,
                        video_thumbsup_count,
                        video_views_count,
                        video_uploaded_date,
                        video_text,
                    ) = youtube_crawler.get_video_infos(video_link)
                except Exception:
                    youtube_crawler.set_webdriver()
                    continue
                time.sleep(0.01)

                # 채널 관련 데이터
                channel_link = youtube_preprocessor.preprocess(channel_link)
                channel_name = youtube_preprocessor.preprocess(channel_name)
                channel_img = youtube_preprocessor.preprocess(channel_img)
                channel_subscribers_count = youtube_preprocessor.convert_to_number(
                    channel_subscribers_count.strip()[:-1]
                )

                # 유튜브 비디오 관련 데이터
                video_link = youtube_preprocessor.preprocess(video_link)
                video_title = youtube_preprocessor.preprocess(video_title)
                video_thumbnail = youtube_preprocessor.preprocess(video_thumbnail)
                video_thumbsup_count = youtube_preprocessor.convert_to_number(
                    video_thumbsup_count
                )
                video_views_count = youtube_preprocessor.convert_to_number(
                    video_views_count
                )
                video_uploaded_date = youtube_preprocessor.convert_to_date(
                    video_uploaded_date
                )
                video_text = youtube_preprocessor.preprocess(video_text)

                # 레시피 관련 데이터.
                # 예시
                # portions: int = 1
                # ingredient_info: list[dict]
                # [
                #    {'ingredient': '주꾸미', 'quantity': 13, 'unit': '마리', 'vague': ''},
                #    {'ingredient': '양파', 'quantity': 1, 'unit': '개', 'vague': ''},
                #    {'ingredient': '대파', 'quantity': 1, 'unit': '개', 'vague': ''},
                #    {'ingredient': '당근', 'quantity': 0, 'unit': '', 'vague': '조금'},
                #    {'ingredient': '홍고추', 'quantity': 1, 'unit': '개', 'vague': ''},
                #    ...
                # ]
                portions, ingredient_info = youtube_preprocessor.inference(video_text)

                # db write 코드 작성
                try:
                    channel_id = youtube_loader.write_to_channel(
                        name=channel_name,
                        url=channel_link,
                        subscribers_count=channel_subscribers_count,
                        img_src=channel_img,
                    )
                    youtube_video_id = youtube_loader.write_to_youtube_video(
                        channel_id=channel_id,
                        title=video_title,
                        url=video_link,
                        thumbnail_src=video_thumbnail,
                        views=video_views_count,
                        thumbsup_count=video_thumbsup_count,
                        uploaded_date=video_uploaded_date,
                    )
                    recipe_id = youtube_loader.write_to_recipe(
                        youtube_video_id=youtube_video_id,
                        menu_id=menu_id,
                        full_text=video_text,
                    )
                    if ingredient_info:
                        for k in range(len(ingredient_info)):
                            ingredient_name = ingredient_info[k]["ingredient"]
                            quantity = ingredient_info[k]["quantity"]
                            unit = ingredient_info[k]["unit"]
                            vague = ingredient_info[k]["vague"]
                            # TODO: db 쿼리 수정
                            youtube_loader.write_to_ingredient(
                                recipe_id=recipe_id,
                                name=ingredient_name,
                            )
                except Exception as e:
                    print(f"에러 발생 : {e}")

    youtube_crawler.quit_webdriver()

    if conn:
        cursor.close()
        conn.close()
        print("DB Connection closed.")
