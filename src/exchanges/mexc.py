from mexc_sdk import Spot
from config import MEXC_ACCESS_KEY, MEXC_SECRET_KEY


def initialise_mexc_spot():
    return Spot(api_key=MEXC_ACCESS_KEY, api_secret=MEXC_SECRET_KEY)

def get_current_assets(spot_client: Spot):
    return [balance_info['asset'] for balance_info in spot_client.account_info()['balances'] if balance_info['asset'] != "USDT"]


def get_open_trades(spot_client: Spot, assets):
    trades = []
    for asset in assets:
        trade_list = spot_client.account_trade_list(asset + "USDT")
        for trade in trade_list:
            symbol = trade['symbol']
            quantity = trade['qty']
            entry_price = trade['price']
            current_price = spot_client.ticker_price(symbol)['price']
            cost = trade['quoteQty']
            order_id = trade['orderId']
            trades.append({"symbol": symbol, "entry_price": entry_price, "cost": cost, "current_price": current_price, "order_id": order_id, "exchange": "MEXC", "quantity": quantity})
    return trades

spot = initialise_mexc_spot()
print(get_open_trades(spot, get_current_assets(spot)))