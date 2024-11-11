from flask import Flask, render_template, g
from mainmodule.models import get_db_connection
app = Flask(__name__)

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

@app.errorhandler(404)
def NotPage(error):
    return (render_template('404.html'), 404)

if __name__ == "__main__":
    app.run()