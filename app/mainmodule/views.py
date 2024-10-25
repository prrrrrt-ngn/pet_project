from flask import render_template
from .models import get_products, get_food, get_categories


def main_view():
    return render_template('mainmodule/main.html')

def products_view(category_id):
    categories = get_categories()
    products_dict = get_products(category_id)
    products = list(products_dict.values())
    return render_template('mainmodule/index.html', products=products, categories=categories)

def order_view():
    return f'Ваш заказ отправлен на бар!'

def not_found_view():
    return render_template('404.html'), 404