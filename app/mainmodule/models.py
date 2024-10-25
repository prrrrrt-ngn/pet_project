from flask import g
import psycopg2
from config import Config

def get_db_connection():
    if 'connection' not in g:
        try:
            g.connection = psycopg2.connect(
                host=Config.host,
                user=Config.user,
                password=Config.password,
                database=Config.db_name
            )
        except Exception as _ex:
            print("[INFO], ошибка", _ex)
    return g.connection


def get_categories():
    g.cursor.execute(
        "SELECT * "
        "FROM categories" 
    )
    rows = g.cursor.fetchall()
    categories = []
    for category_id, category_name, subcategory in rows:
        categories.append({'id': category_id, 'name': category_name, 'subcategory': subcategory})
    return (categories)

def get_products(category_id):
    g.cursor.execute(
        """
        SELECT products.product_id, products.name, ingredients.name, products.price
        FROM products 
        LEFT JOIN recipes ON products.product_id = recipes.product_id 
        LEFT JOIN ingredients ON recipes.ingredient_id = ingredients.ingredient_id 
        WHERE products.category = %s
        """,
        (category_id,)
    )
    rows = g.cursor.fetchall()
    print(rows)
    cocktails = {}
    for cocktail_id, cocktail_name, ingredient_name, price in rows:
        if cocktail_id not in cocktails:
            cocktails[cocktail_id] = ({'id': cocktail_id, 'name': cocktail_name, 'ingredients': [], 'price': str(price)})
        cocktails[cocktail_id]['ingredients'].append(ingredient_name)
    return (cocktails)


def get_food():
    g.cursor.execute(
        "SELECT * "
        "FROM food"
    )
    rows = g.cursor.fetchall()
    food = []
    for food_id, food_name, price in rows:
        food.append({'id': food_id, 'name': food_name, 'price': str(price)})
    return (food)