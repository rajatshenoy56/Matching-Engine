from matching_engine.models import Stock,Trade

# order1 = Stock(order_id=1,stock_code="AMZ",trade_type="Bid", price=45, quantity= 10)
# order2 = Stock(order_id=2,stock_code="AMZ",trade_type="Ask", price=46, quantity= 5)
# order3 = Stock(order_id=3,stock_code="AMZ",trade_type ="Ask", price=47, quantity= 10)
# order4 = Stock(order_id=4,stock_code="AMZ",trade_type="Ask", price=48, quantity= 5)
# order5 = Stock(order_id=5,stock_code="AM",trade_type="Ask", price=48, quantity= 5)
# order6 = Stock(order_id=6,stock_code="AM",trade_type="Bid", price=48, quantity= 5)
# order7 = Stock(order_id=7,stock_code="AM",trade_type="Bid", quantity= 5)

class Order_Queue(object):

    def __init__(self):
        self.queue = {}
    
    def enqueue(self, order):
        if order.stock_code not in self.queue:
            self.queue[order.stock_code] = {'Bid':[],'Ask':[]}
        
        order_list = self.queue[order.stock_code][order.trade_type]
        order_list.append(order)
        # key = order.price
        # order_list = sorted(order_list, key = lambda o: key, reverse= (True if order.trade_type == 'Bid' else False))

    def match(self, order):
        match_list = []
        bid = self.queue[order.stock_code]['Bid']
        ask = self.queue[order.stock_code]['Ask']
        if order.trade_type == "Bid":
            for ask_order in ask:
                if order.quantity == ask_order.quantity:
                    match_list.append((order,ask_order,order.quantity,ask_order.price))
                    ask.remove(ask_order)
                    self.queue[order.stock_code][order.trade_type].pop()
        else:
            for bid_order in bid:
                if order.quantity == bid_order.quantity:
                    match_list.append((bid_order,order,order.quantity,bid_order.price))
                    bid.remove(bid_order)
                    self.queue[order.stock_code][order.trade_type].pop()
                
        return match_list
        
# order_queue = Order_Queue()

# order_queue.enqueue(order1)

# order_queue.enqueue(order2)
# print(order_queue.match(order2))

# order_queue.enqueue(order3)
# print(order_queue.match(order3))

# order_queue.enqueue(order4)
# print(order_queue.match(order4))

# order_queue.enqueue(order5)
# print(order_queue.match(order5))

# order_queue.enqueue(order6)
# print(order_queue.match(order6))

# order_queue.enqueue(order7)
# print(order_queue.match(order7))