import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from time import sleep
from lightweight_charts import Chart
import os

# Function to generate synthetic tick data based on OHLC data
def generate_ticks(ohlc_df):
    ticks = []
    
    for i, row in ohlc_df.iterrows():
        # Ensure date is in datetime format
        if isinstance(row['date'], str):
            start_time = pd.to_datetime(row['date'])
        else:
            start_time = row['date']
        
        end_time = start_time + timedelta(minutes=1)  # Assuming 1 minute interval

        # Generate random number of ticks (between 20 to 100 ticks per interval)
        num_ticks = random.randint(20, 100)
        
        # Generate synthetic tick prices
        tick_times = [start_time + (end_time - start_time) * i / num_ticks for i in range(num_ticks)]
        tick_prices = np.random.uniform(row['low'], row['high'], num_ticks)

        # Append tick data to the list
        for tick_time, tick_price in zip(tick_times, tick_prices):
            ticks.append({'time': tick_time.isoformat(), 'price': tick_price})

    # Create a DataFrame from the ticks
    ticks_df = pd.DataFrame(ticks)
    
    # Convert time to datetime, handling various formats
    ticks_df['time'] = pd.to_datetime(ticks_df['time'], format=None, errors='coerce')
    
    # Drop rows where conversion failed (if any)
    ticks_df = ticks_df.dropna(subset=['time'])
    
    # Sort by time
    ticks_df = ticks_df.sort_values(by='time').reset_index(drop=True)
    
    return ticks_df

if __name__ == '__main__':
    try:
        # Define the CSV filename and extract the symbol
        csv_filename = 'data/ADA_USDT_ohlcv_data.csv'
        symbol = os.path.basename(csv_filename).split('_')[0]  # Extract symbol from filename
        df1 = pd.read_csv(csv_filename)
        df1['date'] = pd.to_datetime(df1['date'])
        
        # Generate synthetic tick data
        ticks_df = generate_ticks(df1)
        
        # Initialize and set up the chart
        chart = Chart()
        
        # Apply styling
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
        chart.legend(visible=True, font_size=16, font_family='Arial')  # Changed font_size to 16 and font_family to 'Arial'
        chart.set(df1)
        chart.show()
        
        # Update the chart with synthetic tick data
        last_bar_time = df1['date'].max()  # Get the timestamp of the last OHLC bar
        
        for i, tick in ticks_df.iterrows():
            tick_time = tick['time']
            
            # Ensure tick timestamp is strictly after the last OHLC bar timestamp
            if tick_time > last_bar_time:
                chart.update_from_tick(tick)
                sleep(0.03)  # Control the speed of tick updates
        
        # Keep the script running to view the chart
        input("Press Enter to exit...")
        
    except Exception as e:
        print(f"An error occurred: {e}")
