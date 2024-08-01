import psycopg2

def load_to_rds(ingredient_result):
    conn = psycopg2.connect(
        dbname=Variable.get("dbname"),
        user=Variable.get("user"),
        password=Variable.get("password"),
        host=Variable.get("host"),
        port="5432",
    )

# unit conversion에 하나라도 매칭이 안되는 값이 있다면 레시피를 제외한다.
# 1. quantity 2. unit 3. u -> q 
# product에 있는지 unit과 gram을 비교해야함.
# vague는 수량의 개념이없음.

    query = """
        CREATE VIEW ingre_conn_cheap_product_view2 AS 
        WITH convert_ingredient_unit AS (
            SELECT
                i.name
                ,i.recipe_id
                ,i.cheapest_product_id
                ,COALESCE((i.quantity * u.converted_vol), i.quantity) AS quantity
                ,COALESCE(u.standard_unit, i.unit,i.vague) AS unit
            FROM 
                ingredient i LEFT JOIN unit_conversion u ON i.unit = u.unit_name
        )
        , convert_ingredient_quantity AS (
            SELECT
                i.name
                ,i.recipe_id
                ,cheapest_product_id
                ,CASE WHEN u.converted_gram IS NOT NULL THEN u.converted_gram ELSE i.quantity END AS quantity
                ,CASE WHEN u.converted_gram IS NOT NULL THEN 'g' ELSE i.unit END AS unit
            FROM 
                convert_ingredient_unit i LEFT JOIN quantity_conversion u 
                    ON i.name = u.ingredient_name AND i.unit = u.unit_name
        )
        SELECT
            i.name
            ,i.recipe_id
            ,i.quantity
            ,p.unit_price
            ,(i.quantity * p.unit_price) AS ingredient_price
        FROM
            convert_ingredient_quantity i JOIN product p
                ON i.cheapest_product_id = p.id AND i.unit = p.unit
        ;

        DELETE FROM cheap_recipe;

        INSERT INTO cheap_recipe (recipe_id, menu, youtube_url, min_total_price)
            SELECT
                i.recipe_id
                ,m.name AS menu
                ,y.youtube_url
                ,SUM(i.ingredient_price) AS min_total_price
            FROM
                ingre_conn_cheap_product_view2 i
            JOIN recipe r ON i.recipe_id = r.id
            JOIN menu m ON r.menu_id = m.id
            JOIN youtube_vdo y ON y.id = r.youtube_vdo_id
            GROUP BY 1,2,3;
    """

    try:
        cur = conn.cursor()
        cur.execute(drop_create_table_query)
        cur.executemany(insert_query, ingredient_result[1:])
        conn.commit()
        cur.close()
        conn.close()
        print("Table created or replaced and data inserted successfully!")

    except Exception as e:
        print("Error:", e)