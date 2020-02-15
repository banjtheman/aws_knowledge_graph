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


web_address = "https://aws.amazon.com/whitepapers/?awsm.page-whitepapers-main="
whitepapers_array = []


def parse_white_paper_page(page):
    browser.get(web_address+str(page))
    whitepapers = browser.find_elements_by_class_name("m-card-container")
    


    
    for whitepaper in whitepapers:


        whitepaper_object = {}

        whitepaper_object["whitepaper_type"] = whitepaper.find_element_by_xpath('.//div[@class="m-hd"]//h3[@class="m-category"]//span').get_attribute("innerHTML")

        #url
        whitepaper_object["url"] = whitepaper.find_element_by_xpath('.//div[@class="m-card-main"]//div[@class="m-content"]//h2[@class="m-headline m-truncate"]//a').get_attribute("href")

        #print(whitepaper_object["url"])

        #name
        whitepaper_object["name"] = whitepaper.find_element_by_xpath('.//div[@class="m-card-main"]//div[@class="m-content"]//h2[@class="m-headline m-truncate"]//a').get_attribute("innerHTML").strip()

        #print(whitepaper_object["name"])

        #desc
        whitepaper_object["desc"] = whitepaper.find_element_by_xpath('.//div[@class="m-card-main"]//div[@class="m-content"]//div[@class="m-desc"]').get_attribute("innerHTML").strip().split("<p>")[0]


        #print(whitepaper_object["desc"])

        #topic
        try:
            whitepaper_object["topic"] = whitepaper.find_element_by_xpath('.//div[@class="m-card-main"]//div[@class="m-content"]//div[@class="m-desc"]//p[@class="m-subheadline"]').get_attribute("innerHTML").strip()
        except:
            #hardcode for one pesky pdf on page 18 thats not tagged
            whitepaper_object["topic"] = "Security, Identity, & Compliance"


        #print(whitepaper_object["topic"])


        #date
        whitepaper_object["date"] = whitepaper.find_element_by_xpath('.//div[@class="m-ft"]//div[@class="m-ft-info"]//div[@class="m-info-txt"]').get_attribute("innerHTML").strip()

        #print(whitepaper_object["date"])


        whitepapers_array.append(whitepaper_object)




def main():
    print("Getting whitepapers")
    page_counter = 1
    parse_white_paper_page(page_counter)

    #ran into some overlap issues? can just run 22 times lol
    # while page_counter < 22:
    #     parse_white_paper_page(page_counter)
    #     print("Page "+str(page_counter)+" done")
    #     page_counter += 1


    # print(str(whitepapers_array))
    

    file_name = "whitepapers_json/whitepaper-"+str(page_counter)+".json"

    with open(file_name, 'w') as outfile:
        json.dump(whitepapers_array, outfile)

    browser.close()


main()


