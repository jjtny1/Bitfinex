from Bitfinex import Bitfinex

BFX = Bitfinex('API-KEY', 'API-SECRET', 'https://api.bitfinex.com/v1')

print BFX.order_book()
print BFX.open_order()
resp = BFX.buy('BTCUSD', 1.03, 400, "exchange market")
print resp