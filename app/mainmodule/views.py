from flask import render_template, url_for
from .models import get_cocktails, get_food

def main_view():
    return render_template('mainmodule/main.html')

def drinks_view():
    cocktails_dict = get_cocktails()
    cocktails = list(cocktails_dict.values())
    return render_template('mainmodule/index.html', products=cocktails)

def food_view():
    food = get_food()
    return render_template('mainmodule/index.html', products=food)

def order_view():
    return f'Ваш заказ отправлен на бар!'

def not_found_view():
    return render_template('404.html'), 404