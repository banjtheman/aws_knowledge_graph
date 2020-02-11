import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
import pprint


nlp = en_core_web_sm.load()


page = open('page.txt', 'r').read()

#nlp work here
doc_nlp = nlp(page)


sentences = list(doc_nlp.sents)
pp = pprint.PrettyPrinter(indent=4)


pp.pprint(sentences)