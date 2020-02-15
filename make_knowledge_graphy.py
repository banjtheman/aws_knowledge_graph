# Python Library Imports
import os
import json
import random
import time
import pandas as pd, numpy as np
import csv

import redis
import glob
from grakn.client import GraknClient


import time

def update_knowledge_graph(services,linkages):
    with GraknClient(uri="localhost:48555") as client:
        with client.session(keyspace = "aws") as session:
            load_data_into_grakn(services,linkages, session)




def add_service(service):
    #print(str(service))
    url_string = service["url"].replace("https://","https_").replace("/","_").replace(".","_dot_")

    graql_insert_query =  'insert $c isa Service, has name "' + str(service["name"]) + '"'
    graql_insert_query += ', has service_desc "' + str(service["desc"]) + '"'
    graql_insert_query += ', has url "' + str(url_string) + '"'
    graql_insert_query += ', has service_type "' + str(service["service_type"]) + '"'
    graql_insert_query += ";"
    return graql_insert_query


def linked(linked_rel):
    # match reactor
    graql_insert_query = 'match $linked isa Service, has name "' + linked_rel["service1"] + '";'
    # match reacte
    graql_insert_query += ' $linker isa Service, has name "' + linked_rel["service2"] + '";'
    # insert reaction
    graql_insert_query += (" insert $linkage(linked: $linked, linker: $linker) isa Linkage; " + "$linkage has details '" + str(linked_rel["details"]) +"'; ")
    return graql_insert_query

def load_data_into_grakn(services,linkages,session):

    for service in services:

        # service_json = {}
        # service_json["name"] = service["name"].strip().replace("'","")
        # #hard code for now...
        # service_json["desc"] = service["desc"]
        # service_json["url"] = service["url"]
        with session.transaction().write() as transaction:
            graql_insert_query = add_service(service)
            #print("Executing Graql Query: " + graql_insert_query)
            transaction.query(graql_insert_query)
            transaction.commit()

    for linkage in linkages:
            #now create the relartionship between services
            linkage_rel = {}
            linkage_rel["service1"] = linkage["service1"].strip().replace("'","")
            linkage_rel["service2"] = linkage["service2"].strip().replace("'","")


            details_json = {}
            details_json["service1"] = linkage["service1"].strip().replace("'","")
            details_json["service2"] = linkage["service2"].strip().replace("'","")
            details_json["sentence"] = linkage["sentence"]
            #add the paper metadata
            details_json["whitepaper_url"] = linkage["whitepaper_url"]
            details_json["whitepaper_name"] = linkage["whitepaper_name"]
            details_json["whitepaper_desc"] = linkage["whitepaper_desc"]
            details_json["whitepaper_topic"] = linkage["whitepaper_topic"]
            details_json["whitepaper_date"] = linkage["whitepaper_date"]
            
            details_string = json.dumps(details_json)

            linkage_rel["details"] =  details_string
            with session.transaction().write() as transaction:
                graql_insert_query = linked(linkage_rel)
                #print("Executing Graql Query: " + graql_insert_query)
                transaction.query(graql_insert_query)
                transaction.commit()

    #print("Done and Done")

services = []
linkages = []

#this should only be done once
def add_services():
    with open('json_output/services.json') as json_file:
        services = json.load(json_file)
    update_knowledge_graph(services,[])


def add_linkages(json_loc):
    with open(json_loc) as json_file:
        linkages = json.load(json_file)    

    update_knowledge_graph([],linkages)


#add_services()