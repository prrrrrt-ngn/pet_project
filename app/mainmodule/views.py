from flask import render_template, url_for
from .models import get_cocktails

def main_view():
    return render_template('mainmodule/main.html')

def drinks_view():
    cocktails = get_cocktails()
    return render_template('mainmodule/index.html', cocktails=cocktails)

def order_view():
    return f'Ваш заказ отправлен на бар!'

def not_found_view():
    return render_template('404.html'), 404