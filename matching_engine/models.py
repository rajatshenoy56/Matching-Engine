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
        return f"Stock('{self.order_id}','{self.stock_code}','{self.trade_type}','{self.price}','{self.quantity}','{self.flavor}')"

class Trade(db.Model):
    trade_id = db.Column(db.Integer, primary_key = True)
    buyer_name = db.Column(db.String(20), nullable = False)
    seller_name = db.Column(db.String(20),nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Float, nullable = False)
    stock_code = db.Column(db.Integer, db.ForeignKey('stock.stock_code'), nullable = False)

    def __repr__(self):
        return f"Trade('{self.trade_id}','{self.buyer_name}','{self.seller_name}','{self.quantity}','{self.price}','{self.stock_code}')"
db.create_all()

