from binance_interface.api import API
from binance_interface.app.utils import eprint

if __name__ == '__main__':
    proxy_host = 'http://43.156.53.213'  # Binance_resender地址
    api = API(proxy_host=proxy_host)
    ticker_result = api.spot.market.get_ticker_bookTicker(symbol='BTCUSDT')
    eprint(ticker_result)
