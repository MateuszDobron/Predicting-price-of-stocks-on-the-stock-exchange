# "https://www.financecharts.com/stocks/AAPL/growth/roe"
from scraping_function import scrape
from extract_financecharts_function import extract_financecharts
from extract_moneysupply_function import extract_moneysupply
from extract_interestratesbonds_function import extract_interestratesbonds
from extract_cpi_function import extract_cpi

# scrape('https://www.financecharts.com/stocks/AAPL/growth/roa', 'AAPL', 'AAPL_ROA')
extract_financecharts('./data/AAPL/AAPL_ROA', 3, 4, 'ROA')

# macro data https://www.federalreserve.gov/datadownload/Choose.aspx?rel=H6
# extract_moneysupply()

# https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2023
# extract_interestratesbonds()

# https://data.bls.gov/timeseries/CUUR0000SA0?years_option=all_years
# extract_cpi()
