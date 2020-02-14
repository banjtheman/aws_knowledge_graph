import os
import json
import random
import time
import pandas as pd, numpy as np
import csv


from grakn.client import GraknClient

services = []
linkages = []
services_map = {}

with open('json_output/services.json') as json_file:
    services = json.load(json_file)


with open('json_output/final.json') as json_file:
    linkages = json.load(json_file)


with open('json_output/services_map.json') as json_file:
    services_map = json.load(json_file)

num_max_questions = len(linkages)-1
num_max_services = len(services)-1


def make_service_map():
    service_map = {}

    for service in services:
        name = service["name"]
        service_map[name] = service
    
    with open('services_map.json', 'w') as outfile:
        json.dump(service_map, outfile)



def get_random_answers(answer):
    choices = []
    choice_counter = 0
    while choice_counter < 3:
        rand = random.randint(0,num_max_services)
        rand_answer = services[rand]["name"]
        if answer is rand_answer:
            continue
        choices.append(rand_answer)
        choice_counter += 1
    
    return choices



def pick_3_answers(random_answers,sim_answers):
    # try sim answers first
    final_answers = []

    fc_counter = 0 

    for answer in sim_answers:
        final_answers.append(answer)
        fc_counter += 1
    

    #if 0 then return random answers
    if fc_counter == 0:
        #o no need to make deep copy
        for answer in random_answers:
            final_answers.append(answer)
        return final_answers
    
    if fc_counter < 3:
        #add random answers until 3
        r_counter = 0
        while len(final_answers) < 3:        
            final_answers.append(random_answers[r_counter])
            r_counter += 1
        
        return final_answers
    
    #greater than 3
    random.shuffle(final_answers)
    return final_answers[0:3]

    

        




def get_sim_answers(session,answer):

    sim_answers = []
    #answer = "AWS Lambda"
    #print("Check this answer: "+answer)

    with session.transaction().read() as read_transaction:
        query_string = query_grakn(answer)
        answer_iterator = read_transaction.query(query_string)

        for service_answer in answer_iterator:
            #print(dir(service_answer))
            concept_ret = service_answer.get("common-service")
            #print(service_answer.map())
            #print("Retrieved contains with id " + str(concept_ret.id))
            
            attr_iterator = concept_ret.attributes()
            #rel_iterator = service_answer.map().get("x").relations()
            #print(attr_iterator)

            #prob better way to do this but grakn annoying to figure out
            for attr in attr_iterator:
                #print(attr)
                if attr.type().label() == "name":
                    #print("got name")
                    #print(attr.value())
                    sim_answers.append(attr.value())
    

    return sim_answers




def get_graph(answer):
    with GraknClient(uri="localhost:48555") as client:
        with client.session(keyspace = "aws") as session:
            try:
                jsonResp = get_sim_answers(session,answer)
                print(jsonResp)
                return jsonResp
            except Exception as e:
                print(e)
                print({"error": "failed to load"})

def query_grakn(answer):
    grakn_query = 'match $common-service isa Service, has name $name; $service-a isa Service, has name "'+answer+'";(linked: $service-a, linker: $common-service) isa Linkage; get;'
    return grakn_query


def gen_question():

    #query knowledge graph???

    #pick a random int
    question_json = {}

    rand = random.randint(0,num_max_questions)
    
    senetence = linkages[rand]["sentence"]
    answer = linkages[rand]["service2"]
    topic = linkages[rand]["service1"]
    blank_string ="____________ "
    hint = services_map[answer]["desc"] 

    fill_in_blank_question = senetence.replace(answer,blank_string)
    #print(senetence)
    #print("answer: "+answer)
    #print("topic: "+topic)
    print(fill_in_blank_question)

    
    random_answers = get_random_answers(answer)
    #print(random_answers)

    sim_answers = get_graph(answer)



    hard_answers = pick_3_answers(random_answers,sim_answers)
    hard_answers.append(answer)

    final_answers = random_answers
    final_answers.append(answer)

    random.shuffle(final_answers)
    random.shuffle(hard_answers)


    question_json["answer"] = answer
    question_json["choices"] = final_answers
    question_json["hard_choices"] = hard_answers
    question_json["question"] = fill_in_blank_question
    question_json["hint"] = hint
    question_json["whitepaper"] = "white_paper name"
    question_json["whitepaper_url"] = "whitepaper url"

    print("Json:\n\n")

    print(question_json)
    print("\n\n")

    return(question_json)







def main():
    print("Generating questions...")
    qcounter = 0
    questions = []
    while qcounter < 10:
        questions.append(gen_question())
        qcounter += 1
    
    with open('quiz.json', 'w') as outfile:
        json.dump(questions, outfile)



main()

