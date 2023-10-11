from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
<<<<<<< HEAD
import time, os


def scrape(url, ticker, output_file_name):
=======
import time


def scrape(url, output_file_name):
>>>>>>> 264900d (started preproc)
    service = Service('./chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument("--enable-javascript")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
<<<<<<< HEAD
    time.sleep(30)
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    divTag = soup.find_all("table", {"class": "table table-hover"})

    if not os.path.isdir('./data/' + ticker):
        os.makedirs('./data/' + ticker)

    text_file = open('./data/' + ticker + '/' + output_file_name + '.txt', "w")
=======
    time.sleep(20)
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    divTag = soup.find_all("table", {"class": "table table-hover"})

    text_file = open(output_file_name + '.txt', "w")
>>>>>>> 264900d (started preproc)

    for tag in divTag:
        tdTags = tag.find_all("td", {"class": "dt-val"})
        for tag in tdTags:
            print(tag.text)
            text_file.write(tag.text)

    driver.quit()
    text_file.close()
