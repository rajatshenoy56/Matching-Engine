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
from matching_engine.models import UnMatched, Queued, InActive
from random import seed, randint

queue = logic.Order_Queue()
unmatched_orders = []


@app.route('/hello')
def hello():
    return "Hello"


def loadData():
    global unmatched_orders
    global queue
    print('unmatched')
    for order in UnMatched.query.all():
        stock = logic.Stock(
                            username   = order.username,
                            order_id   = order.order_id,
                            trade_type = order.trade_type,
                            order_type = order.order_type,
                            quantity   = order.quantity,
                            price      = order.price,
                            stock_code = order.stock_code,
                            flavor     = order.flavor,
                            trigger_price= (order.trigger_price or 0)
                           )

        unmatched_orders.append(stock)
        print(json.dumps(stock.__repr__()))
        db.session.delete(order)
    print('queued')

    for order in Queued.query.all():
        stock = logic.Stock(
                            username   = order.username,
                            order_id   = order.order_id,
                            trade_type = order.trade_type,
                            order_type = order.order_type,
                            quantity   = order.quantity,
                            price      = order.price,
                            stock_code = order.stock_code,
                            flavor     = order.flavor,
                            trigger_price= (order.trigger_price or 0)
                           )

        queue.enqueue(stock)
        print(json.dumps(stock.__repr__()))
        db.session.delete(order)
    print('inactive')

    for order in InActive.query.all():
        stock = logic.Stock(
                            username   = order.username,
                            order_id   = order.order_id,
                            trade_type = order.trade_type,
                            order_type = order.order_type,
                            quantity   = order.quantity,
                            price      = order.price,
                            stock_code = order.stock_code,
                            flavor     = order.flavor,
                            trigger_price= (order.trigger_price or 0)
                           )

        queue.enqueue(stock)
        print(json.dumps(stock.__repr__()))
        db.session.delete(order)

    db.session.commit()


loadData()

@app.route('/')
def Demo():
    return render_template('/index.html')


@app.route('/place_order', methods=['POST'])
def place_order():
    global queue

    order = logic.Stock(
                        username    = request.form['username'],
                        order_id    = randint(10000, 99999),
                        stock_code  = request.form['stock_code'],
                        trade_type  = request.form['trade_type'],
                        price       = 0,
                        quantity    = int(request.form['quantity']),
                        order_type  = request.form['order_type'],
                        flavor      = request.form['flavor']
                       )

    if(order.order_type == 'stoplimit'):
        order.trigger_price=float(request.form['trigger_price'])
        order.price=float(request.form['price'])
    elif(order.order_type == 'stop'):
        order.trigger_price=float(request.form['trigger_price'])
    else:
        order.price=float(request.form['price'])
    queue.enqueue(order)
    #print(order.price)
    match_list = queue.match(order)
    #print(order.price)
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
        if unmatched_orders[i].username == username:
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
    if(request.form['order_type'] != 'stop'):
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

        if(target_order.order_type != 'stop'):
            target_order.price = price

        target_order.quantity = quantity
        target_order.flavor = flavor

        if target_order.order_type == 'stop':
            target_order.trigger_price = price
        elif target_order.order_type == 'stoplimit':
            target_order.trigger_price = request.form['trigger_price']


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


def saveData():
    for order in unmatched_orders :
        unmatched = UnMatched(
                                username = order.username,
                                order_id = order.order_id,
                                trade_type = order.trade_type,
                                order_type = order.order_type,
                                quantity = order.quantity,
                                price = order.price,
                                stock_code = order.stock_code,
                                flavor = order.flavor,
                                trigger_price= (order.trigger_price or 0)
                             )

        db.session.add(unmatched)

    for stock_code in queue.active_list.keys():
        for order in queue.active_list[stock_code]['Bid'] :
            queued = Queued(
                                username = order.username,
                                order_id = order.order_id,
                                trade_type = order.trade_type,
                                order_type = order.order_type,
                                quantity = order.quantity,
                                price = order.price,
                                stock_code = order.stock_code,
                                flavor = order.flavor,
                                trigger_price= (order.trigger_price or 0)
                             )
            db.session.add(queued)

        for order in queue.active_list[stock_code]['Ask'] :
            queued = Queued(
                                username = order.username,
                                order_id = order.order_id,
                                trade_type = order.trade_type,
                                order_type = order.order_type,
                                quantity = order.quantity,
                                price = order.price,
                                stock_code = order.stock_code,
                                flavor = order.flavor,
                                trigger_price= (order.trigger_price or 0)
                             )
            db.session.add(queued)

    for stock_code in queue.inactive_list.keys():
        for order in queue.inactive_list[stock_code] :
            inactive = InActive(
                                username   = order.username,
                                order_id   = order.order_id,
                                trade_type = order.trade_type,
                                order_type = order.order_type,
                                quantity   = order.quantity,
                                price      = order.price,
                                stock_code = order.stock_code,
                                flavor     = order.flavor
                               )
            db.session.add(inactive)

    db.session.commit()

import atexit
atexit.register(saveData)