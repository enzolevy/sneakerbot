import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

import fake_useragent


def get_proxy_list(driver_path):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--user-agent={0}'.format(fake_useragent.UserAgent()))
    chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2,
                                                     "disk-cache-size": 4096})

    driver = webdriver.Chrome(driver_path, options=chrome_options)
    driver.get("https://free-proxy-list.net/")

    nb_pages = driver.find_element_by_xpath(
        "//select[@name='proxylisttable_length']//option[@value='80'][contains(text(),'80')]")
    nb_pages.click()

    search = driver.find_element_by_xpath("//input[@type='search']")
    search.send_keys("ELITE")

    proxies_pages = []
    page_buttons = range(1, 10)

    for page_button in page_buttons:
        try:
            if (page_button > 1):
                xpath = "//a[contains(text(),'{}')]".format(page_button)
                button = driver.find_element_by_xpath(xpath)
                button.click()

            proxies_html = [
                BeautifulSoup(proxy.get_attribute('innerHTML'), 'html.parser').findAll('td')
                for proxy in driver.find_elements_by_xpath("//section[@id='list']//tbody//tr")
            ]

            proxies_pages.append(
                pd.DataFrame([{
                    'IP': proxy[0].get_text(),
                    'Port': proxy[1].get_text(),
                    'Code': proxy[2].get_text(),
                    'Country': proxy[3].get_text(),
                    'Anonymity': proxy[4].get_text(),
                    'Google': proxy[5].get_text(),
                    'Https': proxy[6].get_text(),
                    'Last checked': proxy[7].get_text()
                } for proxy in proxies_html
                ]))

            time.sleep(2)

        except:
            pass

    driver.quit()

    proxies = pd.concat(proxies_pages)
    proxies = proxies.loc[proxies['Https'] == 'yes']
    print("Proxy retrieved : ", proxies.shape[0])

    return proxies
