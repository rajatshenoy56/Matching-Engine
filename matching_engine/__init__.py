from flask import Flask,Response,render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

@app.route('/hello', methods=['POST', 'GET'])
def hello():
    
    return request.form['ABC']

from matching_engine import logic

queue = logic.Order_Queue()
last_order_id = 0


@app.route('/dashboard/')
def Demo():
    return render_template('/index.html')

@app.route('/place_order', methods=['POST', 'GET'])
def place_order():
    #response =Response()
    #response.headers["Access-Control-Allow-Origin"] = "*"
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
   
    return  str(queue.match(order))
