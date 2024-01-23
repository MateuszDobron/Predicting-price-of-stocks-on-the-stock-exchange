import pandas as pd
import os

def manual_sma(data, window):
    return sum(data[-window:]) / window

def manual_ema(data, window):
    ema = [sum(data[:window]) / window]
    multiplier = 2 / (window + 1)
    for price in data[window:]:
        ema.append((price - ema[-1]) * multiplier + ema[-1])
    return ema[-1]

def manual_rsi(data, window):
    gains = losses = 0
    for i in range(1, window):
        delta = data[i] - data[i - 1]
        if delta > 0:
            gains += delta
        else:
            losses -= delta

    average_gain = gains / window
    average_loss = losses / window

    if average_loss == 0:
        return 100
    rs = average_gain / average_loss
    return 100 - (100 / (1 + rs))

def manual_bollinger_bands(data, window):
    sma = manual_sma(data, window)
    squared_diffs = [(x - sma) ** 2 for x in data[-window:]]
    std_dev = (sum(squared_diffs) / window) ** 0.5
    return sma + 2 * std_dev, sma - 2 * std_dev
    
def calculate_macd(data):
    span1 = 12
    span2 = 26
    signal_span = 9
    ema_fast = data.ewm(span=span1, adjust=False).mean()
    ema_slow = data.ewm(span=span2, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal_span, adjust=False).mean()
    return macd_line, signal_line

def process_csv(input_file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, input_file_name)
    output_file = os.path.join(script_dir, 'technical_indicators.csv')

    df = pd.read_csv(input_file)
    close_columns = [col for col in df.columns if col.endswith('_Close')]
    window = 30
    
    final_df = pd.DataFrame()

    for col in close_columns:
        data = df[col].tail(30 + window - 1).tolist()
        final_df[col] = df[col].tail(30)
        final_df.loc[df.index[-30:], col + '_SMA'] = [round(manual_sma(data[i:i + window], window), 2) for i in range(30)]
        final_df.loc[df.index[-30:], col + '_EMA'] = [round(manual_ema(data[:i + window], window), 2) for i in range(30)]
        final_df.loc[df.index[-30:], col + '_RSI'] = [round(manual_rsi(data[i:i + window], window), 2) for i in range(30)]
        bb_high, bb_low = zip(*[manual_bollinger_bands(data[i:i + window], window) for i in range(30)])
        final_df.loc[df.index[-30:], col + '_BB_high'] = [round(val, 2) for val in bb_high]
        final_df.loc[df.index[-30:], col + '_BB_low'] = [round(val, 2) for val in bb_low]
        macd_line, signal_line = calculate_macd(df[col].tail(30))
        final_df[col + '_MACD'] = macd_line.tail(30).tolist()
        final_df[col + '_MACD_Signal'] = signal_line.tail(30).tolist()

    final_df.to_csv(output_file, index=False)

    return output_file

