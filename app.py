from flask import Flask, render_template, jsonify, request
from models import OHLCV, Session
from chart import generate_chart
import pandas as pd
import numpy as np
import random
from datetime import timedelta

app = Flask(__name__)

session = Session()

def generate_ticks(ohlc_df):
    ticks = []
    for i, row in ohlc_df.iterrows():
        start_time = pd.to_datetime(row['date'])
        end_time = start_time + timedelta(minutes=1)
        num_ticks = random.randint(20, 100)
        tick_times = [start_time + (end_time - start_time) * i / num_ticks for i in range(num_ticks)]
        tick_prices = np.random.uniform(row['low'], row['high'], num_ticks)
        for tick_time, tick_price in zip(tick_times, tick_prices):
            ticks.append({'time': tick_time.isoformat(), 'price': tick_price})
    ticks_df = pd.DataFrame(ticks)
    ticks_df['time'] = pd.to_datetime(ticks_df['time'], format=None, errors='coerce')
    ticks_df = ticks_df.dropna(subset=['time'])
    ticks_df = ticks_df.sort_values(by='time').reset_index(drop=True)
    return ticks_df

def load_ohlcv_data(symbol):
    data = session.query(OHLCV).filter_by(symbol=symbol).all()
    ohlcv_data = [{
        "date": ohlcv.date,
        "open": ohlcv.open,
        "high": ohlcv.high,
        "low": ohlcv.low,
        "close": ohlcv.close,
        "volume": ohlcv.volume,
        "average": ohlcv.average,
        "barCount": ohlcv.barCount
    } for ohlcv in data]
    df = pd.DataFrame(ohlcv_data)
    df['date'] = pd.to_datetime(df['date'])
    return df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cryptos')
def get_cryptos():
    symbols = session.query(OHLCV.symbol).distinct().all()
    symbols_list = [symbol[0] for symbol in symbols]
    return jsonify(symbols_list)

@app.route('/ohlcv/<path:symbol>')
def get_ohlcv(symbol):
    data = session.query(OHLCV).filter_by(symbol=symbol).all()
    ohlcv_data = [{
        "date": ohlcv.date,
        "open": ohlcv.open,
        "high": ohlcv.high,
        "low": ohlcv.low,
        "close": ohlcv.close,
        "volume": ohlcv.volume,
        "average": ohlcv.average,
        "barCount": ohlcv.barCount
    } for ohlcv in data]
    return jsonify(ohlcv_data)

@app.route('/chart/<path:symbol>')
def get_chart(symbol):
    chart = generate_chart(symbol)
    if chart:
        return chart.show()
    else:
        return "Error generating chart", 500

@app.route('/api/get_ticks', methods=['GET'])
def get_ticks():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({'error': 'No symbol provided'}), 400

    ohlcv_data = load_ohlcv_data(symbol)
    ticks_data = generate_ticks(ohlcv_data)
    return jsonify({
        'ohlcv': ohlcv_data.to_dict(orient='records'),
        'ticks': ticks_data.to_dict(orient='records')
    })

if __name__ == '__main__':
    app.run(debug=True)
