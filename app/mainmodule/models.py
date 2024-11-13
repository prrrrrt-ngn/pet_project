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
        SELECT products.product_id, products.name, ingredients.name, products.price, categories.name
        FROM products
        LEFT JOIN recipes ON products.product_id = recipes.product_id
        LEFT JOIN ingredients ON recipes.ingredient_id = ingredients.ingredient_id
        JOIN categories ON products.category = categories.category_id
        LEFT JOIN categories AS parent_categories ON categories.subcategory = parent_categories.subcategory
        WHERE (categories.category_id = %s OR categories.subcategory = %s)
        ORDER BY products.name;

        """,
        (category_id, category_id)
    )
    rows = g.cursor.fetchall()
    print(rows)
    cocktails_per_subcategory = {}
    for cocktail_id, cocktail_name, ingredient_name, price, subcategory in rows:
        if subcategory not in cocktails_per_subcategory:
                cocktails_per_subcategory[subcategory] = []

        # Проверяем генераторным выражением, проходящему по всем продуктам в подкатегории, добавлен он уже или нет
        product = next((c for c in cocktails_per_subcategory[subcategory] if c['id'] == cocktail_id), None)

        # Если продукта нет, то добавляем
        if not product:
            product = {'id': cocktail_id, 'name': cocktail_name, 'ingredients': [], 'price': str(price)}
            cocktails_per_subcategory[subcategory].append(product)

        # В любом случае через ссылку, указывающую на нужный продукт добавляем новый ингредиент
        product['ingredients'].append(ingredient_name)
        
    print('-------------------------')
    print(cocktails_per_subcategory)
    return (cocktails_per_subcategory)


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