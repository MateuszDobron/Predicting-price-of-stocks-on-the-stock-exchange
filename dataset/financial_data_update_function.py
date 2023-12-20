from scraping_financecharts import scrape_financecharts
from extract_financecharts_function import extract_financecharts
from scraping_yahoo import scrape_yahoo
from extract_moneysupply_function import extract_moneysupply
from extract_interestratesbonds_function import extract_interestratesbonds
from extract_cpi_function import extract_cpi
from extract_yahoo_function import extract_yahoo
import os

def financial_data_update():
    print('dataset financial data update, need to change to 20y interval each time')

    print('https://finance.yahoo.com/calendar/earnings?symbol=AAPL')
    scrape_yahoo('https://finance.yahoo.com/calendar/earnings?symbol=AAPL', './dataset/data/AAPL/dates')
    extract_yahoo('./dataset/data/AAPL/dates')

    print('./dataset/data/AAPL/AAPL_ROA')
    scrape_financecharts('https://www.financecharts.com/stocks/AAPL/growth/roa', './dataset/data/AAPL/AAPL_ROA')
    input("Check for redundance in file and press enter when ready")
    extract_financecharts(3, 4, 'ROA', 'AAPL')

    print('./dataset/data/AAPL/AAPL_ROE')
    scrape_financecharts('https://www.financecharts.com/stocks/AAPL/growth/roe', './dataset/data/AAPL/AAPL_ROE')
    input("Check for redundance in file and press enter when ready")
    extract_financecharts(3, 4, 'ROE', 'AAPL')

    print('./dataset/data/AAPL/AAPL_EPS')
    scrape_financecharts('https://www.financecharts.com/stocks/AAPL/income-statement/eps-basic', './dataset/data/AAPL/AAPL_EPS')
    input("Check for redundance in file and press enter when ready")
    extract_financecharts(1, 2, 'EPS', 'AAPL')

    print('https://finance.yahoo.com/calendar/earnings?symbol=AMZN')
    scrape_yahoo('https://finance.yahoo.com/calendar/earnings?symbol=AMZN', './dataset/data/AMZN/dates')
    extract_yahoo('./dataset/data/AMZN/dates')

    print('./dataset/data/AMZN/AMZN_ROA')
    scrape_financecharts('https://www.financecharts.com/stocks/AMZN/growth/roa', './dataset/data/AMZN/AMZN_ROA')
    input("Check for redundance in file and press enter when ready")
    extract_financecharts(3, 4, 'ROA', 'AMZN')

    print('./dataset/data/AMZN/AMZN_ROE')
    scrape_financecharts('https://www.financecharts.com/stocks/AMZN/growth/roe', './dataset/data/AMZN/AMZN_ROE')
    input("Check for redundance in file and press enter when ready")
    extract_financecharts(3, 4, 'ROE', 'AMZN')

    print('./dataset/data/AMZN/AMZN_EPS')
    scrape_financecharts('https://www.financecharts.com/stocks/AMZN/income-statement/eps-basic', './dataset/data/AMZN/AMZN_EPS')
    input("Check for redundance in file and press enter when ready")
    extract_financecharts(1, 2, 'EPS', 'AMZN')

    print('https://finance.yahoo.com/calendar/earnings?symbol=AMD')
    scrape_yahoo('https://finance.yahoo.com/calendar/earnings?symbol=AMD', './dataset/data/AMD/dates')
    extract_yahoo('./dataset/data/AMD/dates')

    print('./dataset/data/AMD/AMD_ROA')
    scrape_financecharts('https://www.financecharts.com/stocks/AMD/growth/roa', './dataset/data/AMD/AMD_ROA')
    input("Check for redundance in file and press enter when ready")
    extract_financecharts(3, 4, 'ROA', 'AMD')

    print('./dataset/data/AMD/AMD_ROE')
    scrape_financecharts('https://www.financecharts.com/stocks/AMD/growth/roe', './dataset/data/AMD/AMD_ROE')
    input("Check for redundance in file and press enter when ready")
    extract_financecharts(3, 4, 'ROE', 'AMD')

    print('./dataset/data/AMD/AMD_EPS')
    scrape_financecharts('https://www.financecharts.com/stocks/AMD/income-statement/eps-basic', './dataset/data/AMD/AMD_EPS')
    input("Check for redundance in file and press enter when ready")
    extract_financecharts(1, 2, 'EPS', 'AMD')

    print('https://finance.yahoo.com/calendar/earnings?symbol=MSFT')
    scrape_yahoo('https://finance.yahoo.com/calendar/earnings?symbol=MSFT', './dataset/data/MSFT/dates')
    extract_yahoo('./dataset/data/MSFT/dates')

    print('./dataset/data/MSFT/MSFT_ROA')
    scrape_financecharts('https://www.financecharts.com/stocks/MSFT/growth/roa', './dataset/data/MSFT/MSFT_ROA')
    input("Check for redundance in file and press enter when ready")
    extract_financecharts(3, 4, 'ROA', 'MSFT')

    print('./dataset/data/MSFT/MSFT_ROE')
    scrape_financecharts('https://www.financecharts.com/stocks/MSFT/growth/roe', './dataset/data/MSFT/MSFT_ROE')
    input("Check for redundance in file and press enter when ready")
    extract_financecharts(3, 4, 'ROE', 'MSFT')

    print('./dataset/data/MSFT/MSFT_EPS')
    scrape_financecharts('https://www.financecharts.com/stocks/MSFT/income-statement/eps-basic', './dataset/data/MSFT/MSFT_EPS')
    input("Check for redundance in file and press enter when ready")
    extract_financecharts(1, 2, 'EPS', 'MSFT')

    print('https://finance.yahoo.com/calendar/earnings?symbol=NVDA')
    scrape_yahoo('https://finance.yahoo.com/calendar/earnings?symbol=NVDA', './dataset/data/NVDA/dates')
    extract_yahoo('./dataset/data/NVDA/dates')

    print('./dataset/data/NVDA/NVDA_ROA')
    scrape_financecharts('https://www.financecharts.com/stocks/NVDA/growth/roa', './dataset/data/NVDA/NVDA_ROA')
    input("Check for redundance in file and press enter when ready")
    extract_financecharts(3, 4, 'ROA', 'NVDA')

    print('./dataset/data/NVDA/NVDA_ROE')
    scrape_financecharts('https://www.financecharts.com/stocks/NVDA/growth/roe', './dataset/data/NVDA/NVDA_ROE')
    input("Check for redundance in file and press enter when ready")
    extract_financecharts(3, 4, 'ROE', 'NVDA')

    print('./dataset/data/NVDA/NVDA_EPS')
    scrape_financecharts('https://www.financecharts.com/stocks/NVDA/income-statement/eps-basic', './dataset/data/NVDA/NVDA_EPS')
    input("Check for redundance in file and press enter when ready")
    extract_financecharts(1, 2, 'EPS', 'NVDA')

    if os.path.exists('./dataset/data/MoneySupply/FRB_H6.csv'):
        os.remove('./dataset/data/MoneySupply/FRB_H6.csv')
    print('now go to the specified website')
    print('https://www.federalreserve.gov/datadownload/Choose.aspx?rel=H6')
    print('download monthly data and put it as ./dataset/data/MoneySupply/FRB_H6.csv')
    input("press enter when ready")
    # macro data https://www.federalreserve.gov/datadownload/Choose.aspx?rel=H6
    extract_moneysupply()

    if os.path.exists('./dataset/data/InterestRatesBonds/daily-treasury-rates_2023.csv'):
        os.remove('./dataset/data/InterestRatesBonds/daily-treasury-rates_2023.csv')
    print('now go to the specified website')
    print('https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2023')
    print('2023 -> apply -> download CSV')
    print('add _2023 at the file name')
    print('put it as ./dataset/data/InterestRatesBonds/daily-treasury-rates_2023.csv')
    input("press enter when ready")
    # https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2023
    extract_interestratesbonds()

    if os.path.exists('./dataset/data/CPI/SeriesReport.xlsx'):
        os.remove('./dataset/data/CPI/SeriesReport.xlsx')
    if os.path.exists('./dataset/data/CPI/SeriesReport.csv'):
        os.remove('./dataset/data/CPI/SeriesReport.csv')
    if os.path.exists('./dataset/data/CPI/CPI.csv'):
        os.remove('./dataset/data/CPI/CPI.csv')
    print('now go to the specified website')
    print('https://data.bls.gov/timeseries/CUUR0000SA0?years_option=all_years')
    print('dowload .xlsx and change name to SeriesReport.xlsx')
    print('open it in xlsx editor and remove all rows up to (not including) year jan feb ...')
    print('put it as ./dataset/data/CPI/SeriesReport.xlsx')
    input("press enter when ready")
    # https://data.bls.gov/timeseries/CUUR0000SA0?years_option=all_years
    extract_cpi()
