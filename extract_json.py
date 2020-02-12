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

#this is the time consuming annoying part
aws_keyword_map["S3"] = "Amazon S3"
aws_keyword_map["Amazon S3"] = "Amazon S3"
aws_keyword_map["Amazon Simple Storage Service"] = "Amazon S3"


aws_keyword_map["Amazon EC2"] = "Amazon EC2"
aws_keyword_map["EC2"] = "Amazon EC2"
aws_keyword_map["AWS EC2"] = "Amazon EC2"


aws_keyword_map["AWS Shield Advanced"] = "AWS Shield Advanced"

aws_keyword_map["Amazon Elastic Block Store"] = "Amazon Elastic Block Store"
aws_keyword_map["Amazon EBS"] = "Amazon Elastic Block Store"


aws_keyword_map["Amazon Elastic File System"] = "Amazon Elastic File System"
aws_keyword_map["Amazon EFS"] = "Amazon Elastic File System"

aws_keyword_map["Elastic Load Balancers"] = "Elastic Load Balancers"
aws_keyword_map["ELB"] = "Elastic Load Balancers"

aws_keyword_map["AWS Certificate Manager"] = "AWS Certificate Manager"

aws_service_map = []





def extract_json(service_object):
	print("hello")









