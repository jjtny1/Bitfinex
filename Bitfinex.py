import requests
import json
import hmac
import hashlib
import base64
import time

class Bitfinex:
	
	def __init__ (self,api_key, api_secret, url):
		self.api_key = api_key
		self.api_secret = api_secret
		self.url = url

	def construct_and_send(self, post_data, url_path):
		try:
			nonce = str(time.time() * 10000)
			post_data['nonce'] = nonce
			post_data['request'] = "/v1" + url_path
			post_data_encoded =  base64.b64encode(json.dumps(post_data))
			sign = hmac.new(self.api_secret, post_data_encoded, hashlib.sha384).hexdigest()
			headers = {'X-BFX-APIKEY' : self.api_key, 'X-BFX-PAYLOAD' : post_data_encoded, 'X-BFX-SIGNATURE' : sign}
			req = requests.post(self.url + url_path, data=post_data, headers=headers,timeout=15).json()
			return req
		except Exception,e: #retry on error
			print e
			time.sleep(10)
			return self.construct_and_send(post_data, url_path)

	def open_order(self):
		url_path = '/orders'
		return self.construct_and_send({},url_path)

	'''
	symbol	[string]	The name of the symbol (see `/symbols`).
	amount	[decimal]	Order size: how much to buy or sell.
	price	[price]	Price to buy or sell at. Must be positive. Use random number for market orders.
	exchange	[string]	"bitfinex"
	side	[string]	Either "buy" or "sell".
	type	[string]	Either "market" / "limit" / "stop" / "trailing-stop" / "fill-or-kill" / "exchange market" / "exchange limit" / "exchange stop" 
						/ "exchange trailing-stop" / "exchange fill-or-kill". 
						(type starting by "exchange " are exchange orders, others are margin trading orders)
	'''
	def buy(self, symbol, amount, price, type_, exchange='bitfinex'):
		post_data = {'symbol' : symbol, 'amount' : str(amount), 'price' : str(price), 'exchange' : exchange, 'side' : 'buy', 'type' : type_}
		url_path = '/order/new'
		return self.construct_and_send(post_data, url_path)

	def sell(self, symbol, amount, price, type_, exchange='bitfinex'):
		post_data = {'symbol' : symbol, 'amount' : str(amount), 'price' : str(price), 'exchange' : exchange, 'side' : 'sell', 'type' : type_}
		url_path = '/order/new'
		return self.construct_and_send(post_data, url_path)

	def cancelOrder(self, order_id):
		post_data = {'order_id' : order_id}
		url_path = '/order/cancel'
		return self.construct_and_send(post_data, url_path)

	def replaceOrder(self, order_id, symbol, amount, price, exchange, side, type_):
		post_data = post_data = {'order_id' : 'order_id', 'symbol' : symbol, 'amount' : amount, 'price' : price, 'exchange' : exchange, 'side' : side, 'type' : type_}
		url_path = '/order/cancel/replace'
		return self.construct_and_send(post_data,url_path)
	'''
	withdraw_type	[string]	can be "bitcoin", "litecoin" or "darkcoin" or "tether".
	walletselected	[string]	The wallet to withdraw from, can be "trading", "exchange", or "deposit".
	amount	[string]	Amount to withdraw.
	address	[string]	Destination address for withdrawal.
	'''
	def withdraw(self, withdraw_type, walletselected, amount, address):
		post_data = {'withdraw_type' : withdraw_type, 'walletselected' : walletselected, 'amount' : str(amount), 'address' : address}
		url_path = '/withdraw'
		return self.construct_and_send(post_data, url_path)
			
	def balances(self):
		post_data = {}
		url_path = '/balances'
		return self.construct_and_send(post_data,url_path)

	def order_book(self, symbol):
		try:
			return requests.get(self.url + '/book/' + symbol).json()
		except Exception, e:
			print e
			return self.order_book(symbol)
