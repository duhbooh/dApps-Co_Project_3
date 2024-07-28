import pandas as pd
from models import OHLCV, Session

def load_csv_to_db(file_path, symbol):
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])  # Changed from 'timestamp' to 'date'
    df['symbol'] = symbol
    records = df.to_dict(orient='records')
    session = Session()
    for record in records:
        ohlcv = OHLCV(**record)
        session.add(ohlcv)
    session.commit()

# List of CSV files in the data folder
csv_files = [
    'data/AUDIO_USDT_ohlcv_data.csv', 'data/AXS_USDT_ohlcv_data.csv', 'data/CHZ_USDT_ohlcv_data.csv',
    'data/FLOW_USDT_ohlcv_data.csv', 'data/MANA_USDT_ohlcv_data.csv', 'data/SAND_USDT_ohlcv_data.csv',
    'data/XRP_USDT_ohlcv_data.csv', 'data/LTC_USDT_ohlcv_data.csv', 'data/ETH_USDT_ohlcv_data.csv',
    'data/DOT_USDT_ohlcv_data.csv', 'data/BTC_USDT_ohlcv_data.csv', 'data/ADA_USDT_ohlcv_data.csv'
]

for csv_file in csv_files:
    symbol = csv_file.split('/')[1].split('_')[0] + '/' + csv_file.split('/')[1].split('_')[1]
    load_csv_to_db(csv_file, symbol)
