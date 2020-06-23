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
unmatched_orders = []

@app.route('/place_order', methods=['POST'])
def place_order():

    global last_order_id
    global queue
    last_order_id = last_order_id + 1

    order = logic.Stock(
                        username   = request.form['username'],
                        order_id   = last_order_id,
                        stock_code = request.form['stock_code'],
                        trade_type = request.form['trade_type'],
                        price      = float(request.form['price']),
                        quantity   = int(request.form['quantity']),
                        order_type = request.form['order_type'],
                        flavor     = request.form['flavor']
                       )

    queue.enqueue(order)

    match_list = queue.match(order)

    if(len(match_list) == 0):
        if(order.order_type == 'market'):
            unmatched_orders.append(order)

    return 'ACK'

@app.route('/history', methods=['POST', 'GET'])
def history():
    unmatched = unmatched_orders
    matched = []
    queued = []

    username = request.args.get('username')

    for stock_code in queue.active_list.keys():
        for order in queue.active_list[stock_code]['Bid']:
            if(order['username'] == username):
                queued.append(order)
        for order in queue.active_list[stock_code]['Ask']:
            if(order['username'] == username):
                queued.append(order)

    for stock_code in queue.inactive_list.keys():
        for order in queue.active_list[stock_code]:
            if(order['username'] == username):
                queued.append(order)

    trades = logic.Trade.query.filter_by(buyer_name=username).all()
    if(len(trades) > 0):
        matched = matched + trades
    
    
    trades = logic.Trade.query.filter_by(seller_name=username).all()
    if(len(trades) > 0):
        matched = matched + trades

    for i in range(0, len(unmatched)):
        unmatched[i] = unmatched[i].__repr__()
    for i in range(0, len(matched)):
        matched[i] = matched[i].__repr__()
    for i in range(0, len(queued)):
        queued[i] = queued[i].__repr__()

    return json.dumps({
        'unmatched': unmatched_orders,
        'matched': matched,
        'queued': queued
    })

@app.route('/getPrice')
def getMarketPrice():
    return json.dumps(mockServer.stocks)