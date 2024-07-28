# chart.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from lightweight_charts import Chart
import os

def generate_ticks(ohlc_df):
    ticks = []
    
    for i, row in ohlc_df.iterrows():
        if isinstance(row['date'], str):
            start_time = pd.to_datetime(row['date'])
        else:
            start_time = row['date']
        
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

from models import OHLCV, Session

def generate_chart(symbol):
    try:
        session = Session()
        ohlcv_data = session.query(OHLCV).filter_by(symbol=symbol).all()
        df1 = pd.DataFrame([{
            "date": ohlcv.date,
            "open": ohlcv.open,
            "high": ohlcv.high,
            "low": ohlcv.low,
            "close": ohlcv.close,
            "volume": ohlcv.volume,
            "average": ohlcv.average,
            "barCount": ohlcv.barCount
        } for ohlcv in ohlcv_data])

        df1['date'] = pd.to_datetime(df1['date'])
        ticks_df = generate_ticks(df1)
        
        chart = Chart()
        
        chart.layout(background_color='#090008', text_color='#FFFFFF', font_size=16, font_family='Helvetica')
        
        chart.candle_style(
            up_color='#00ff55', 
            down_color='#ed4807',
            border_up_color='#FFFFFF', 
            border_down_color='#FFFFFF',
            wick_up_color='#FFFFFF', 
            wick_down_color='#FFFFFF'
        )
        
        chart.volume_config(up_color='#00ff55', down_color='#ed4807')
        
        chart.watermark(f'1D {symbol}', color='rgba(180, 180, 240, 0.7)')
        
        chart.crosshair(
            mode='normal', 
            vert_color='#FFFFFF', 
            vert_style='dotted',
            horz_color='#FFFFFF', 
            horz_style='dotted'
        )
        chart.legend(visible=True, font_size=16, font_family='Arial')
        chart.set(df1)
        
        return chart

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
