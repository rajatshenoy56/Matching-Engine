from matching_engine import db

class Stock(db.Model):
    order_id = db.Column(db.Integer, primary_key = True)
    stock_code = db.Column(db.Integer, nullable = False)
    trade_type = db.Column(db.String(10), nullable = False)  #Bid and Ask
    price = db.Column(db.Float, nullable = True)
    quantity = db.Column(db.Integer, nullable = False)
    order_type = db.Column(db.String(20),nullable = False)
    flavor = db.Column(db.String(20),nullable = False)
    username = db.Column(db.String(20), nullable = False)
    trigger_price = db.Column(db.Integer, nullable = True)
    # min_quantity = db.Column(db.Integer)

    def __repr__(self):
        return {
            'order_id': self.order_id,
            'trade_type': self.trade_type,
            'order_type': self.order_type,
            'quantity': self.quantity,
            'price': self.price,
            'trigger_price':self.trigger_price,
            'stock_code': self.stock_code,
            'flavor': self.flavor
        }

class Trade(db.Model):
    trade_id = db.Column(db.Integer, primary_key = True)
    buyer_name = db.Column(db.String(20), nullable = False)
    seller_name = db.Column(db.String(20),nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Float, nullable = False)
    stock_code = db.Column(db.Integer, db.ForeignKey('stock.stock_code'), nullable = False)

    def __repr__(self):
        return {
            'trade_id': self.trade_id,
            'buyer_name': self.buyer_name,
            'seller_name': self.seller_name,
            'quantity': self.quantity,
            'price': self.price,
            'stock_code': self.stock_code
        }

class UnMatched(db.Model):
    order_id = db.Column(db.Integer, primary_key = True)
    stock_code = db.Column(db.Integer, nullable = False)
    trade_type = db.Column(db.String(10), nullable = False)  #Bid and Ask
    price = db.Column(db.Float, nullable = True)
    quantity = db.Column(db.Integer, nullable = False)
    order_type = db.Column(db.String(20),nullable = False)
    flavor = db.Column(db.String(20),nullable = False)
    username = db.Column(db.String(20), nullable = False)
    trigger_price = db.Column(db.Integer, nullable = True)
    def __repr__(self):
        return {
            'order_id': self.order_id,
            'trade_type': self.trade_type,
            'order_type': self.order_type,
            'quantity': self.quantity,
            'price': self.price,
            'stock_code': self.stock_code,
            'flavor': self.flavor,
            'trigger_price':self.trigger_price
        }

class Queued(db.Model):
    order_id = db.Column(db.Integer, primary_key = True)
    stock_code = db.Column(db.Integer, nullable = False)
    trade_type = db.Column(db.String(10), nullable = False)  #Bid and Ask
    price = db.Column(db.Float, nullable = True)
    quantity = db.Column(db.Integer, nullable = False)
    order_type = db.Column(db.String(20),nullable = False)
    flavor = db.Column(db.String(20),nullable = False)
    username = db.Column(db.String(20), nullable = False)
    trigger_price = db.Column(db.Integer, nullable = True)
    def __repr__(self):
        return {
            'order_id': self.order_id,
            'trade_type': self.trade_type,
            'order_type': self.order_type,
            'quantity': self.quantity,
            'price': self.price,
            'stock_code': self.stock_code,
            'flavor': self.flavor,
            'trigger_price':self.trigger_price
        }

class InActive(db.Model):
    order_id = db.Column(db.Integer, primary_key = True)
    stock_code = db.Column(db.Integer, nullable = False)
    trade_type = db.Column(db.String(10), nullable = False)  #Bid and Ask
    price = db.Column(db.Float, nullable = True)
    quantity = db.Column(db.Integer, nullable = False)
    order_type = db.Column(db.String(20),nullable = False)
    flavor = db.Column(db.String(20),nullable = False)
    username = db.Column(db.String(20), nullable = False)
    trigger_price = db.Column(db.Integer, nullable = True)
    def __repr__(self):
        return {
            'order_id': self.order_id,
            'trade_type': self.trade_type,
            'order_type': self.order_type,
            'quantity': self.quantity,
            'price': self.price,
            'stock_code': self.stock_code,
            'flavor': self.flavor,
            'trigger_price':self.trigger_price
        }


db.create_all()
