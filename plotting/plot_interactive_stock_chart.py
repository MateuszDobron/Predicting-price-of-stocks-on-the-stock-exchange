import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

def plot_interactive_stock_chart(main_data, stock_symbol, secondary_data_path):
    
    
    # Load secondary data
    secondary_data = pd.read_csv(secondary_data_path)

    # plotting results with the indicators
    fig = plt.figure(figsize=(15, 8))
    ax_main = fig.add_axes([0.1, 0.3, 0.55, 0.6]) 

    # plotting historical price
    line_price, = ax_main.plot(main_data['Date'], main_data[f'{stock_symbol}_Close'], label=f'{stock_symbol} Close Price', color='blue')

    # Placeholder for technical indicators
    lines_indicators = { 'SMA_10': ax_main.plot([], [], label='SMA 10', color='orange')[0], 'SMA_30': ax_main.plot([], [], label='SMA 30', color='purple')[0], 'EMA_10': ax_main.plot([], [], label='EMA 10', color='cyan')[0], 'EMA_30': ax_main.plot([], [], label='EMA 30', color='magenta')[0], 'RSI_14': ax_main.plot([], [], label='RSI 14', color='green')[0], 'MACD': ax_main.plot([], [], label='MACD', color='red')[0], 'MACD_Signal': ax_main.plot([], [], label='MACD Signal', color='brown')[0], 'MACD_Diff': ax_main.bar([], [], label='MACD Histogram', color='grey') }

    # Function to update indicator lines
    def update_indicator(indicator):
        if indicator in ['SMA_10', 'SMA_30', 'EMA_10', 'EMA_30', 'RSI_14']:
            lines_indicators[indicator].set_data(main_data['Date'], main_data[f'{stock_symbol}_{indicator}'])
        elif indicator in ['MACD', 'MACD_Signal']:
            lines_indicators[indicator].set_data(main_data['Date'], main_data[f'{stock_symbol}_{indicator}'])
        elif indicator == 'MACD_Diff':
            ax_main.clear()
            ax_main.plot(main_data['Date'], main_data[f'{stock_symbol}_Close'], label=f'{stock_symbol} Close Price', color='blue')
            for other_ind in ['SMA_10', 'SMA_30', 'EMA_10', 'EMA_30', 'RSI_14', 'MACD', 'MACD_Signal']:
                if lines_indicators[other_ind].get_xdata().size > 0:  # If other indicators are already plotted
                    ax_main.plot(main_data['Date'], main_data[f'{stock_symbol}_{other_ind}'], label=lines_indicators[other_ind].get_label(), color=lines_indicators[other_ind].get_color())
            lines_indicators['MACD_Diff'] = ax_main.bar(main_data['Date'], main_data[f'{stock_symbol}_MACD_Diff'], label='MACD Histogram', color='grey')
        plt.draw()

    # Clearing indicator lines
    def clear_indicator(indicator):
        if indicator in ['SMA_10', 'SMA_30', 'EMA_10', 'EMA_30', 'RSI_14', 'MACD', 'MACD_Signal']:
            lines_indicators[indicator].set_data([], [])
        elif indicator == 'MACD_Diff':
            for bar in lines_indicators['MACD_Diff']:
                bar.remove()
            lines_indicators['MACD_Diff'] = []
        plt.draw()

    # Adding buttons for indicators
    button_positions = {'SMA_10': [0.1, 0.05, 0.1, 0.04], 'SMA_30': [0.2, 0.05, 0.1, 0.04], 'EMA_10': [0.3, 0.05, 0.1, 0.04], 'EMA_30': [0.4, 0.05, 0.1, 0.04], 'RSI_14': [0.5, 0.05, 0.1, 0.04], 'MACD': [0.6, 0.05, 0.1, 0.04], 'MACD_Signal': [0.7, 0.05, 0.1, 0.04], 'MACD_Diff': [0.8, 0.05, 0.1, 0.04]}
    buttons = {}
    for indicator, pos in button_positions.items():
        ax_button = plt.axes(pos) 
        buttons[indicator] = Button(ax_button, indicator)
        buttons[indicator].on_clicked(lambda event, ind=indicator: update_indicator(ind))

    #clearing all indicators
    ax_clear = plt.axes([0.9, 0.05, 0.1, 0.04])
    btn_clear = Button(ax_clear, 'Clear All')
    btn_clear.on_clicked(lambda event: [clear_indicator(ind) for ind in button_positions.keys()])

    #results plotting
    ax_secondary = fig.add_axes([0.7, 0.3, 0.25, 0.6])
    secondary_stock = secondary_data.columns[1].split('_')[0]
    ax_secondary.plot(secondary_data['Date'], secondary_data[f'{secondary_stock}_Close'], label=f'{secondary_stock} Close Price', color='green')

    plt.show()

