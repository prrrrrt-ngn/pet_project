from flask import Blueprint, request, g, redirect, url_for, session
from .models import get_db_connection
from .views import products_view, order_view, not_found_view, carts_view
from app.services.telegram_service import send_to_telegram

main_module = Blueprint('mainmodule', __name__, template_folder='../templates')

@main_module.before_request
def conn():
    g.connection = get_db_connection()
    g.cursor = g.connection.cursor()
#соединение с бд

@main_module.after_request
def disconn(responce):
    if hasattr(g, 'connection'):
        g.connection.close()
    if hasattr(g, 'cursor'):
        g.cursor.close()
    return responce
#закрытие соединения с бд

@main_module.route('/', methods=['GET'])
def main():
    return redirect(url_for('mainmodule.products', category_id=1))
#редирект на страницу 1 страницу меню, здесь лучше заменить в будущем на главную страницу

@main_module.route('/products/category/<string:category_id>', methods=["GET"])
def products(category_id):
    return products_view(category_id)
#контроллер отображения страницы меню (айди категории передается с url в функцию)


# @main_module.route('/order', methods=["POST"])
# def order():
#     order = {}
#     for cocktail_name, details in request.form.items():
#         quantity = int(details)
#         if quantity > 0:
#             order[cocktail_name] = quantity
    
#     send_to_telegram(order)
#     return order_view()
#обработчик пост запроса для вывода в тг


@main_module.route('/order', methods=["POST"])
def order():
    order = {}
    for cocktail_name, details in request.form.items():
        quantity = int(details)
        if quantity > 0:
            order[cocktail_name] = quantity
    if 'cart' not in session:
        session['cart'] = []
    
    session['cart'].append(order)
    session.modified = True
    
    return redirect(url_for('mainmodule.products', category_id=1))


@main_module.route('/carts', methods=["GET"])
def cart():
    return carts_view()


@main_module.errorhandler(404)
def NotPage(error):
    return not_found_view()