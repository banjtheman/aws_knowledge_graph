# imports:
import csv
import re 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random 

from lxml import html
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup
import re
import sys


chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless") 
browser = webdriver.Chrome(executable_path=r"webdriver/chromedriver", options=chrome_options)


web_address = "https://aws.amazon.com/products/"

page = requests.get(web_address)
html = page.text


#print(html)
soup = BeautifulSoup(html, "html.parser")

cats = soup.findAll('div',{'class':'lb-item-wrapper'})

services_array = []
for cat in cats:
    products = cat.findAll('div',{'class':'lb-content-item'})

    for product in products:
        service_object = {}

        #service_type
        service_object["service_type"] = cat.a.text.strip()

        #url
        service_object["url"] = "https://aws.amazon.com"+product.a["href"].split("/?")[0]

        #desc
        service_object["desc"] = product.a.span.text.strip()

        #name
        service_object["name"] = product.a.text.replace(product.a.span.text,"").strip()
        services_array.append(service_object)




with open('services.json', 'w') as outfile:
    json.dump(services_array, outfile)





