import pandas as pd
from models import OHLCV, Session

def load_csv_to_db(file_path, symbol):
    df = pd.read_csv(file_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['symbol'] = symbol
    records = df.to_dict(orient='records')
    session = Session()
    for record in records:
        ohlcv = OHLCV(**record)
        session.add(ohlcv)
    session.commit()

# List of CSV files
csv_files = [
    'AUDIO_USDT_ohlcv_data.csv', 'AXS_USDT_ohlcv_data.csv', 'CHZ_USDT_ohlcv_data.csv',
    'FLOW_USDT_ohlcv_data.csv', 'MANA_USDT_ohlcv_data.csv', 'SAND_USDT_ohlcv_data.csv',
    'XRP_USDT_ohlcv_data.csv', 'LTC_USDT_ohlcv_data.csv', 'ETH_USDT_ohlcv_data.csv',
    'DOT_USDT_ohlcv_data.csv', 'BTC_USDT_ohlcv_data.csv', 'ADA_USDT_ohlcv_data.csv'
]

for csv_file in csv_files:
    symbol = csv_file.split('_')[0] + '/' + csv_file.split('_')[1]
    load_csv_to_db(csv_file, symbol)
