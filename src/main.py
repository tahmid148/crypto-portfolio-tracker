import xlwings as xw
import pandas as pd
from exchanges.mexc import initialise_mexc_spot, get_current_assets, get_open_trades
import config

file_path = '../CryptoPortfolio.xlsx'

current_positions = pd.read_excel(file_path, skiprows=5, usecols="B:K")

def fill_open_positions_table(trades):
    df = pd.DataFrame(trades)
    df['entry_price'] = df['entry_price'].astype(float)
    df['current_price'] = df['current_price'].astype(float)

    current_positions['Symbol'] = df['symbol']
    current_positions['Entry Price ($)'] = df['entry_price']
    current_positions['Cost ($)'] = df['cost']
    current_positions['Current Price ($)'] = df['current_price']
    current_positions['OrderID'] = df['order_id']
    current_positions['Quantity'] = df['quantity']
    current_positions['Value ($)'] = df['current_price'].astype(float) * df['quantity'].astype(float)
    current_positions['Exchange'] = df['exchange']
    current_positions['PnL (%)'] = df[['entry_price', 'current_price']].pct_change(axis=1)['current_price']
    current_positions['PnL ($)'] = current_positions['Value ($)'] - df['cost'].astype(float)

    print(current_positions)

    wb = xw.Book(file_path)
    sheet = wb.sheets['CEX']
    sheet.range('B7').options(index=False, header=False).value = current_positions

def main():
    mexc_client = initialise_mexc_spot()
    mexc_assets = get_current_assets(mexc_client)
    mexc_trades = get_open_trades(mexc_client, mexc_assets)

    # mexc_trades = [{'symbol': 'AMOUSDT', 'entry_price': '0.002135', 'cost': '9.9999984', 'current_price': '0.002712', 'order_id': 'C01__362920439695044609', 'exchange': 'MEXC', 'quantity': '4683.84'}, {'symbol': 'AMOUSDT', 'entry_price': '0.002295', 'cost': '9.99998055', 'current_price': '0.002712', 'order_id': 'C01__362875530103517185', 'exchange': 'MEXC', 'quantity': '4357.29'}, {'symbol': 'AMOUSDT', 'entry_price': '0.002301', 'cost': '9.99998493', 'current_price': '0.002712', 'order_id': 'C01__362854619610685441', 'exchange': 'MEXC', 'quantity': '4345.93'}, {'symbol': 'AMOUSDT', 'entry_price': '0.002398', 'cost': '4.99999786', 'current_price': '0.002712', 'order_id': 'C01__362231658994282497', 'exchange': 'MEXC', 'quantity': '2085.07'}, {'symbol': 'AMOUSDT', 'entry_price': '0.002423', 'cost': '4.99998165', 'current_price': '0.002712', 'order_id': 'C01__362230812126502913', 'exchange': 'MEXC', 'quantity': '2063.55'}]
    fill_open_positions_table(mexc_trades)    

if __name__ == "__main__":
    main()