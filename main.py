import pandas as pd
import sys

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time



from scrapper import scrap_size_official

from buyer import buy_shoe

infos = {
    'product_name':'size?',
    'size' : '2.5-5',
    'mail' : 'chaoulammar1@gmail.com',
    'mdp' : 'Sneakersbot2019',
    'paypal_email' : 'avnerammar1@gmail.com',
    'paypal_mdp': 'lalala'
    #'paypal_mdp' : 'Avammar28!'
}

driver_path = './chromedriver'

scrap_url = 'https://www.sizeofficial.fr/femme/accessoires/'

def launch_bot(driver_path, scrap_url, infos):
    scrap_size_official(driver_path, scrap_url, infos)
    buy_shoe(driver_path, infos)

def main(args):
    launch_bot(driver_path, scrap_url, infos)

if __name__ == "__main__":
    main(sys.argv[1:])
