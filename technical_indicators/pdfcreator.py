import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.backends.backend_pdf import PdfPages
from indicator_descriptions import descriptions
from technical_indicators_calculation import process_csv

def plot_indicator(company, data, indicator, output_folder):
    plt.figure(figsize=(10,8))
    close_col = company + '_Close'
    base_indicator = indicator.replace(company + '_Close_', '').split('_')[0]
    if close_col in data and indicator in data:
        if 'BB' in indicator:
            plt.plot(data.index, data[close_col], label=f'{company} Close', color='blue')
            plt.plot(data.index, data[company + '_Close_BB_low'], label='BB low', color='red')
            plt.plot(data.index, data[company + '_Close_BB_high'], label='BB high', color='green')
            plt.title(f"{company} - Bollinger Bands")
        else: 
            plt.plot(data.index, data[close_col], label=f'{company} Close', color='blue')
            plt.plot(data.index, data[indicator], label=base_indicator, color='red')
            plt.title(f"{company} - {base_indicator}")
        plt.xlabel('Day of measurement')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)
        plt.subplots_adjust(bottom = 0.1)

        description = descriptions.get(base_indicator, "No description available")
        plt.figtext(0.5, 0.02, description, wrap=True, horizontalalignment = 'center', fontsize=10, va='top')

        pdf_path = os.path.join(output_folder, f"{company +' '+ base_indicator}.pdf")
        plt.savefig(pdf_path, bbox_inches='tight', format='pdf')
        plt.close()
def process_csv_and_generate_plots(input_file):
    processed_csv = process_csv(input_file)
    
    df = pd.read_csv(processed_csv)
    companies = set(col.split('_')[0] for col in df.columns if '_Close' in col)

    for company in companies:
        output_folder = os.path.join('Technical_Indicators', company)
        os.makedirs(output_folder, exist_ok=True)

        indicators = [col for col in df.columns if col.startswith(company) and col != company + '_Close']
        for indicator in indicators:
            plot_indicator(company, df, indicator, output_folder)

# Usage (to use without the app)
process_csv_and_generate_plots('dataset.csv')
