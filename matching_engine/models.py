from matching_engine import db

class Stock(db.Model):
    order_id = db.Column(db.Integer, primary_key = True)
    stock_code = db.Column(db.Integer, nullable = False)
    trade_type = db.Column(db.String(10), nullable = False)  #Bid and Ask
    price = db.Column(db.Float, nullable = True)
    quantity = db.Column(db.Integer, nullable = False)
    # uid = db.Column(db.Integer, nullable = False)
    # order_type = db.Column(db.String(20),nullable = False)
    # flavor = db.Column(db.String(20),nullable = False)
    # min_quantity = db.Column(db.Integer)

    def __repr__(self):
        return f"Stock('{self.stock_code}','{self.trade_type}','{self.price}','{self.quantity}')"

class Trade(db.Model):
    buyer_id = db.Column(db.Integer, nullable = False)
    seller_id = db.Column(db.Integer,nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Float, nullable = False)
    stock_code = db.Column(db.Integer, db.ForeignKey('stock.stock_code'), nullable = False)
    order_id = db.Column(db.Integer, primary_key = True)