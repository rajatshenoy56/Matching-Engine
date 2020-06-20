"""
Bid means Buy
Ask means Sell
"""

#Encodings for trade types
#(Change these to boolean later?)
BID=0
ASK=1



#Stores all the active but undispatched orders.
class ActiveOrdersList():
	def __init__(self):
		#The list is a list data structure.
		#We can choose another one later.
		#List for limit orders.
		self.limit_order_list=[]
		#List for market orders
		self.market_order_list=[]
	

	#A generic add as a wrapper.
	def add(self,order):
		if isinstance(order,MarketOrder):
			return self.__add_market_order(order)
		if isinstance(order,LimitOrder):
			return self.__add_limit_order(order)
		raise TypeError('Invalid order.')


	#Adding a new market order(private method)
	def __add_market_order(self,order):
		#Try to match here.
		first_match=self.match_market_order(order)
		#If unsuccessful , add it in the list.
		if first_match is None:
			self.market_order_list.append(order)
			return None
		#If successful , do not add this order but dispatch it.
		return first_match

	#Adding a new limit order(private method)
	def __add_limit_order(self,order):
		#Try to match here.
		first_match=self.match_limit_order(order)
		#If unsuccessful , add it in the list.
		if first_match is None:
			self.limit_order_list.append(order)
			return None
		#If successful , do not add this order but dispatch it.
		return first_match

	#Matching market orders.
	def match_market_order(self,order):
		#The type of trade we want to match against.
		target_trade_type=ASK if order.trade_type==BID else BID
		#Match!
		#For a market order to match , we must have:
		#	the trade type must be the opposite of the incoming order.
		#	the stock code should match.
		#	the quantity should match.
		#So we filter them out and return the first occurrence.
		for mo in self.market_order_list:
			if mo.trade_type!=target_trade_type:
				continue
			if mo.stock_code!=order.stock_code:
				continue
			if mo.quantity!=order.quantity:
				continue
			self.market_order_list.remove(mo)
			#If we don't want to return the first occurrence , append this to a list and return it.
			return mo
		return None

	#Matching limit orders.
	def match_limit_order(self,order):
		#The type of trade we want to match against.
		target_trade_type=ASK if order.trade_type==BID else BID
		#Match!
		matches=[]
		for lo in self.limit_order_list:
			if lo.trade_type!=target_trade_type:
				continue
			if lo.stock_code!=order.stock_code:
				continue
			if lo.quantity!=order.quantity:
				continue
			#The person is willing to sell at a lower price then what we asked for.
			if target_trade_type==ASK and lo.limit<=order.limit:
				matches.append(lo)
			#The person is willing to buy at a higher price then what we asked for.
			if target_trade_type==BID and lo.limit>=order.limit:
				matches.append(lo)
		#Remove the matched orders
		for matched in matches:
				self.limit_order_list.remove(matched)
		return matches if len(matches)>0 else None


	#Dump all orders to the console.
	def dump_orders(self):
		print('\n---------')
		print('Market orders:')
		for mo in self.market_order_list:
			print(mo)
		print('Limit orders:')
		for lo in self.limit_order_list:
			print(lo)
		print('---------\n')




class Order():
	_id=0
	def __init__(self,stock_code,quantity,trade_type):
		self.order_id=Order._id
		Order._id+=1
		self.stock_code=stock_code
		self.quantity=quantity
		self.trade_type=trade_type

	@classmethod
	def total_orders(cls):
		return Order._id


class MarketOrder(Order):
	def __init__(self,stock_code,quantity,trade_type):
		super().__init__(stock_code,quantity,trade_type)
	
	def __repr__(self):
		str_buffer=[]
		str_buffer.append(f'[Market Order')
		str_buffer.append(f'Order Id[{self.order_id}]')
		str_buffer.append(f'Stock Code[{self.stock_code}]')
		str_buffer.append(f'Stock Quantity[{self.quantity}]')
		action='Bid' if self.trade_type==BID else 'Ask'
		str_buffer.append(f'Trade Type[{action}]]')
		return ' : '.join(str_buffer)

	#Create a new MarketOrder object from a StopOrder passed in.
	#	so		:	The StopLimitOrder to convert
	@classmethod
	def market_from_stop(cls,so):
		return cls(so.stock_code,so.quantity,so.trade_type)


class LimitOrder(Order):
	def __init__(self,stock_code,quantity,trade_type,limit):
		super().__init__(stock_code,quantity,trade_type)
		self.limit=limit

	def __repr__(self):
		str_buffer=[]
		str_buffer.append(f'[Limit Order')
		str_buffer.append(f'Order Id[{self.order_id}]')
		str_buffer.append(f'Stock Code[{self.stock_code}]')
		str_buffer.append(f'Stock Quantity[{self.quantity}]')
		action='Bid' if self.trade_type==BID else 'Ask'
		str_buffer.append(f'Trade Type[{action}]')
		str_buffer.append(f'Limit[{self.limit}]]')
		return ' : '.join(str_buffer)

	#Create a new LimitOrder object from a StopLimitOrder passed in.
	#	slo		:	The StopLimitOrder to convert
	@classmethod
	def limit_from_stoplimit(cls,slo):
		return cls(slo.stock_code,slo.quantity,slo.trade_type,slo.limit)


class StopOrder(MarketOrder):
	inactive_orders_list=None
	def __init__(self,stock_code,quantity,trade_type,stop):
		#Ths list of inactive orders must be set before any StopOrder can be made.
		if self.__class__.inactive_orders_list is None:
			raise Exception('Inactive list not assigned.')
		super().__init__(stock_code,quantity,trade_type)
		self.stop=stop
		self.__class__.inactive_orders_list.append(self)

	#The StopOrders must share a common list of inactive orders.
	#So we set that first using a @classmethod
	@classmethod
	def set_list(cls,iol):
		if cls.inactive_orders_list is not None:
			raise Exception('Inactive list can be assigned only once.')
		cls.inactive_orders_list=iol

	def __repr__(self):
		str_buffer=[]
		str_buffer.append(f'[Stop Order')
		str_buffer.append(f'Order Id[{self.order_id}]')
		str_buffer.append(f'Stock Code[{self.stock_code}]')
		str_buffer.append(f'Stock Quantity[{self.quantity}]')
		action='Bid' if self.trade_type==BID else 'Ask'
		str_buffer.append(f'Trade Type[{action}]')
		str_buffer.append(f'Stop Value[{self.stop}]]')
		return ' : '.join(str_buffer)


class StopLimitOrder(LimitOrder):
	inactive_orders_list=None
	def __init__(self,stock_code,quantity,trade_type,limit,stop):
		#Ths list of inactive orders must be set before any StopOrder can be made.
		if self.__class__.inactive_orders_list is None:
			raise Exception('Inactive list not assigned.')
		super().__init__(stock_code,quantity,trade_type,limit)
		self.stop=stop
		self.__class__.inactive_orders_list.append(self)

	#The StopLimitOrders must share a common list of inactive orders.
	#So we set that first using a @classmethod
	@classmethod
	def set_list(cls,iol):
		if cls.inactive_orders_list is not None:
			raise Exception('Inactive list can be assigned only once.')
		cls.inactive_orders_list=iol

	def __repr__(self):
		str_buffer=[]
		str_buffer.append(f'[Stop Limit Order')
		str_buffer.append(f'Order Id[{self.order_id}]')
		str_buffer.append(f'Stock Code[{self.stock_code}]')
		str_buffer.append(f'Stock Quantity[{self.quantity}]')
		action='Bid' if self.trade_type==BID else 'Ask'
		str_buffer.append(f'Trade Type[{action}]')
		str_buffer.append(f'Limit[{self.limit}]')
		str_buffer.append(f'Stop Value[{self.stop}]]')
		return ' : '.join(str_buffer)


#Function to activate any stop/stop-limit orders given the inactive-order-list and the current maket price.
#The activated orders are immediately inserted into the ActiveOrdersList
#	iol		:	Inactive Order List
#	aol		:	Active Order List
#	cmp		:	Current Market Price
def activate(iol,aol,cmp):
	activated=[]
	for inactive in iol:
		if inactive.stop==cmp:
			activated.append(inactive)
			#If the order is of type StopOrder , we will get an exception for the 'limit' property.
			#So we use a try-except block to avoid explicit exception-checking.
			try:
				lo=LimitOrder.limit_from_stoplimit(inactive)
				try_add(aol,lo)
			except Exception:
				mo=MarketOrder.market_from_stop(inactive)
				try_add(aol,mo)
	for active in activated:
		iol.remove(active)


def try_add(aol,order):
	x=aol.add(order)
	if x is None:
		print(f'Matching for {order} is:\n{x}')
	elif isinstance(order,MarketOrder):
		print(f'Matching for {order} is:\n{x}')
	else:
		print(f'Matching for {order} is:\n')
		for mlo in x:
			print(mlo)
	aol.dump_orders()
	print()


def test1():

	#Create the order list
	aol=ActiveOrdersList()

	#Create an inactive orders list which must be shared by the StopOrder and the StopLimitOrder classes.
	#Both classes must share the same instance.
	iol=[]
	StopLimitOrder.set_list(iol)
	StopOrder.set_list(iol)

	#Add some market orders
#	mo1=MarketOrder(stock_code='S1',quantity=10,trade_type=BID)
	mo2=MarketOrder(stock_code='S2',quantity=15,trade_type=BID)
#	mo3=MarketOrder(stock_code='S1',quantity=10,trade_type=ASK)

	#Add some limit orders
	lo1=LimitOrder(stock_code='S1',quantity=10,trade_type=BID,limit=101)
#	lo2=LimitOrder(stock_code='S1',quantity=10,trade_type=BID,limit=105)
#	lo3=LimitOrder(stock_code='S1',quantity=10,trade_type=ASK,limit=103)
	lo4=LimitOrder(stock_code='S1',quantity=10,trade_type=BID,limit=107)

	#Try to add them and see the matching.

#	try_add(aol,mo1)
	try_add(aol,mo2)
#	try_add(aol,mo3)

	try_add(aol,lo1)
#	try_add(aol,lo2)
#	try_add(aol,lo3)
	try_add(aol,lo4)

	#Test case to match with lo1 , lo4
	slo1=StopLimitOrder(stock_code='S1',quantity=10,trade_type=ASK,limit=100,stop=1010)
	#Test case to match with mo2
	so1=StopOrder(stock_code='S2',quantity=15,trade_type=ASK,stop=1010)

	#Activate slo1 , try to add it into the aol and see the matching.
#	Call this whenever the market value update comes from the API.
	activate(iol,aol,cmp=1010)

if __name__=='__main__':

	test1()
