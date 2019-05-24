import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import fake_useragent

import time

def add_to_cart(driver, infos):
    cookie_close_1 = driver.find_element_by_class_name('cookie-msg__close')
    cookie_close_1.click()
    time.sleep(2)
    cookie_close_2 = driver.find_element_by_class_name('cookie-msg__close')
    cookie_close_2.click()

    size_list = driver.find_element_by_id("productSizeStock")
    all_size = size_list.find_elements_by_class_name("btn")
    for size in all_size:
        if (size.text == infos['size']):
            size.click()

    add_to_cart_button = driver.find_element_by_id('addToBasket')
    add_to_cart_button.click()
    driver.get('https://www.sizeofficial.fr/cart/')

def fill_checkout(infos, driver):
    #ajouter quantité chaussures

    driver.get('https://www.sizeofficial.fr/checkout/login')
    mail_container = driver.find_element_by_id('email')
    mail_container.send_keys(infos['mail'])
    mdp_container = driver.find_element_by_id('passwrd')
    mdp_container.send_keys(infos['mdp'])
    time.sleep(2)
    connect_button = driver.find_element_by_id('checkoutRegistered')
    connect_button.click()
    time.sleep(10)
    shipping_method_list = driver.find_elements_by_class_name("checkModCheckList")
    for shipping_method in shipping_method_list:
        h4 = shipping_method.find_element_by_tag_name('h4')
        if (h4.text == 'Livraison Standard'):
            shipping_btn = shipping_method.find_element_by_class_name('chkbox')
            shipping_btn.click()
    time.sleep(3)
    continue_btn = driver.find_element_by_id('continueSecurelyButton')
    continue_btn.click()
    time.sleep(3)

def pay_shoe(infos, driver):
    paypal_div = driver.find_element_by_class_name('paybyPAYPAL')
    paypal_btn = paypal_div.find_element_by_tag_name('button')
    paypal_btn.click()
    time.sleep(2)
    paypal_mail_container = driver.find_element_by_name('login_email')
    paypal_mail_container.clear()
    time.sleep(1)
    paypal_mail_container.send_keys(infos['paypal_email'])
    paypal_mdp_container = driver.find_element_by_name('login_password')
    paypal_mdp_container.clear()
    paypal_mdp_container.send_keys(infos['paypal_mdp'])
    time.sleep(1)
    continue_btn = driver.find_element_by_id('btnLogin')
    continue_btn.click()
    time.sleep(5)
    cookie_close_1 = driver.find_element_by_id('acceptAllButton')
    cookie_close_1.click()
    continue_btn_2 = driver.find_element_by_id('confirmButtonTop')
    continue_btn_2.click()


def buy_shoe(driver_path, infos):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--user-agent={0}'.format(fake_useragent.UserAgent()))
    chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2,
                                                     "disk-cache-size": 4096})
    driver = webdriver.Chrome(driver_path)

    driver.get(infos['url'])
    add_to_cart(driver, infos)
    fill_checkout(infos, driver)
    pay_shoe(infos, driver)
