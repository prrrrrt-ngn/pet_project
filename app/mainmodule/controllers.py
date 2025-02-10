from flask import Blueprint, request, g, redirect, url_for, session, jsonify
from .models import get_db_connection, get_products
from .views import products_view, not_found_view, order_view
from ..services.telegram_service import send_to_telegram

main_module = Blueprint('mainmodule', __name__, template_folder='../templates')


@main_module.before_request
def before_request():
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


@main_module.route('/add_to_order', methods=["POST"])
def add_to_order():
    try:
        data = request.get_json()
        category_id = data.get("category_id")
        products = data.get("products", [])

        if not category_id or not products:
            return jsonify({"error": "Category ID or products are missing"}), 400
        
        valid_products = {p['name'] for _, products in get_products(category_id).items() for p in products}
    
        if 'order' not in session:
            session['order'] = []

        for product in products:
            product_name = product.get("id")
            quantity = product.get("quantity")

            if product_name not in valid_products or quantity <= 0:
                continue

            for item in session['order']:
                if product_name in item:
                    item[product_name] += quantity
                    break
            else:
                session['order'].append({product_name: quantity})
        session.modified = True

        return jsonify({"message": "Order successfully update"}), 200
    
    except Exception as e:
        return jsonify({"error": f"An error occurres: {str(e)}"}), 500


@main_module.route('/order', methods=["GET", "POST"])
def order():
    if request.method == "POST":
        try:
            data = request.get_json()
            product_to_remove = data.get('product')
            if product_to_remove and 'order' in session:
                removedFlag = False
                new_order = []
                for item in session['order']:
                    if product_to_remove in item:
                        del item[product_to_remove]
                        removedFlag = True
                    if item:
                        new_order.append(item)
                if removedFlag == False:
                    return jsonify({"message": 'Такой позиции нет в заказе'}), 200
                session['order'] = new_order
                session.modified = True
                print(session['order'])
                return jsonify({"message": 'Успешно удалена позиция!'}), 200
            
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    if 'order' not in session:
        session['order'] = []
    return order_view(session['order'])


@main_module.route('/confirm_order', methods=["POST"])
def confirm_order():
    try:
        data = request.get_json()
        if not data.get('order'):
            return jsonify({"error": "Заказ пуст"}), 400
        ready_order = data.get('order')
        send_to_telegram(ready_order)
        return jsonify({"message": "Заказ подтвержден!"}), 200
    
    except Exception as e:
        return jsonify({"error": f"An error occurres: {str(e)}"}), 500

@main_module.errorhandler(404)
def NotPage(error):
    return not_found_view()