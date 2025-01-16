from flask import render_template, session
from .models import get_products, get_categories

def products_view(category_id):
    categories = get_categories()
    products_dict = get_products(category_id)
    return render_template('mainmodule/index.html', products_by_subcategories=products_dict, categories=categories)

def order_view():
    return f'Ваш заказ отправлен на бар!'

def carts_view():
    return f'{session.get['cart']}'

def not_found_view():
    return render_template('404.html'), 404