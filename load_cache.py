import os
import json
import random
import time
import pandas as pd, numpy as np
import csv

import redis
from grakn.client import GraknClient


r = redis.Redis(host="localhost", port=6379, db=0)


def get_contains_map(session):

    associate_map = {}

    with session.transaction().read() as read_transaction:
        answer_iterator = read_transaction.query("match $x isa Linkage; get;")

        for answer in answer_iterator:
            concept_ret = answer.map().get("x")
            #print("Retrieved contains with id " + concept_ret.id)
            #print(answer.map())
            attr_iterator = answer.map().get("x").attributes()
            rel_iterator = answer.map().get("x").relations()
            #print(attr_iterator)

            tmp_key = ""
            tmp_weight = 10

            for attr in attr_iterator:
                if attr.type().label() == "details":
                    #print("got details")
                    #print(attr.value())
                    tmp_key = attr.value()

    
            if not tmp_key == "" :
                associate_map[tmp_key] = {}
                associate_map[tmp_key]["weight"] = tmp_weight
                associate_map[tmp_key]["id"] = concept_ret.id   


    
    jsonMap = {}

    nodes = []
    nodes_map = {}

    #the choices
    links = []
    id_counter = 1
    counter = 0 


    for key in associate_map:

        key_nodes = []
        key_json = json.loads(key)
        key_nodes.append(key_json["service1"])
        key_nodes.append(key_json["service2"])
        sentence = key_json["sentence"]


        #check if anchor node
        tmp_source = 0
        tmp_target = 0





        if key_nodes[0] not in nodes_map:
            tmp_node = {}
            tmp_node["id"] = id_counter
            tmp_node["name"] = key_nodes[0]

            #check the type
            #print(key_json["product_type"])
            # try:
            #     tmp_node["color"] = color_map[key_json["service_type"]]
            # except:
            #     tmp_node["color"] = "orange"


            tmp_node["color"] = "orange"    

            tmp_node["weight"] = 10
            tmp_node["font_size"] = 10
            nodes_map[key_nodes[0]] = id_counter
            tmp_source = id_counter
            id_counter += 1
            nodes.append(tmp_node)

        else:
            #get id
            #print("node already in")
            tmp_source = nodes_map[key_nodes[0]]


        if key_nodes[1] not in nodes_map:
            tmp_node = {}
            tmp_node["id"] = id_counter
            tmp_node["name"] = key_nodes[1]
            tmp_node["weight"] = 10
            tmp_node["font_size"] = 10
            tmp_node["color"] = "orange"
            nodes_map[key_nodes[1]] = id_counter
            tmp_target = id_counter
            id_counter += 1
            nodes.append(tmp_node)
        else:
            #already in map
            tmp_target = nodes_map[key_nodes[1]]


        #add links
        tmp_link = {}
        tmp_link["source"] = tmp_source
        tmp_link["target"] = tmp_target
        tmp_link["sentence"] = sentence
        links.append(tmp_link)




    #Transform it to the javascript format
    #{"Au to Copper":{"id":"V40997088","weight":2},"Au to Gold":{"id":"V53376","weight":1},"Au to Salt":{"id":"V41168","weight":1},"Fe to Iron":{"id":"V41033928","weight":1},"Fe to Sword":{"id":"V36936","weight":4},"H20 to Water":{"id":"V28880","weight":8}}

    # test_data = {'nodes': [{'id': 1, 'name': 'A'}, {'id': 2, 'name': 'B'}, {'id': 3, 'name': 'C'}, {'id': 4, 'name': 'D'}, {'id': 5, 'name': 'E'}, {'id': 6, 'name': 'F'}, {'id': 7, 'name': 'G'}, {'id': 8, 'name': 'H'}, {'id': 9, 'name': 'I'}, {'id': 10, 'name': 'J'}], 'links': [{'source': 1, 'target': 2}, {'source': 1, 'target': 5}, {'source': 1, 'target': 6}, {'source': 2, 'target': 3}, {'source': 2, 'target': 7}, {'source': 3, 'target': 4}, {'source': 8, 'target': 3}, {'source': 4, 'target': 5}, {'source': 4, 'target': 9}, {'source': 5, 'target': 10}]}


    jsonMap["nodes"] = nodes
    jsonMap["links"] = links

    print("done sending to redis")
    print(str(jsonMap))

    with open('nodes_links.json', 'w') as outfile:
        json.dump(jsonMap, outfile)


    r.set("nodes", json.dumps(nodes))
    r.set("links", json.dumps(links))
    #print(jsonMap)





    return jsonMap



def get_graph():
    with GraknClient(uri="localhost:48555") as client:
        with client.session(keyspace = "aws") as session:
            try:
                jsonResp = get_contains_map(session)
                print(jsonResp)
            except Exception as e:
                print(e)
                print({"error": "failed to load"})


print("loading cache")
get_graph()