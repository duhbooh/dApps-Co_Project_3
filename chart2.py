import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from lightweight_charts import Chart
import os

# Function to generate synthetic tick data based on OHLC data
def generate_ticks(ohlc_df):
    ticks = []
    for i, row in ohlc_df.iterrows():
        start_time = pd.to_datetime(row['date']) if isinstance(row['date'], str) else row['date']
        end_time = start_time + timedelta(minutes=1)  # Assuming 1 minute interval
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

if __name__ == '__main__':
    try:
        # CSV filenames
        csv_filenames = [
            'data/ADA_USDT_ohlcv_data.csv',
            'data/AUDIO_USDT_ohlcv_data.csv',
            'data/AXS_USDT_ohlcv_data.csv',
            'data/BTC_USDT_ohlcv_data.csv',
            'data/CHZ_USDT_ohlcv_data.csv',
            'data/DOT_USDT_ohlcv_data.csv'
        ]

        # Create a list to hold chart instances
        charts = []

        # Load data and generate ticks
        for csv_filename in csv_filenames:
            symbol = os.path.basename(csv_filename).split('_')[0]
            df = pd.read_csv(csv_filename)
            df['date'] = pd.to_datetime(df['date'])
            ticks_df = generate_ticks(df)
            chart = Chart()  # Create a new chart instance
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
            chart.set(df)
            charts.append(chart)

        # Display all charts in a single instance, if the library supports it
        for chart in charts:
            chart.show(block=True)  # Ensure the display is handled in a blocking manner

        input("Press Enter to exit...")

    except Exception as e:
        print(f"An error occurred: {e}")
