from flask import Blueprint, request, g, redirect, url_for, session, jsonify
from .models import get_db_connection, get_products
from .views import products_view, not_found_view, cart_view
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


@main_module.route('/order', methods=["POST"])
def order():
    order = {}
    category_id = request.form.get('category')
    if not category_id:
        return jsonify({"error": "Category ID is missing"}), 400

    products_in_menu = get_products(category_id)
    product_names_in_menu = set()

    for subcategory, products in products_in_menu.items():
        for product in products:
            product_names_in_menu.add(product['name'])

    for cocktail_name, details in request.form.items():
        if cocktail_name == 'category':
            continue
        quantity = int(details)
        if quantity > 0:
            if cocktail_name in product_names_in_menu:
                if 'cart' not in session:
                    session['cart'] = []

                # Проверяем, существует ли продукт уже в корзине
                product_exists = False
                for item in session['cart']:
                    if cocktail_name in item:
                        item[cocktail_name] += quantity
                        product_exists = True
                        break

                # Если продукт не существует в корзине, добавляем его
                if not product_exists:
                    session['cart'].append({cocktail_name: quantity})

                session.modified = True
            else:
                return jsonify({"error": f"Product {cocktail_name} not found in menu"}), 400

    return redirect(url_for('mainmodule.products', category_id=category_id))




@main_module.route('/cart', methods=["GET", "POST"])
def cart():
    if request.method == "POST":
        product_to_remove = request.form.get('product')
        if product_to_remove and 'cart' in session:
            for item in session['cart']:
                if product_to_remove in item:
                    del item[product_to_remove]
                    session.modified = True
                    break
        return redirect(url_for('mainmodule.cart'))
    
    return cart_view(session.get('cart', {}))


@main_module.errorhandler(404)
def NotPage(error):
    return not_found_view()