from flask import Flask, render_template, request, g, redirect
import requests
import psycopg2
from config import host, user, password, db_name

app = Flask(__name__)

def get_db_connection():
    if 'connection' not in g:
        try:
            g.connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
        except Exception as _ex:
            print("[INFO] ОШИБКА", _ex)
        return g.connection

@app.before_request
def conn():
    g.connection = get_db_connection()
    g.cursor = g.connection.cursor()

@app.after_request
def disconn(responce):
    if hasattr(g, 'connection'):
        g.connection.close()
    if hasattr(g, 'cursor'):
        g.cursor.close()
    return responce


@app.route('/', methods=["GET"])
def index():
    g.cursor.execute(
        "SELECT cocktails.cocktail_id, cocktails.name, ingredients.name "
        "FROM recipes "
        "JOIN ingredients ON recipes.ingredient_id = ingredients.ingredient_id " 
        "JOIN cocktails ON recipes.cocktail_id = cocktails.cocktail_id"
    )
    rows = g.cursor.fetchall()
    cocktails = {}
    for cocktail_id, cocktail_name, ingredient_name in rows:
        if cocktail_name not in cocktails:
            cocktails[cocktail_name] = {'id': cocktail_id, 'ingredients': []}
        cocktails[cocktail_name]['ingredients'].append(ingredient_name)
    print (cocktails)
    return render_template('index.html', cocktails=cocktails)


@app.route('/order', methods=["POST"])
def order():
    order = {}
    for cocktail_name, details in request.form.items():
        quantity = int(details)
        if quantity > 0:
            order[cocktail_name] = quantity
    print(request.form.items())

    send_to_telegram(order)
    return f'Ваш заказ отправлен на бар!'


def send_to_telegram(order):
    bot_token = '6433487048:AAGQLVcaUaFJJxLiE4a-z046_4-Evn7ztwo'
    chat_id = '705153780'
    message_lines = [f'Новый заказ:']
    for cocktail_name, quantity in order.items():
        message_lines.append(f'{cocktail_name} - {quantity} шт')
    
    message = '\n'.join(message_lines)
    
    # Отправляем сообщение в Telegram
    requests.get(f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}')

@app.errorhandler(404)
def NotPage(error):
    return (render_template('404.html'), 404)

if __name__ == "__main__":
    app.run(debug=True)