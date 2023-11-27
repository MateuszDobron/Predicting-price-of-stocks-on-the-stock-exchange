from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time, os

# required to have selenium at least 4.0
def scrape(url, output_file_name):
    # service = Service('/scraping/chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument("--enable-javascript")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(30)
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    divTag = soup.find_all("table", {"class": "table table-hover"})

    if os.path.exists(output_file_name+'.txt'):
        os.remove(output_file_name+'.txt')

    text_file = open(output_file_name + '.txt', "w")

    for tag in divTag:
        tdTags = tag.find_all("td", {"class": "dt-val"})
        for tag in tdTags:
            print(tag.text)
            text_file.write(tag.text)

    driver.quit()
    text_file.close()
