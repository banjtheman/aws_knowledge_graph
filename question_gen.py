import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
import json
from datetime import datetime
import pprint





page = open('entities.json', 'r').read()


raw_data = json.loads(page)

#print(raw_data)
pp = pprint.PrettyPrinter(indent=4)


#To start lets do EC2

#Lets make questions using ON
for datum in raw_data:
    if "EC2" in datum["subject"]:
            print("Q: Which of these is an example of using "+datum["subject"].replace("\n", " ").strip())
            print("A: "+datum["sentence"].replace("\n", " ").strip())
            print()
            
        # if datum["verb"] == "on":
        #     #pp.pprint(datum)
        #     print("Q: Which of these is an example of running "+datum["snippet"].replace("\n", " ").strip())
        #     print("A: "+datum["sentence"].replace("\n", " ").strip())
        #     print()
        # if datum["verb"] == "with":
        #     #pp.pprint(datum)
        #     print("Q: Which of these is an example of using "+datum["subject"].replace("\n", " ").strip())
        #     print("A: "+datum["sentence"].replace("\n", " ").strip())
        #     print()
        # if datum["verb"] == "use":
        #     #pp.pprint(datum)
        #     print("Q: Which of these usecases explains how to use "+datum["subject"].replace("\n", " ").strip())
        #     print("A: "+datum["sentence"].replace("\n", " ").strip())
        #     print()


#Lets make questions using ON
for datum in raw_data:
    if "CloudWatch" in datum["subject"]:
            print("Q: Which of these is an example of using "+datum["subject"].replace("\n", " ").strip())
            print("A: "+datum["sentence"].replace("\n", " ").strip())
            print()
            
        # if datum["verb"] == "on":
        #     #pp.pprint(datum)
        #     print("Q: Which of these is an example of running "+datum["snippet"].replace("\n", " ").strip())
        #     print("A: "+datum["sentence"].replace("\n", " ").strip())
        #     print()
        # if datum["verb"] == "with":
        #     #pp.pprint(datum)
        #     print("Q: Which of these is an example of using "+datum["subject"].replace("\n", " ").strip())
        #     print("A: "+datum["sentence"].replace("\n", " ").strip())
        #     print()
        # if datum["verb"] == "use":
        #     #pp.pprint(datum)
        #     print("Q: Which of these usecases explains how to use "+datum["subject"].replace("\n", " ").strip())
        #     print("A: "+datum["sentence"].replace("\n", " ").strip())
        #     print()

#Lets make questions using ON
for datum in raw_data:
    if "Lambda" in datum["subject"]:
            print("Q: Which of these is an example of using "+datum["subject"].replace("\n", " ").strip())
            print("A: "+datum["sentence"].replace("\n", " ").strip())
            print()
            
        # if datum["verb"] == "on":
        #     #pp.pprint(datum)
        #     print("Q: Which of these is an example of running "+datum["subject"].replace("\n", " ").strip())
        #     print("A: "+datum["sentence"].replace("\n", " ").strip())
        #     print()
        # if datum["verb"] == "with":
        #     #pp.pprint(datum)
        #     print("Q: Which of these is an example of using "+datum["subject"].replace("\n", " ").strip())
        #     print("A: "+datum["sentence"].replace("\n", " ").strip())
        #     print()
        # if datum["verb"] == "use":
        #     #pp.pprint(datum)
        #     print("Q: Which of these usecases explains how to use "+datum["subject"].replace("\n", " ").strip())
        #     print("A: "+datum["sentence"].replace("\n", " ").strip())
        #     print()


#Lets make questions using ON
for datum in raw_data:
    if "S3" in datum["subject"]:
            print("Q: Which of these is an example of using "+datum["subject"].replace("\n", " ").strip())
            print("A: "+datum["sentence"].replace("\n", " ").strip())
            print()
            
        # if datum["verb"] == "on":
        #     #pp.pprint(datum)
        #     print("Q: Which of these is an example of running "+datum["subject"].replace("\n", " ").strip())
        #     print("A: "+datum["sentence"].replace("\n", " ").strip())
        #     print()
        # if datum["verb"] == "with":
        #     #pp.pprint(datum)
        #     print("Q: Which of these is an example of using "+datum["subject"].replace("\n", " ").strip())
        #     print("A: "+datum["sentence"].replace("\n", " ").strip())
        #     print()
        # if datum["verb"] == "use":
        #     #pp.pprint(datum)
        #     print("Q: Which of these usecases explains how to use "+datum["subject"].replace("\n", " ").strip())
        #     print("A: "+datum["sentence"].replace("\n", " ").strip())
        #     print()