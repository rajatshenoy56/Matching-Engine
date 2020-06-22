from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from matching_engine import logic
from matching_engine import mockServer

@app.route('/hello')
def hello():
    return 'hello'


queue = logic.Order_Queue()
last_order_id = 0


@app.route('/place_order', methods=['POST', 'GET'])
def place_order():

    global last_order_id
    global queue
    last_order_id = last_order_id + 1

    order = logic.Stock(
                        order_id   = last_order_id,
                        stock_code = request.form['stock_code'],
                        trade_type = request.form['trade_type'],
                        price      = float(request.form['price']),
                        quantity   = int(request.form['quantity']),
                        order_type = request.form['order_type'],
                        flavor     = request.form['flavor']
                       )

    queue.enqueue(order)

    return queue.match(order)

@app.route('/getPrice')
def getMarketPrice():
    return json.dumps(mockServer.stocks)