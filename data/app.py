from flask import Flask, render_template, request, jsonify
from models import OHLCV, Session

app = Flask(__name__)

session = Session()

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
        "timestamp": ohlcv.timestamp,
        "open": ohlcv.open,
        "high": ohlcv.high,
        "low": ohlcv.low,
        "close": ohlcv.close,
        "volume": ohlcv.volume
    } for ohlcv in data]
    return jsonify(ohlcv_data)

if __name__ == '__main__':
    app.run(debug=True)
