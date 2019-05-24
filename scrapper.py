import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from itertools import cycle
from proxies import get_proxy_list
import fake_useragent
import time

def get_bs_obj(driver_path, url, ip, port):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--proxy-server=http://{0}:{1}'.format(ip, port))
    chrome_options.add_argument('--user-agent={0}'.format(fake_useragent.UserAgent()))

    driver = webdriver.Chrome(driver_path)

    driver.get(url)

    html = driver.page_source

    driver.quit()

    return BeautifulSoup(html, "html.parser")

def get_sneakers(bs_obj):
    return [
        get_sneaker(li) for li in bs_obj.find("ul", {"class":"listProducts"}).findAll('li')
    ]

def get_sneaker(li):
    return {
        'image' : li.find('picture').find('source').attrs['data-srcset'],
        'title' : li.find('span', {"class":"itemTitle"}).find('a').get_text(),
        'link'  : li.find('span', {"class":"itemTitle"}).find('a').attrs['href'],
        'price' : li.find('span', {"class":"pri"}).get_text()
    }

def get_urls(driver_path, url, ip, port):
    bs_obj = get_bs_obj(driver_path, url, ip , port)
    nb_pages = int(str(bs_obj.find("div", {"class":"pageCount"})).split()[2])
    return [
        url + '?from={0}'.format(24*x)
        for x in range(0, int(nb_pages/24)+1) if x <= nb_pages
    ]

def get_page(driver_path, url, ip, port):
    bs_obj = get_bs_obj(driver_path, url, ip, port)
    sneakers = get_sneakers(bs_obj)
    return pd.DataFrame(sneakers)

def get_pages(driver_path, url):
    df_proxies = get_proxy_list(driver_path)
    proxies = df_proxies[['IP', 'Port']].values
    proxies_cycle = cycle(proxies)
    url_list = get_urls(driver_path, url, proxies[0], proxies[1])
    df_list = []
    for url in url_list:
        proxy = next(proxies_cycle)
        ip, port = proxy
        df_list.append(get_page(driver_path, url, ip, port))
    return df_list

def get_product_url(name, shoes_list):
    mask = shoes_list['title'].str.contains(name)
    shoe_url = shoes_list.loc[mask, ['link']].values[0][0]
    shoe_url_concatenated = 'https://www.sizeofficial.fr' + shoe_url
    return shoe_url_concatenated

def scrap_size_official(driver_path, scrap_url, infos):
    shoes_list = pd.concat(get_pages(driver_path, scrap_url))
    infos.update({'url': get_product_url(infos['product_name'], shoes_list)})
    return infos
