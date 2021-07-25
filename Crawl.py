from selenium import webdriver
import sys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def CrawlPools():
    PATH = '/usr/local/bin/chromedriver'
    driver = webdriver.Chrome(PATH)

    driver.get("https://miningpoolstats.stream/")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "coins"))
    )

    sys.stdout = open("CoinStats/home.txt", "w")
    print(driver.page_source)

    element = driver.find_element_by_xpath(
        '/html[1]/body[1]/div[1]/div[1]/section[1]/table[1]/tbody[1]/tr[1]/td[2]/div[2]/'
        'div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/table[1]/tbody[1]')

    links = element.find_elements_by_class_name('homeurl')

    linkNames = []

    for link in links:
        linkNames.append(link.find_element_by_tag_name('b').get_attribute('innerHTML'))

    for name in linkNames:
        driver.find_element_by_link_text(name).click()
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "pools"))
            )
            table = driver.page_source
            sys.stdout = open("PoolStats/" + name + ".txt", "w")
            print(table)
            driver.back()
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "coins"))
            )
        except:
            print()

    sys.stdout.close()
    driver.close()


def CrawlMiners():
    PATH = '/usr/local/bin/chromedriver'
    driver = webdriver.Chrome(PATH)

    driver.get("https://www.f2pool.com/miners")
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "listContainer"))
    )
    links = driver.find_element_by_class_name('dropdown-miner-list').find_elements_by_class_name('dropdown-item')

    for link in links:
        driver.find_element_by_class_name('dropdown-miner-list').click()
        name = link.get_attribute('data-display_currency_code')
        driver.find_element_by_link_text(name).click()
        try:
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "listContainer"))
            )
            sys.stdout = open("MinerStats/" + name + ".txt", "w")
            print(driver.page_source)
        except:
            print()

    driver.close()


def main():
    CrawlPools()
    CrawlMiners()


if __name__ == "__main__":
    main()