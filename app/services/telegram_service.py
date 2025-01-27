import os
import requests
import urllib.parse

def send_to_telegram(ready_order):
    print(ready_order)
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    message_lines = [f'Новый заказ:']

    for order_item in ready_order:
        product_name = order_item.get('product')
        quantity = order_item.get('quantity')
        
        if product_name and quantity:
            product_name_encoded = urllib.parse.quote(product_name)
            message_lines.append(f'{product_name_encoded} - {quantity} шт')
    
    message = '\n'.join(message_lines)
    
    requests.get(f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}')
