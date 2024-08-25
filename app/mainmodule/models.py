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


def get_cocktails():
    g.cursor.execute(
        "SELECT cocktails.cocktail_id, cocktails.name, ingredients.name, cocktails.price "
        "FROM recipes "
        "JOIN cocktails ON recipes.cocktail_id = cocktails.cocktail_id "
        "JOIN ingredients ON recipes.ingredient_id = ingredients.ingredient_id"
    )
    rows = g.cursor.fetchall()
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