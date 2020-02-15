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
import os


import glob
import wget


import text_analyze
import extract_json
import make_knowledge_graphy
import en_core_web_lg
#   {
#     "whitepaper_type": "Whitepaper",
#     "url": "https://d1.awsstatic.com/whitepapers/cloud-migration-main.pdf?did=wp_card&trk=wp_card",
#     "name": "Migrating Your Existing Applications to the AWS…",
#     "desc": "A phase-driven approach to cloud migration with three example scenarios.",
#     "topic": "Enterprise Apps",
#     "date": "October 2010"
#   },

nlp = en_core_web_lg.load()

def process_data():

    file_list = glob.glob("whitepapers_json/*.json")
    #file_list = ["whitepapers_test.json"]

    for json_file in file_list:
        #load data to tmp object
        with open(json_file) as whitepapers_info:
             #add tmp object to product list
             whitepapers = json.load(whitepapers_info)

             for whitepaper in whitepapers:
                 #download paper
                 url = whitepaper["url"]
                 dl_file_name = whitepaper["name"].replace(" ","_").replace("…","")
                 whitepaper["name"] = whitepaper["name"].replace("…","")
                 #dl_name = "whitepapers/"+
                 wget.download(url,"whitepapers/"+dl_file_name+".pdf")

                 #conver pdf to txt
                 #pdf2txt.py -o waf.txt AWS_Well-Architected_Framework.pdf
                 txt_location = "whitepapers_txt/"+dl_file_name+".txt"

                 cmd = "pdf2txt.py -o "+txt_location+" whitepapers/"+dl_file_name+".pdf"
                 os.system(cmd)

                 #run text_analyze
                 sentences = text_analyze.analyze_whitepaper(txt_location,nlp)

                 whitepaper_obj = {}
                 whitepaper_obj["metadata"] = whitepaper
                 whitepaper_obj["sentences"] = sentences

                 #add it all up
                 json_location = "whitepapers_final/"+dl_file_name+".json"

                 with open(json_location, 'w') as outfile:
                     json.dump(whitepaper_obj, outfile)
                

                 #convert to knowledge graph format
                 kg_format = extract_json.transform_to_kg(json_location)

                 kg_location = "whitepapers_kg/"+dl_file_name+".json"

                 with open(kg_location, 'w') as outfile:
                     json.dump(kg_format, outfile)
                
                 #add to knowledge graph
                 make_knowledge_graphy.add_linkages(kg_location)
                 print("Have added whitepaper: "+str(whitepaper["name"])+" to Knowledge graph")
                

            

process_data()