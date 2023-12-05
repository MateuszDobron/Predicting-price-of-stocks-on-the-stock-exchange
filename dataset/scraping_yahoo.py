from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time, os

# required to have selenium at least 4.0
def scrape_yahoo(url, output_file_name):
    service = Service('./dataset/chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument("--enable-javascript")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    input("press enter when passed no-robot test")
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    divTag = soup.find_all("table", {"class": "W(100%)"})

    if os.path.exists(output_file_name+'.txt'):
        os.remove(output_file_name+'.txt')
    text_file = open(output_file_name + '.txt', "w")

    for tag in divTag:
        tdTags = tag.find_all("td", {"class": "Va(m) Ta(start) Pstart(15px) W(20%) Whs(nw) Ov(h) Tov(e) Fz(s)"})
        for tag in tdTags:
            # print(tag.text)
            text_file.write(tag.text + '\n')

    driver.quit()
    text_file.close()