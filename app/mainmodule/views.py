from flask import render_template
from .models import get_products, get_categories

def products_view(category_id):
    categories = get_categories()
    products_dict = get_products(category_id)
    return render_template('mainmodule/index.html', products_by_subcategories=products_dict, categories=categories)

def cart_view(cart):
    return render_template('mainmodule/cart.html', cart = cart)

def not_found_view():
    return render_template('404.html'), 404