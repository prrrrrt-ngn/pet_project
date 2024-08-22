import os
import requests

def send_to_telegram(order):
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    message_lines = [f'Новый заказ:']
    for cocktail_name, quantity in order.items():
        message_lines.append(f'{cocktail_name} - {quantity} шт')
    
    message = '\n'.join(message_lines)
    
    requests.get(f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}')
