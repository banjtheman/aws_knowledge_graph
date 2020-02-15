import os
import json
import random
import time
import pandas as pd, numpy as np
import csv


#for all sentences check if keyword in sentence
#if keyword in sentence, add keyword to list
# we have n keywords and k setences so it will be a n*k op best case n worst case n^2
# also this is a one time think so dont worry about compute time
aws_keyword_map ={}

#some hard coded values
aws_keyword_map["S3"] = "Amazon S3"
aws_keyword_map["Amazon S3"] = "Amazon S3"
aws_keyword_map["Amazon Simple Storage Service"] = "Amazon S3"


aws_keyword_map["Amazon EC2"] = "Amazon EC2"
aws_keyword_map["EC2"] = "Amazon EC2"
aws_keyword_map["AWS EC2"] = "Amazon EC2"
aws_keyword_map["Amazon Elastic Compute Cloud"] = "Amazon EC2"
aws_keyword_map["Amazon Elastic Compute Cloud (EC2)"] = "Amazon EC2"


aws_keyword_map["AWS Shield"] = "AWS Shield"

aws_keyword_map["Amazon Elastic Block Store"] = "Amazon Elastic Block Store"
aws_keyword_map["Amazon EBS"] = "Amazon Elastic Block Store"


aws_keyword_map["Amazon Elastic File System"] = "Amazon Elastic File System"
aws_keyword_map["Amazon EFS"] = "Amazon Elastic File System"

aws_keyword_map["Elastic Load Balancers"] = "Elastic Load Balancing"
aws_keyword_map["ELB"] = "Elastic Load Balancing"

aws_keyword_map["AWS Certificate Manager"] = "AWS Certificate Manager"

services_array = []
aws_overview = []

with open('json_output/services.json') as json_file:
    services_array = json.load(json_file)

def fill_in_map():
    #add fields to keyword map
    for service in services_array:
        service_name = service["name"]
        aws_keyword_map[service_name] = service_name

def extract_json(whitepaper_json):

    #print("Creating keyword map")
    fill_in_map()

    extracted_json = []

    #iterate over the sentences
    whitepaper_sentences = whitepaper_json["sentences"]
    whitepaper_url = whitepaper_json["metadata"]["url"]
    whitepaper_name = whitepaper_json["metadata"]["name"]
    whitepaper_desc = whitepaper_json["metadata"]["desc"]
    whitepaper_topic = whitepaper_json["metadata"]["topic"]
    whitepaper_date = whitepaper_json["metadata"]["date"]

    for obj in whitepaper_sentences:

        subject = obj["subject"]
        entity = obj["entity"]
        sentence = obj["sentence"]


        #check if subject/entity is in keyword map

        if subject in aws_keyword_map:
            #print(subject)
            #check if the sentence contains any words from key map
            temp_obj = []
            for key in aws_keyword_map.keys():
                service = aws_keyword_map[key]
                if service in sentence:
                    if not service == subject:
                        temp_obj.append(service)
            
            temp_obj = set(temp_obj)
            #print(subject+"-"+str(temp_obj))

            for link in temp_obj:
                #create a linkage
                link_obj = {}
                link_obj["service1"] = subject
                link_obj["service2"] = link
                link_obj["sentence"] = sentence
                #whitepaper metadata
                link_obj["whitepaper_url"] = whitepaper_url
                link_obj["whitepaper_name"] = whitepaper_name
                link_obj["whitepaper_desc"] = whitepaper_desc
                link_obj["whitepaper_topic"] = whitepaper_topic
                link_obj["whitepaper_date"] = whitepaper_date
                extracted_json.append(link_obj)

    return extracted_json




def transform_to_kg(whitepaper_loc):
    #will soon go over all white papers at some point
    whitepaper_json = []
    with open(whitepaper_loc) as json_file:
        whitepaper_json = json.load(json_file)

    final_json = extract_json(whitepaper_json)

    return final_json



    









