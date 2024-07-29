from __future__ import annotations

import psycopg2


class YoutubeLoader:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def write_to_youtube_video(self, menu_id, youtube_url, full_text):
        try:
            # Check if the video with the same URL exists
            self.cursor.execute(
                "SELECT id FROM youtube_vdo WHERE youtube_url = %s", (youtube_url,)
            )
            existing_video = self.cursor.fetchone()

            if existing_video:
                # If the video already exists, return its ID
                video_id = existing_video[0]
                print(
                    "Video with the same URL already exists. Returning existing video ID:",
                    video_id,
                )
            else:
                # If the video doesn't exist, insert new data and return its ID
                insert_query = "INSERT INTO youtube_vdo (menu_id, youtube_url, full_text) VALUES (%s, %s, %s) RETURNING id"
                self.cursor.execute(
                    insert_query,
                    (menu_id, youtube_url, full_text),
                )
                video_id = self.cursor.fetchone()[0]
                self.conn.commit()
                print("New video data inserted successfully. New video ID:", video_id)

            return video_id
        except (Exception, psycopg2.Error) as error:
            print("Error while writing to youtube_vdo table:", error)
            self.conn.rollback()

    def write_to_recipe(self, youtube_vdo_id, menu_id, portions):
        try:
            # Check if the recipe with the same youtube_vdo_id and menu_id exists
            self.cursor.execute(
                "SELECT id FROM recipe WHERE youtube_vdo_id = %s AND menu_id = %s",
                (youtube_vdo_id, menu_id),
            )
            existing_recipe = self.cursor.fetchone()

            if existing_recipe:
                # If the recipe already exists, do nothing
                recipe_id = existing_recipe[0]
                print(
                    "Recipe with the same youtube_vdo_id and menu_id already exists. Skipping insertion."
                )
            else:
                # If the recipe doesn't exist, insert new data
                insert_query = "INSERT INTO recipe (youtube_vdo_id, menu_id, portions) VALUES (%s, %s, %s) RETURNING id"
                self.cursor.execute(insert_query, (youtube_vdo_id, menu_id, portions))
                recipe_id = self.cursor.fetchone()[0]
                self.conn.commit()
                print(
                    "New recipe data inserted successfully. New recipe ID:", recipe_id
                )

            return recipe_id
        except (Exception, psycopg2.Error) as error:
            print("Error while writing to recipe table:", error)
            self.conn.rollback()

    def write_to_ingredient(
        self, name, quantity, unit, vague, alternative_id=None, cheapest_product_id=None
    ):
        try:
            # Check if the ingredient with the same name, quantity, unit, and vague exists
            self.cursor.execute(
                "SELECT id FROM ingredient WHERE name = %s AND quantity = %s AND unit = %s AND vague = %s",
                (name, quantity, unit, vague),
            )
            existing_ingredient = self.cursor.fetchone()

            if existing_ingredient:
                # If the ingredient already exists, do nothing
                print(
                    "Ingredient with the same name, quantity, unit, and vague already exists. Skipping insertion."
                )
            else:
                # If the ingredient doesn't exist, insert new data
                insert_query = """
                INSERT INTO ingredient (name, quantity, unit, vague, alternative_id, cheapest_product_id)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
                """
                self.cursor.execute(
                    insert_query,
                    (name, quantity, unit, vague, alternative_id, cheapest_product_id),
                )
                ingredient_id = self.cursor.fetchone()[0]
                self.conn.commit()
                print(
                    "New ingredient data inserted successfully. New ingredient ID:",
                    ingredient_id,
                )
                return ingredient_id

        except (Exception, psycopg2.Error) as error:
            print("Error while writing to ingredient table:", error)
            self.conn.rollback()

    def get_or_create_ingredient(self, name, quantity, unit, vague):
        try:
            self.cursor.execute("SELECT id FROM ingredient WHERE name = %s", (name,))
            existing_ingredient = self.cursor.fetchone()
            if existing_ingredient:
                ingredient_id = existing_ingredient[0]
                print(
                    "Ingredient already exists. Returning existing ingredient ID:",
                    ingredient_id,
                )
            else:
                insert_query = "INSERT INTO ingredient (name, quantity, unit, vague) VALUES (%s, %s, %s, %s) RETURNING id"
                self.cursor.execute(insert_query, (name, quantity, unit, vague))
                ingredient_id = self.cursor.fetchone()[0]
                self.conn.commit()
                print(
                    "New ingredient data inserted successfully. New ingredient ID:",
                    ingredient_id,
                )
            return ingredient_id
        except (Exception, psycopg2.Error) as error:
            print("Error while writing to ingredient table:", error)
            self.conn.rollback()

    def write_to_recipe_ingredient(
        self, recipe_id, ingredient_name, quantity, unit, vague
    ):
        try:
            # Check if the relationship already exists
            ingredient_id = self.get_or_create_ingredient(
                ingredient_name, quantity, unit, vague
            )
            self.cursor.execute(
                "SELECT id FROM recipe_ingredient WHERE recipe_id = %s AND ingredient_id = %s",
                (recipe_id, ingredient_id),
            )
            existing_relation = self.cursor.fetchone()

            if existing_relation:
                # If the relationship already exists, return its ID
                relation_id = existing_relation[0]
                print(
                    "Relationship with the same recipe_id and ingredient_id already exists. Returning existing relation ID:",
                    relation_id,
                )
            else:
                # If the relationship doesn't exist, insert new data and return its ID
                insert_query = "INSERT INTO recipe_ingredient (recipe_id, ingredient_id) VALUES (%s, %s) RETURNING id"
                self.cursor.execute(insert_query, (recipe_id, ingredient_id))
                relation_id = self.cursor.fetchone()[0]
                self.conn.commit()
                print(
                    "New relationship data inserted successfully. New relation ID:",
                    relation_id,
                )
        except (Exception, psycopg2.Error) as error:
            print("Error while writing to recipe_ingredient table:", error)
            self.conn.rollback()
