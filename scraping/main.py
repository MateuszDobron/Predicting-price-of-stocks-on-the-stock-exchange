# "https://www.financecharts.com/stocks/AAPL/growth/roe"
from scraping_function import scrape
from extract_financecharts_function import extract_financecharts
from extract_moneysupply_function import extract_moneysupply
from extract_interestratesbonds_function import extract_interestratesbonds
from extract_cpi_function import extract_cpi
import os

print('scraping data, need to change to 20y interval each time')

print('./scraping/data/AAPL/AAPL_ROA')
scrape('https://www.financecharts.com/stocks/AAPL/growth/roa', './scraping/data/AAPL/AAPL_ROA')
input("Check for redundance in file and press enter when ready")
extract_financecharts('./scraping/data/AAPL/AAPL_ROA', 3, 4, 'ROA')

print('./scraping/data/AAPL/AAPL_ROE')
scrape('https://www.financecharts.com/stocks/AAPL/growth/roe', './scraping/data/AAPL/AAPL_ROE')
input("Check for redundance in file and press enter when ready")
extract_financecharts('./scraping/data/AAPL/AAPL_ROE', 3, 4, 'ROE')

print('./scraping/data/AAPL/AAPL_EPS')
scrape('https://www.financecharts.com/stocks/AAPL/income-statement/eps-basic', './scraping/data/AAPL/AAPL_EPS')
input("Check for redundance in file and press enter when ready")
extract_financecharts('./scraping/data/AAPL/AAPL_EPS', 1, 2, 'EPS')

print('./scraping/data/AMZN/AMZN_ROA')
scrape('https://www.financecharts.com/stocks/AMZN/growth/roa', './scraping/data/AMZN/AMZN_ROA')
input("Check for redundance in file and press enter when ready")
extract_financecharts('./scraping/data/AMZN/AMZN_ROA', 3, 4, 'ROA')

print('./scraping/data/AMZN/AMZN_ROE')
scrape('https://www.financecharts.com/stocks/AMZN/growth/roe', './scraping/data/AMZN/AMZN_ROE')
input("Check for redundance in file and press enter when ready")
extract_financecharts('./scraping/data/AMZN/AMZN_ROA', 3, 4, 'ROE')

print('./scraping/data/AMZN/AMZN_EPS')
scrape('https://www.financecharts.com/stocks/AMZN/income-statement/eps-basic', './scraping/data/AMZN/AMZN_EPS')
input("Check for redundance in file and press enter when ready")
extract_financecharts('./scraping/data/AMZN/AMZN_EPS', 1, 2, 'EPS')

print('./scraping/data/GOOG/GOOG_ROA')
scrape('https://www.financecharts.com/stocks/GOOG/growth/roa', './scraping/data/GOOG/GOOG_ROA')
input("Check for redundance in file and press enter when ready")
extract_financecharts('./scraping/data/GOOG/GOOG_ROA', 3, 4, 'ROA')

print('./scraping/data/GOOG/GOOG_ROE')
scrape('https://www.financecharts.com/stocks/GOOG/growth/roe', './scraping/data/GOOG/GOOG_ROE')
input("Check for redundance in file and press enter when ready")
extract_financecharts('./scraping/data/GOOG/GOOG_ROE', 3, 4, 'ROE')

print('./scraping/data/GOOG/GOOG_EPS')
scrape('https://www.financecharts.com/stocks/GOOG/income-statement/eps-basic', './scraping/data/GOOG/GOOG_EPS')
input("Check for redundance in file and press enter when ready")
extract_financecharts('./scraping/data/GOOG/GOOG_EPS', 1, 2, 'EPS')

print('./scraping/data/MSFT/MSFT_ROA')
scrape('https://www.financecharts.com/stocks/MSFT/growth/roa', './scraping/data/MSFT/MSFT_ROA')
input("Check for redundance in file and press enter when ready")
extract_financecharts('./scraping/data/MSFT/MSFT_ROA', 3, 4, 'ROA')

print('./scraping/data/MSFT/MSFT_ROE')
scrape('https://www.financecharts.com/stocks/MSFT/growth/roe', './scraping/data/MSFT/MSFT_ROE')
input("Check for redundance in file and press enter when ready")
extract_financecharts('./scraping/data/MSFT/MSFT_ROE', 3, 4, 'ROE')

print('./scraping/data/MSFT/MSFT_EPS')
scrape('https://www.financecharts.com/stocks/MSFT/income-statement/eps-basic', './scraping/data/MSFT/MSFT_EPS')
input("Check for redundance in file and press enter when ready")
extract_financecharts('./scraping/data/MSFT/MSFT_EPS', 1, 2, 'EPS')

print('./scraping/data/NVDA/NVDA_ROA')
scrape('https://www.financecharts.com/stocks/NVDA/growth/roa', './scraping/data/NVDA/NVDA_ROA')
input("Check for redundance in file and press enter when ready")
extract_financecharts('./scraping/data/NVDA/NVDA_ROA', 3, 4, 'ROA')

print('./scraping/data/NVDA/NVDA_ROE')
scrape('https://www.financecharts.com/stocks/NVDA/growth/roe', './scraping/data/NVDA/NVDA_ROE')
input("Check for redundance in file and press enter when ready")
extract_financecharts('./scraping/data/NVDA/NVDA_ROE', 3, 4, 'ROE')

print('./scraping/data/NVDA/NVDA_EPS')
scrape('https://www.financecharts.com/stocks/NVDA/income-statement/eps-basic', './scraping/data/NVDA/NVDA_EPS')
input("Check for redundance in file and press enter when ready")
extract_financecharts('./scraping/data/NVDA/NVDA_EPS', 1, 2, 'EPS')

if os.path.exists('./scraping/data/MoneySupply/FRB_H6.csv'):
    os.remove('./scraping/data/MoneySupply/FRB_H6.csv')
print('now go to the specified website')
print('https://www.federalreserve.gov/datadownload/Choose.aspx?rel=H6')
print('download monthly data and put it as ./scraping/data/MoneySupply/FRB_H6.csv')
input("Check for redundance in file and press enter when ready")
# macro data https://www.federalreserve.gov/datadownload/Choose.aspx?rel=H6
extract_moneysupply()

if os.path.exists('./scraping/data/InterestRatesBonds/daily-treasury-rates_2023.csv'):
    os.remove('./scraping/data/InterestRatesBonds/daily-treasury-rates_2023.csv')
print('now go to the specified website')
print('https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2023')
print('2023 -> apply -> download CSV')
print('add _2023 at the file name')
print('put it as ./scraping/data/InterestRatesBonds/daily-treasury-rates_2023.csv')
# https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2023
extract_interestratesbonds()

if os.path.exists('./scraping/data/CPI/SeriesReport.csv'):
    os.remove('./scraping/data/CPI/SeriesReport.csv')
print('now go to the specified website')
print('https://data.bls.gov/timeseries/CUUR0000SA0?years_option=all_years')
print('dowload .xlsx and change name to SeriesReport.csv')
print('put it as ./scraping/data/CPI/SeriesReport.csv')
# https://data.bls.gov/timeseries/CUUR0000SA0?years_option=all_years
extract_cpi()
