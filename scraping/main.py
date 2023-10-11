# "https://www.financecharts.com/stocks/AAPL/growth/roe"
from scraping_function import scrape
from text_extract_function import text_extract

# scrape('https://www.financecharts.com/stocks/AAPL/income-statement/eps-basic', './AAPL_EPS')
text_extract('./AAPL_EPS', 1, 2, 'EPS', 'AAPL_EPS')