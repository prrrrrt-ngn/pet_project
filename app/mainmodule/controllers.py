from flask import Blueprint, render_template, request, g
from .models import get_db_connection
from .views import index_view, order_view, not_found_view
from app.services.telegram_service import send_to_telegram

main_module = Blueprint('mainmodule', __name__, template_folder='../templates')

@main_module.before_request
def conn():
    g.connection = get_db_connection()
    g.cursor = g.connection.cursor()

@main_module.after_request
def disconn(responce):
    if hasattr(g, 'connection'):
        g.connection.close()
    if hasattr(g, 'cursor'):
        g.cursor.close()
    return responce


@main_module.route('/', methods=["GET"])
def index():
    return index_view()


@main_module.route('/order', methods=["POST"])
def order():
    order = {}
    for cocktail_name, details in request.form.items():
        quantity = int(details)
        if quantity > 0:
            order[cocktail_name] = quantity
    
    send_to_telegram(order)
    return order_view()


@main_module.errorhandler(404)
def NotPage(error):
    return f'sasas'