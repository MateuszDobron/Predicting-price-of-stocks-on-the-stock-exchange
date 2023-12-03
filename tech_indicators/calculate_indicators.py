import csv

def read_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
        headers = reader.fieldnames
    return data, headers

def write_csv(file_path, data, fieldnames):
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def calculate_sma(prices, window):
    return sum(prices[-window:]) / window if len(prices) >= window else None

def calculate_ema(prices, window):
    ema = []
    multiplier = 2 / (window + 1)
    for i, price in enumerate(prices):
        if i < window - 1:
            continue
        elif i == window - 1:
            sma = sum(prices[:window]) / window
            ema.append(sma)
        else:
            ema.append((price - ema[-1]) * multiplier + ema[-1])
    return ema[-1] if ema else None

def calculate_rsi(prices, window):
    if len(prices) < window:
        return None
    gains, losses = 0, 0
    for i in range(1, window):
        delta = prices[i] - prices[i - 1]
        if delta > 0:
            gains += delta
        else:
            losses -= delta
    avg_gain = gains / window
    avg_loss = losses / window
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calculate_macd(prices):
    ema12 = calculate_ema(prices, 12)
    ema26 = calculate_ema(prices, 26)
    macd = ema12 - ema26 if ema12 and ema26 else None
    signal = calculate_ema(prices[-26:], 9) if len(prices) >= 26 else None
    macd_diff = macd - signal if macd and signal else None
    return macd, signal, macd_diff

# Extracting stock names from headers
def extract_stock_names(headers):
    return list(set([header.split('_')[0] for header in headers if '_' in header]))

# Main logic
file_path = 'your_dataset.csv'  # Replace with your dataset file path
data, headers = read_csv(file_path)
stocks = extract_stock_names(headers)

# Add new fields for indicators
fieldnames = headers.copy()
for stock in stocks:
    fieldnames.extend([f'{stock}_SMA_10', f'{stock}_SMA_30', f'{stock}_EMA_10', f'{stock}_EMA_30', f'{stock}_RSI_14', f'{stock}_MACD', f'{stock}_MACD_Signal', f'{stock}_MACD_Diff'])

# Calculate indicators
for row in data:
    for stock in stocks:
        prices = [float(row[f'{stock}_Close']) for row in data[:data.index(row) + 1] if f'{stock}_Close' in row and row[f'{stock}_Close']]
        row[f'{stock}_SMA_10'] = calculate_sma(prices, 10)
        row[f'{stock}_SMA_30'] = calculate_sma(prices, 30)
        row[f'{stock}_EMA_10'] = calculate_ema(prices, 10)
        row[f'{stock}_EMA_30'] = calculate_ema(prices, 30)
        row[f'{stock}_RSI_14'] = calculate_rsi(prices, 14)
        macd, signal, macd_diff = calculate_macd(prices)
        row[f'{stock}_MACD'] = macd
        row[f'{stock}_MACD_Signal'] = signal
        row[f'{stock}_MACD_Diff'] = macd_diff

# Save the results to a new CSV file
output_file = 'stocks_with_indicators.csv'
write_csv(output_file, data, fieldnames)
