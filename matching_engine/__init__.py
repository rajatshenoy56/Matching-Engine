from flask import Flask, Response, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

import json

app = Flask(__name__)
CORS(app)
response = Response()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from matching_engine import logic
from matching_engine import mockServer


@app.route('/hello')
def hello():

    return "Hello"


queue = logic.Order_Queue()
last_order_id = 0
unmatched_orders = []


@app.route('/')
def Demo():
    return render_template('/index.html')


@app.route('/place_order', methods=['POST'])
def place_order():

    # response.headers.add('Access-Control-Allow-Origin', '*')

    global last_order_id
    global queue
    last_order_id = last_order_id + 1
    
    order = logic.Stock(username=request.form['username'],
                        order_id=last_order_id,
                        stock_code=request.form['stock_code'],
                        trade_type=request.form['trade_type'],
                        price=float(request.form['price']),
                        quantity=int(request.form['quantity']),
                        order_type=request.form['order_type'],
                        flavor=request.form['flavor'])
    if(order.order_type == 'stop'):
        order.trigger_price=order.price
    queue.enqueue(order)

    match_list = queue.match(order)

    if (len(match_list) == 0):
        if (order.order_type == 'market'):
            unmatched_orders.append(order)

    return 'ACK'


@app.route('/history', methods=['POST'])
@cross_origin()
def history():
    unmatched = []
    matched = []
    queued = []

    username = request.form['username']

    for stock_code in queue.active_list.keys():
        for order in queue.active_list[stock_code]['Bid']:
            if (order.username == username):
                queued.append(order)
        for order in queue.active_list[stock_code]['Ask']:
            if (order.username == username):
                queued.append(order)

    for stock_code in queue.inactive_list.keys():
        for order in queue.inactive_list[stock_code]:
            if (order.username == username):
                queued.append(order)

    trades = logic.Trade.query.filter_by(buyer_name=username).all()
    if (len(trades) > 0):
        matched = matched + trades

    trades = logic.Trade.query.filter_by(seller_name=username).all()
    if (len(trades) > 0):
        matched = matched + trades

    for i in range(0, len(unmatched_orders)):
        unmatched.append(unmatched_orders[i].__repr__())
    for i in range(0, len(matched)):
        matched[i] = matched[i].__repr__()
    for i in range(0, len(queued)):
        queued[i] = queued[i].__repr__()

    return json.dumps({
        'unmatched': unmatched,
        'matched': matched,
        'queued': queued
    })


@app.route('/edit', methods=['POST'])
@cross_origin()

def edit():
    order_id = int(request.form['order_id'])

    price = float(request.form['price'])
    quantity = int(request.form['quantity'])
    flavor = request.form['flavor']

    target_order = None

    for stock_code in queue.active_list.keys():
        for order in queue.active_list[stock_code]['Bid']:
            if (order.order_id == order_id):
                target_order = order
                break
        for order in queue.active_list[stock_code]['Ask']:
            if (order.order_id == order_id):
                target_order = order
                break
    
    if target_order is not None:
        target_order.price = price
        target_order.quantity = quantity
        target_order.flavor = flavor

    return 'ACK'

@app.route('/remove', methods = ['POST'])
@cross_origin()

def remove():
    order_id = int(request.form['order_id'])
   
    for stock_code in queue.active_list.keys():
        queue.active_list[stock_code]['Bid'] = [order for order in queue.active_list[stock_code]['Bid'] if order.order_id != order_id]
        queue.active_list[stock_code]['Ask'] = [order for order in queue.active_list[stock_code]['Ask'] if order.order_id != order_id]
               
    for stock_code in queue.inactive_list.keys():
        queue.inactive_list[stock_code] = [order for order in queue.inactive_list[stock_code] if order.order_id != order_id]

    return 'ACK'


@app.route('/getPrice', methods=['GET'])
def getMarketPrice():
    to_be_activated=queue.activate(mockServer.stocks)
    for order in to_be_activated:
        match_list = queue.match(order)
        if (len(match_list) == 0):
            if (order.order_type == 'market'):
                unmatched_orders.append(order)
    return json.dumps(mockServer.stocks)
